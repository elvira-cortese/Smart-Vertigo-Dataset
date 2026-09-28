import cv2
import os
import numpy as np
import subprocess 


# ================== THINGS TO CHANGE ==================

patient = 'p42av'
video_name = 'gaze_down' # No file extensions
subtest_process = True

# crop values
x, y = 620, 700  # Top-left corner
w, h = 320, 320  # Width and height

# =======================================================




# Input path
if subtest_process:
    input_video = f'./With CF/{patient}/subtests/{video_name}.mp4'
else:
    input_video = f'./With CF/{patient}/{video_name}.mp4'

# output paths
video_save_dir = f'./NystagmusIndicator/CroppedVideos/WithCF/{patient}/subtests/'
temp_video_fn = f'{video_name}.avi'
output_video_fn = f'{video_name}.mp4'


# Construct the output file name by removing the '.avi' extension

# Ensure the destination directory exists
os.makedirs(video_save_dir, exist_ok=True)

# Construct the full path to the output file
output_video_path = os.path.join(video_save_dir, output_video_fn)

# Correcting the directory path issue
if not os.path.exists(video_save_dir):
    os.makedirs(video_save_dir)

#load video
cap = cv2.VideoCapture(input_video)

cnt = 0

fps = cap.get(cv2.CAP_PROP_FPS)

#output
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # MJPEG codec

# Video writer output file in .mp4 format
out = cv2.VideoWriter(f'{video_save_dir}{temp_video_fn}', fourcc, fps, (w, h)) # MP4 format

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret==True:
        #crop frame
        cropped = frame[y:y+h, x:x+w]

        # To flip 180 degrees uncomment line below
        # cropped = np.rot90(np.rot90(cropped))

        out.write(cropped)

        #to see video in live
        cv2.imshow('frame',frame)
        cv2.imshow('cropped frame',cropped)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()


# run ffmpeg to convert to mp4 in destinatio folder
commands = f'ffmpeg -i {video_save_dir}{temp_video_fn} -strict -2 {video_save_dir}{output_video_fn}'

if subprocess.run(commands).returncode == 0:
    print ("✅ FFmpeg Script Ran Successfully")
else:
    print ("⚠️ There was an error running your FFmpeg script")


# delete the avi version of the video
os.remove(f'{video_save_dir}{temp_video_fn}')
print("🗑️ Deleted temporary AVI file.")
