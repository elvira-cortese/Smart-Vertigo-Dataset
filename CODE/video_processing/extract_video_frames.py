import os
import cv2
from PIL import Image

#file paths
video_filepath = './NystagmusIndicator/CroppedVideos/WithCF/p10av/subtests/gaze_right_torsional_rightbeating_ny.mp4'
frames_save_dir = './NystagmusIndicator/CroppedVideos/WithCF/p10av/subtests/gaze_right_torsional_rightbeating_ny/'

#check if dst dir exists
if not os.path.exists(frames_save_dir):
    os.makedirs(frames_save_dir)

#load video
cap = cv2.VideoCapture(video_filepath)

# check
cap = cv2.VideoCapture(video_filepath)
if not cap.isOpened():
    print("Error: Cannot open video file. Check the path and file format.")
    exit()


cnt = 0

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret==True:

        frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame.save(f'{frames_save_dir}{cnt:05d}.png')
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

    if cnt%50 == 0:
        print(f'frame {cnt}')

    cnt += 1

cap.release()
cv2.destroyAllWindows()

