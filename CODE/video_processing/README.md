# Video processing

This directory contains the scripts used for video processing and video-level quality control in the Smart Vertigo Dataset.

## Spatial cropping: 320 × 320 and 960 × 320

The script `spatial_crop_320x320.py` was used to extract rectangular regions of interest (ROIs) from the source videos and generate the 320 × 320 and 960 × 320 pixel outputs.

The same spatial-cropping procedure was used for both output sizes. The output dimensions were controlled by the `w` and `h` parameters, while the `x` and `y` coordinates were adjusted manually for each video according to the position of the region of interest.

The script performs spatial cropping only and does not resize the selected region.

### Software and dependencies

The script was run using:

- Python 3.13.3
- OpenCV (`opencv-python`) 4.11.0.86
- NumPy 2.2.5
- FFmpeg 7.1.1

The Python standard libraries `os` and `subprocess` are used for file handling and execution of FFmpeg.

### Input and output

**Input:** MP4 video file.

**Output:** MP4 video containing either a 320 × 320 or 960 × 320 pixel crop of the selected region of interest.

The script preserves the frame rate reported by the source video. No spatial resizing is applied.

The crop location is manually specified for each video using `x` and `y` coordinates, while the output dimensions are defined by `w` and `h`.

### Cropping parameters and coordinate convention

The crop location was selected manually for each video according to the position of the eye within the source frame.

The crop is defined as:

```python
cropped = frame[y:y+h, x:x+w]
```

where:

- `x` = horizontal coordinate of the left edge of the crop
- `y` = vertical coordinate of the upper edge of the crop
- `w` = width of the crop in pixels
- `h` = height of the crop in pixels

The coordinate origin `(0, 0)` is the upper-left corner of the source frame. The `x` coordinate increases from left to right and the `y` coordinate increases from top to bottom.

For the 320 × 320 outputs:

```python
w = 320
h = 320
```

For the 960 × 320 outputs:

```python
w = 960
h = 320
```

The `x` and `y` values were adjusted manually for individual videos to position the ROI over the eye.

### Frame rate, orientation and encoding

The source video frame rate is obtained using:

```python
fps = cap.get(cv2.CAP_PROP_FPS)
```

This frame rate is passed to the output video writer; the script does not intentionally resample the frame rate.

By default, the cropped frames are not rotated. The script includes an optional 180° rotation:

```python
# cropped = np.rot90(np.rot90(cropped))
```

This operation is disabled unless explicitly uncommented.

The cropped video is initially written as a temporary AVI file using the XVID codec. FFmpeg is then used to convert the temporary file to MP4, after which the temporary AVI file is deleted.

### Parameters specified before processing

Before processing each video, the participant, video name, and crop location were specified manually in the script.

The output dimensions were set to either 320 × 320 or 960 × 320 pixels by modifying the `w` and `h` parameters. The `x` and `y` coordinates were adjusted manually for each video to position the crop around the eye.

Therefore, the crop coordinates shown in `spatial_crop_320x320.py` are an example from one video and were not used for all videos.

## Video frame extraction

The script `extract_video_frames.py` was used to extract individual frames from processed video files.

### Input and output

**Input:** MP4 video file.

**Output:** Individual video frames saved sequentially as PNG images.

Frames are numbered using five-digit sequential filenames, starting from `00000.png` (e.g., `00000.png`, `00001.png`, `00002.png`).

### Software and dependencies

The script was run using:

- Python 3.13.3
- OpenCV (`opencv-python`) 4.11.0.86
- Pillow 11.2.1

The Python standard library `os` is used for directory and file handling.

### Frame extraction

The video is read sequentially using OpenCV. Each frame is converted from OpenCV's BGR colour representation to RGB and saved as a PNG image using Pillow.

The script extracts the available frames sequentially without intentionally changing their spatial dimensions.

## Audio removal and quality-control audit

The script `audit_and_remove_video_audio.py` was used to audit processed video files for the presence of audio streams and, where required, to create audio-free versions of the videos.

### Software and dependencies

The script requires:

- Python 3
- FFmpeg, including `ffprobe`

The Python standard libraries `pathlib`, `datetime`, `subprocess`, `csv`, `os`, `shutil`, and `sys` are used for file handling, command execution, reporting, and quality-control operations.

### Audio detection and removal

The script recursively searches the specified input directory for supported video files (`.mp4`, `.mov`, `.m4v`, `.mkv`, and `.avi`) and uses `ffprobe` to determine whether one or more audio streams are present.

When audio removal is enabled, FFmpeg removes the audio stream without re-encoding the video stream (`-c copy`). This preserves the encoded video stream while generating an audio-free version of the file.

The script can also be run in audit-only mode, in which files are inspected for audio without being modified. In the repository version, audit-only mode is enabled by default and original files are not overwritten.

### Quality-control verification

When audio removal is performed, the processed file is subsequently checked to verify:

- that no audio stream remains;
- that the number of video streams is unchanged;
- that video duration remains within a predefined tolerance of the source file; and
- when enabled, that the encoded video stream is unchanged by comparing MD5 fingerprints of the video stream before and after audio removal.

Files that do not pass these checks are flagged as quality-control failures rather than being accepted as successfully processed.

### Quality-control reports

The script generates timestamped CSV reports documenting the audit and processing results.

The complete QC report records:

- video filename;
- number of audio streams before processing;
- action performed;
- number of audio streams after processing;
- video-stream integrity check;
- QC result; and
- details of any detected problems.

A second CSV report identifies files in which audio was detected.

Input, output, and report directories are configured locally by the user and are not hard-coded to dataset-specific paths in the repository version of the script.

## Metadata and summary counts

No custom code in this directory was used to generate the dataset metadata tables or descriptive summary counts reported in the manuscript. These procedures are separate from the video-processing and audio quality-control workflow described above.

## Authors and development

The video-processing scripts were developed by Elvira Cortese and Benjamin Duvieusart.
Generative AI tools were used to assist with the development and refinement of some of the scripts included in this repository. All AI-generated or AI-suggested code was reviewed, adapted, and validated by the human authors.
