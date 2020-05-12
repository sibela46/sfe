import dlib
import numpy as np
import glob
import os
import sys
import random
from matplotlib import pyplot as plt

predictor_path = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
emotions = {"neutral": "01", "calm": "02", "happy": "03", "sad": "04", "angry": "05", "fearful": "06", "disgust": "07", "surprised": "08"}

def get_random_emotion_shape(faces_folder_path, emotion, actor):
    if (not actor):
        i = random.randint(1, 25)
    else:
        i = int(actor)

    if (i < 10):
        actor_number = '0' + str(i)
    else:
        actor_number = str(i)

    print(emotion)
    actor_path = '/Actor_' + actor_number
    sub_dirs_size = len(glob.glob(os.path.join(faces_folder_path + actor_path, '*')))
    directory = glob.glob(os.path.join(faces_folder_path + actor_path, '*'))
    folder = ""

    if (emotion == None):
        folder_index = random.randint(0, sub_dirs_size-1)
        folder = directory[folder_index]
    else:
        for f in directory:
            if (f.split('-')[2] == emotions[emotion] and (emotion == 'neutral' or f.split('-')[3] == "02") and f.split('-')[5] == "02"):
                folder = f
    
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
    plt.show()
    # plt.scatter(vec[:, 0], vec[:, 1])
    # plt.axis('off')
    # plt.show()
    # plt.savefig("./" + new_dir + "/" + str(index) + ".png")
    # plt.clf()


# get_random_emotion_shape("./3d_video_frames", "neutral", 1)
#     get_random_emotion_shape("./3d_video_frames", "calm", i)
#     get_random_emotion_shape("./3d_video_frames", "happy", i)
#     get_random_emotion_shape("./3d_video_frames", "sad", i)
#     get_random_emotion_shape("./3d_video_frames", "angry", i)
#     get_random_emotion_shape("./3d_video_frames", "fearful", i)
#     get_random_emotion_shape("./3d_video_frames", "disgust", i)
#     get_random_emotion_shape("./3d_video_frames", "surprised", i)

# f = "./3d_video_frames/Actor_01/02-01-03-02-02-02-01/image36.jpg"
# img = dlib.load_rgb_image(f)

# dets = detector(img)

# for k, d in enumerate(dets):
#     shape = predictor(img, d)

# vec_out = np.empty((68, 2), dtype=int)
# for b in range(68):
#     vec_out[b, 0] = shape.part(b).x
#     vec_out[b, 1] = shape.part(b).y

# fig = plt.figure()
# ax = fig.add_subplot(111)
# x = vec_out[:, 0]
# y = vec_out[:, 1]
# ax.scatter(x, y, c='black')
# plt.axis('off')
# plt.gca().invert_xaxis()
# plt.gca().invert_yaxis()
# plt.savefig("actor01_happy_36", bbox_inches='tight')
# plt.show()
