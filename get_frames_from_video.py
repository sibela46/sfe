import sys
import os
import glob
import cv2

def getFrame(vidcap, sec, new_dir):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite(new_dir + "/image"+str(count)+".jpg", image) # save frame as JPG file
    return hasFrames

if len(sys.argv) != 2:
    print("You need to specify the path to the videos")
    exit()

videos_folder_path = sys.argv[1]

for i in range(1, 25):
    number = ' '
    if (i < 10):
        number = '0' + str(i)
    else:
        number = str(i)

    actor_path = '/Actor_' + number

    for f in glob.glob(os.path.join(videos_folder_path + actor_path, "02-01*.mp4")):
        new_dir = "." + actor_path + "/" + f.split('/')[3].split('.')[0]
        os.makedirs(new_dir)
        vidcap = cv2.VideoCapture(f)
        sec = 0
        frameRate = 0.1 #It will capture image in each 0.1 second
        count = 1
        success = getFrame(vidcap, sec, new_dir)
        while success:
            count = count + 1
            sec = sec + frameRate
            sec = round(sec, 2)
            success = getFrame(vidcap, sec, new_dir)
