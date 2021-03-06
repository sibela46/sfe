import dlib
import numpy as np
import glob
import cv2
import os
import sys
import random
from matplotlib import pyplot as plt

predictor_path = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
emotions = {"neutral": "01", "calm": "02", "happy": "03", "sad": "04", "angry": "05", "fearful": "06", "disgust": "07", "surprised": "08"}

def get_folder_from_actor_emotion(path, emotion, actor):
    if (not actor):
        i = random.randint(1, 25)
    else:
        i = int(actor)

    if (i < 10):
        actor_number = '0' + str(i)
    else:
        actor_number = str(i)

    actor_path = '/Actor_' + actor_number
    sub_dirs_size = len(glob.glob(os.path.join(path + actor_path, '*')))
    directory = glob.glob(os.path.join(path + actor_path, '*'))
    folder = ""

    if (emotion == None):
        folder_index = random.randint(0, sub_dirs_size-1)
        folder = directory[folder_index]
    else:
        for f in directory:
            if (f.split('-')[2] == emotions[emotion] and (emotion == 'neutral' or f.split('-')[3] == "02") and f.split('-')[5] == "02"):
                folder = f
    
    return folder

def get_random_emotion_shape(faces_folder_path, emotion, actor):
    folder = get_folder_from_actor_emotion(faces_folder_path, emotion, actor)

    frames = 30
    vecs = np.empty((frames, 136), dtype=int)

    print("Converting video frames into 2d...")
    for (i, f) in enumerate(glob.glob(os.path.join(str(folder), '*.jpg'))):
        if (i < 30):
            img = dlib.load_rgb_image(f)

            dets = detector(img)

            for k, d in enumerate(dets):
                shape = predictor(img, d)

            vec = []
            vec_out = np.empty((68, 2), dtype=int)
            for b in range(68):
                vec.append(shape.part(b).x)
                vec.append(shape.part(b).y)
                # vec_out[b, 0] = shape.part(b).x
                # vec_out[b, 1] = shape.part(b).y

            vecs[i] = vec
            # output_face_plots(vec_out, actor_path, folder, i) #Uncomment if you want to output the low dimensional frames in a folder

    return np.transpose(vecs)

def output_face_plots(vec, actor_path, folder, index):
    new_dir = "./low_dim_frames/" + actor_path + "/" + folder.split('/')[3]
    
    if (not os.path.isdir(new_dir)):
        os.makedirs(new_dir)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    x = vec[:, 0]
    y = vec[:, 1]
    ax.scatter(x, y)
    for i in range(vec.shape[0]):
        ax.annotate(str(i), (x[i], y[i]), xytext=(10,10), textcoords='offset points')
        plt.scatter(x, y, marker='x', color='red')

    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.savefig("./" + new_dir + "/" + str(index) + ".png")
    plt.clf()
