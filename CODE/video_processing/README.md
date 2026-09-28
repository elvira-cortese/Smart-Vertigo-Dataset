# Video processing

This directory contains the scripts used for video processing in the Smart Vertigo Dataset.

## Spatial cropping: 320 × 320

The script `spatial_crop_320x320.py` was used to extract a 320 × 320 pixel region of interest (ROI) from the source videos.

The script performs spatial cropping only and does not resize the selected region.

### Software and dependencies

The script is written in Python and uses:

- OpenCV (`cv2`) for video reading, cropping, and video writing
- NumPy (`numpy`) for optional video rotation
- FFmpeg for conversion of the temporary AVI file to MP4
- Python standard libraries `os` and `subprocess` for file handling and execution of FFmpeg

- ### Input and output

**Input:** MP4 video file.

**Output:** MP4 video containing a 320 × 320 pixel crop of the selected region of interest.

The script preserves the frame rate reported by the source video. No spatial resizing is applied.

The crop location is manually specified for each video using `x` and `y` coordinates, while the output dimensions are defined by `w` and `h`.

### Cropping parameters and coordinate convention

The crop location was selected manually for each video according to the position of the eye within the source frame.

The crop is defined as:

```python
cropped = frame[y:y+h, x:x+w]

### Frame rate, orientation and encoding

The source video frame rate is obtained using:

```python
fps = cap.get(cv2.CAP_PROP_FPS)

### Parameters specified before processing

Before processing each video, the following values were specified manually in the script:

```python
patient = 'p42av'
video_name = 'gaze_down'
subtest_process = True

x, y = 620, 700
w, h = 320, 320


### Parameters specified before processing

Before processing each video, the participant, video name, and crop location were specified manually in the script.

The output size was fixed at 320 × 320 pixels. The `x` and `y` coordinates were changed for each video to position the crop around the eye.

Therefore, the crop coordinates shown in `spatial_crop_320x320.py` are an example from one video and were not used for all videos.
