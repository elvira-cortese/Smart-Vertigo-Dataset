# -*- coding: utf-8 -*-

"""
VIDEO AUDIO REMOVAL AND QUALITY-CONTROL (QC) AUDIT

Purpose
-------
This script audits video files for the presence of audio streams and,
when requested, creates audio-free versions without re-encoding the
video stream.

The script:

1. Searches for video files within a folder and its subfolders.
2. Detects whether each video contains one or more audio streams.
3. Can create an audio-free version without re-encoding the video.
4. Verifies that:
   a) no audio stream remains,
   b) the video stream is unchanged,
   c) video duration remains within a predefined tolerance.
5. Generates CSV quality-control reports.

Requirements
------------
- Python 3
- FFmpeg, including ffprobe, installed and available on the system PATH.

IMPORTANT
---------
The default configuration is AUDIT ONLY and does not modify source files.

Before running the script, replace PATH_TO_VIDEO_FOLDER below with the
path to the folder containing the videos to be audited.
"""

from pathlib import Path
from datetime import datetime
import subprocess
import csv
import os
import shutil
import sys


# ==============================================================
# CONFIGURATION
# ==============================================================

# --------------------------------------------------------------
# (1) REQUIRED: folder containing the videos
#
# Replace PATH_TO_VIDEO_FOLDER with the appropriate local path.
#
# Windows example:
# CARPETA_VIDEOS = Path(r"C:\Data\Videos")
#
# macOS/Linux example:
# CARPETA_VIDEOS = Path("/Users/name/Data/Videos")
# --------------------------------------------------------------

CARPETA_VIDEOS = Path(r"PATH_TO_VIDEO_FOLDER")


# --------------------------------------------------------------
# (2) PROCESSING MODE
#
# REEMPLAZAR_ORIGINALES = False
#     Recommended. Original videos are not overwritten.
#
# REEMPLAZAR_ORIGINALES = True
#     Original files are replaced by the audio-free versions.
#     WARNING: original audio will be permanently removed.
#
# SOLO_REVISAR = True
#     Audit-only mode. No files are modified.
#
# SOLO_REVISAR = False
#     Audio removal is enabled according to the settings above.
# --------------------------------------------------------------

REEMPLAZAR_ORIGINALES = False
SOLO_REVISAR = True


# --------------------------------------------------------------
# (3) OPTIONAL OUTPUT FOLDERS
#
# Leave as None to create output/report folders automatically
# next to the input video folder.
# --------------------------------------------------------------

CARPETA_SALIDA = None
CARPETA_REPORTES = None


# --------------------------------------------------------------
# (4) ADVANCED OPTIONS
# --------------------------------------------------------------

# Video file extensions to process
EXTENSIONES = {".mp4", ".mov", ".m4v", ".mkv", ".avi"}

# True removes file-level metadata such as title, comments,
# location information, and device metadata.
LIMPIAR_METADATOS = False

# False removes subtitle streams, which may contain identifiable
# information.
MANTENER_SUBTITULOS = False

# True compares the video stream before and after processing.
VERIFICAR_VIDEO_IDENTICO = True

# Maximum acceptable duration difference, in seconds.
TOLERANCIA_DURACION = 0.5

# CSV separator.
# Change to ";" if required by the local spreadsheet configuration.
SEPARADOR_CSV = ","


# ==============================================================
# END OF CONFIGURATION
# ==============================================================

MARCA_TEMP = "_TEMP_NO_AUDIO"


def ejecutar(comando):
    """Run an external command and return the completed process."""
    return subprocess.run(
        comando,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def contar_streams(ruta, tipo):
    """
    Count audio ('a') or video ('v') streams in a media file.
    """
    r = ejecutar([
        "ffprobe",
        "-v", "error",
        "-select_streams", tipo,
        "-show_entries", "stream=index",
        "-of", "csv=p=0",
        str(ruta),
    ])

    if r.returncode != 0:
        raise RuntimeError(
            "ffprobe failed: " + r.stderr.strip()
        )

    return len([
        linea
        for linea in r.stdout.splitlines()
        if linea.strip()
    ])


def duracion(ruta):
    """
    Return media duration in seconds.

    Returns None if duration cannot be read.
    """
    r = ejecutar([
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        str(ruta),
    ])

    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def huella_video(ruta):
    """
    Calculate an MD5 fingerprint of the encoded video stream.

    The video stream is copied rather than decoded/re-encoded.
    Matching fingerprints therefore provide a check that the
    encoded video stream was preserved during audio removal.
    """
    r = ejecutar([
        "ffmpeg",
        "-nostdin",
        "-v", "error",
        "-i", str(ruta),
        "-map", "0:v",
        "-c", "copy",
        "-f", "md5",
        "-",
    ])

    if r.returncode != 0:
        raise RuntimeError(
            "Could not calculate video fingerprint: "
            + r.stderr.strip()
        )

    for linea in r.stdout.splitlines():
        if linea.startswith("MD5="):
            return linea.strip()

    raise RuntimeError(
        "No video fingerprint was returned."
    )


def crear_version_sin_audio(origen, destino_temp):
    """
    Create an audio-free version of a video without re-encoding
    the video stream.
    """
    comando = [
        "ffmpeg",
        "-nostdin",
        "-v", "error",
        "-y",
        "-i", str(origen),
        "-map", "0:v",
        "-c", "copy",
        "-an",
        "-dn",
        "-map_metadata",
        "-1" if LIMPIAR_METADATOS else "0",
    ]

    if MANTENER_SUBTITULOS:
        comando += ["-map", "0:s?"]
    else:
        comando += ["-sn"]

    comando.append(str(destino_temp))

    r = ejecutar(comando)

    if r.returncode != 0:
        raise RuntimeError(
            "ffmpeg failed: " + r.stderr.strip()
        )

    if not destino_temp.exists():
        raise RuntimeError(
            "Temporary output file was not created."
        )


def verificar_resultado(origen, nuevo):
    """
    Verify an audio-removed video.

    Checks:
    - absence of audio streams,
    - preservation of the number of video streams,
    - duration within the predefined tolerance,
    - video-stream fingerprint when enabled.

    Returns
    -------
    audio_despues : int
        Number of audio streams after processing.

    video_identico : str
        "YES", "NO", or "NOT CHECKED".

    problemas : list
        List of detected QC problems.
    """
    problemas = []

    audio_despues = contar_streams(nuevo, "a")

    if audio_despues != 0:
        problemas.append(
            "Audio stream remains after processing"
        )

    if contar_streams(origen, "v") != contar_streams(nuevo, "v"):
        problemas.append(
            "Number of video streams changed"
        )

    d1 = duracion(origen)
    d2 = duracion(nuevo)

    if (
        d1 is not None
        and d2 is not None
        and abs(d1 - d2) > TOLERANCIA_DURACION
    ):
        problemas.append(
            f"Duration changed "
            f"({d1:.2f}s vs {d2:.2f}s)"
        )

    if VERIFICAR_VIDEO_IDENTICO:
        if huella_video(origen) == huella_video(nuevo):
            video_identico = "YES"
        else:
            video_identico = "NO"
            problemas.append(
                "Video stream fingerprint differs from original"
            )
    else:
        video_identico = "NOT CHECKED"

    return audio_despues, video_identico, problemas


def procesar_video(video, carpeta_salida):
    """
    Audit or process a single video and return one QC-report row.
    """
    relativo = video.relative_to(CARPETA_VIDEOS)

    audio_antes = contar_streams(video, "a")

    fila = {
        "video": str(relativo),
        "audio_streams_before": audio_antes,
        "action": "",
        "audio_streams_after": "",
        "video_stream_identical": "",
        "result": "",
        "details": "",
    }

    # ----------------------------------------------------------
    # AUDIT-ONLY MODE
    # ----------------------------------------------------------

    if SOLO_REVISAR:
        fila["audio_streams_after"] = audio_antes

        if audio_antes > 0:
            fila["action"] = (
                "Audio detected; no modification performed"
            )
            fila["result"] = "PENDING"
        else:
            fila["action"] = "No audio detected"
            fila["result"] = "OK"

        return fila

    destino = (
        video
        if REEMPLAZAR_ORIGINALES
        else carpeta_salida / relativo
    )

    # ----------------------------------------------------------
    # VIDEO ALREADY HAS NO AUDIO
    # ----------------------------------------------------------

    if audio_antes == 0:

        if not REEMPLAZAR_ORIGINALES:
            destino.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(video, destino)

            if contar_streams(destino, "a") != 0:
                raise RuntimeError(
                    "Unexpected audio stream detected "
                    "in copied file."
                )

            fila["action"] = (
                "No audio; copied without modification"
            )

        else:
            fila["action"] = (
                "No audio; no modification required"
            )

        fila["audio_streams_after"] = 0
        fila["video_stream_identical"] = "N/A"
        fila["result"] = "OK"

        return fila

    # ----------------------------------------------------------
    # VIDEO CONTAINS AUDIO
    # ----------------------------------------------------------

    destino.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporal = destino.with_name(
        destino.stem
        + MARCA_TEMP
        + destino.suffix
    )

    try:
        crear_version_sin_audio(
            video,
            temporal,
        )

        (
            audio_despues,
            identico,
            problemas,
        ) = verificar_resultado(
            video,
            temporal,
        )

        fila["audio_streams_after"] = audio_despues
        fila["video_stream_identical"] = identico

        if problemas:
            raise RuntimeError(
                "; ".join(problemas)
            )

        # The final file is created only after all QC checks pass.
        os.replace(
            temporal,
            destino,
        )

    except Exception:
        if temporal.exists():
            temporal.unlink()

        raise

    fila["action"] = (
        "Audio removed"
        + (
            " (original replaced)"
            if REEMPLAZAR_ORIGINALES
            else " (saved to output folder)"
        )
    )

    fila["result"] = "OK"

    return fila


def guardar_reportes(filas, carpeta_reportes, sello):
    """
    Save complete and audio-positive QC reports as CSV files.
    """
    carpeta_reportes.mkdir(
        parents=True,
        exist_ok=True,
    )

    columnas = [
        "video",
        "audio_streams_before",
        "action",
        "audio_streams_after",
        "video_stream_identical",
        "result",
        "details",
    ]

    reporte_completo = (
        carpeta_reportes
        / f"QC_complete_{sello}.csv"
    )

    with open(
        reporte_completo,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as f:

        w = csv.DictWriter(
            f,
            fieldnames=columnas,
            delimiter=SEPARADOR_CSV,
        )

        w.writeheader()
        w.writerows(filas)

    reporte_modificados = (
        carpeta_reportes
        / f"videos_with_audio_{sello}.csv"
    )

    with open(
        reporte_modificados,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as f:

        w = csv.writer(
            f,
            delimiter=SEPARADOR_CSV,
        )

        w.writerow([
            "video",
            "action",
            "result",
        ])

        for fila in filas:
            if fila["audio_streams_before"] not in (0, ""):
                w.writerow([
                    fila["video"],
                    fila["action"],
                    fila["result"],
                ])

    return (
        reporte_completo,
        reporte_modificados,
    )


def main():

    # ----------------------------------------------------------
    # INITIAL CHECKS
    # ----------------------------------------------------------

    for programa in ("ffmpeg", "ffprobe"):

        if shutil.which(programa) is None:
            sys.exit(
                f"\nERROR: '{programa}' was not found. "
                "Install FFmpeg and ensure that ffmpeg and "
                "ffprobe are available on the system PATH."
            )

    if str(CARPETA_VIDEOS) == "PATH_TO_VIDEO_FOLDER":
        sys.exit(
            "\nERROR: CARPETA_VIDEOS has not been configured.\n"
            "Replace PATH_TO_VIDEO_FOLDER with the path to "
            "the folder containing the videos."
        )

    if not CARPETA_VIDEOS.is_dir():
        sys.exit(
            "\nERROR: video folder does not exist:\n"
            f"{CARPETA_VIDEOS}"
        )

    nombre = CARPETA_VIDEOS.name

    carpeta_salida = (
        CARPETA_SALIDA
        or CARPETA_VIDEOS.parent
        / f"{nombre}_NO_AUDIO"
    )

    carpeta_reportes = (
        CARPETA_REPORTES
        or CARPETA_VIDEOS.parent
        / f"{nombre}_QC_REPORTS"
    )

    # Prevent the output directory from being located inside
    # the source-video directory.
    if (
        not REEMPLAZAR_ORIGINALES
        and not SOLO_REVISAR
    ):

        try:
            carpeta_salida.resolve().relative_to(
                CARPETA_VIDEOS.resolve()
            )

            sys.exit(
                "\nERROR: output folder cannot be located "
                "inside the source-video folder."
            )

        except ValueError:
            pass

    # ----------------------------------------------------------
    # FIND VIDEO FILES
    # ----------------------------------------------------------

    todos = [
        p
        for p in sorted(
            CARPETA_VIDEOS.rglob("*")
        )
        if p.is_file()
    ]

    temporales = [
        p
        for p in todos
        if MARCA_TEMP in p.stem
    ]

    videos = [
        p
        for p in todos
        if (
            p.suffix.lower() in EXTENSIONES
            and MARCA_TEMP not in p.stem
        )
    ]

    print(
        "\n============================================"
    )

    if SOLO_REVISAR:
        print(
            "MODE: AUDIT ONLY "
            "(no files will be modified)"
        )

    elif REEMPLAZAR_ORIGINALES:
        print(
            "MODE: REPLACE ORIGINAL FILES "
            "(irreversible)"
        )

    else:
        print(
            "MODE: SAFE COPY "
            "(original files remain unchanged)"
        )

        print(
            f"Output folder: {carpeta_salida}"
        )

    print(
        f"Video folder: {CARPETA_VIDEOS}"
    )

    print(
        f"Videos found: {len(videos)}"
    )

    print(
        "============================================\n"
    )

    if temporales:
        print(
            f"WARNING: {len(temporales)} temporary "
            "file(s) from a previous interrupted run "
            "were found. They will be ignored.\n"
        )

    if not videos:
        sys.exit(
            "No video files with the configured "
            "extensions were found."
        )

    # ----------------------------------------------------------
    # EXTRA CONFIRMATION BEFORE OVERWRITING ORIGINALS
    # ----------------------------------------------------------

    if (
        REEMPLAZAR_ORIGINALES
        and not SOLO_REVISAR
    ):

        respuesta = input(
            "You are about to OVERWRITE the original "
            "video files.\n"
            "Confirm that a backup exists.\n"
            "Type YES in uppercase to continue: "
        )

        if respuesta.strip() != "YES":
            sys.exit(
                "Cancelled. No files were modified."
            )

    # ----------------------------------------------------------
    # PROCESSING
    # ----------------------------------------------------------

    sello = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filas = []

    try:

        for n, video in enumerate(
            videos,
            start=1,
        ):

            relativo = video.relative_to(
                CARPETA_VIDEOS
            )

            print(
                f"[{n}/{len(videos)}] {relativo}"
            )

            try:

                fila = procesar_video(
                    video,
                    carpeta_salida,
                )

                print(
                    f"   -> {fila['action']} "
                    f"[{fila['result']}]"
                )

            except Exception as error:

                print(
                    f"   ERROR: {error}"
                )

                fila = {
                    "video": str(relativo),
                    "audio_streams_before": "?",
                    "action": "ERROR",
                    "audio_streams_after": "?",
                    "video_stream_identical": "?",
                    "result": "FAILED",
                    "details": str(error),
                }

            filas.append(fila)

    except KeyboardInterrupt:

        print(
            "\nProcessing interrupted by user. "
            "Partial QC reports will be saved."
        )

    finally:

        if filas:

            rep1, rep2 = guardar_reportes(
                filas,
                carpeta_reportes,
                sello,
            )

    # ----------------------------------------------------------
    # SUMMARY
    # ----------------------------------------------------------

    con_audio = sum(
        1
        for f in filas
        if f["audio_streams_before"] not in (
            0,
            "?",
        )
    )

    fallidos = sum(
        1
        for f in filas
        if f["result"] == "FAILED"
    )

    pendientes = sum(
        1
        for f in filas
        if f["result"] == "PENDING"
    )

    print(
        "\n============================================"
    )

    print("SUMMARY")

    print(
        "============================================"
    )

    print(
        f"Videos reviewed: "
        f"{len(filas)} of {len(videos)}"
    )

    print(
        f"Videos containing audio: {con_audio}"
    )

    print(
        f"Videos with QC failure: {fallidos}"
    )

    if SOLO_REVISAR:
        print(
            f"Videos pending audio removal: "
            f"{pendientes}"
        )

    if filas:
        print(
            "\nQC reports saved to:"
            f"\n  {rep1}"
            f"\n  {rep2}"
        )

    if (
        fallidos == 0
        and pendientes == 0
        and len(filas) == len(videos)
    ):

        print(
            "\nALL VIDEOS PASSED QUALITY CONTROL"
        )

    else:

        print(
            "\nREVIEW REQUIRED: one or more videos "
            "failed QC, contain audio, or were not processed."
        )


if __name__ == "__main__":
    main()
