# Video processing

This directory contains the scripts used for video processing in the Smart Vertigo Dataset.

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

* `x` = horizontal coordinate of the left edge of the crop
* `y` = vertical coordinate of the upper edge of the crop
* `w` = width of the crop in pixels
* `h` = height of the crop in pixels

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

The video is read sequentially using OpenCV. Each frame is converted from OpenCV's BGR colour representation to RGB and saved as a PNG image using 
Pillow.

## Metadata, summary counts and quality control

No custom code was used to generate the metadata tables, summary counts, or quality-control results.

The script extracts the available frames sequentially without intentionally changing their spatial dimensions.
