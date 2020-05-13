from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import cv2
import os
from random import shuffle
from tqdm import tqdm
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

TRAIN_DATA_DIR = "./low_dim_frames/"
TEST_DATA_DIR = "./mrd_testing/"

class CNN:
    def __init__(self):
        self.imageSize = 100
        self.lr = 1e-4
        self.model = models.Sequential()
        self.model.add(layers.Conv3D(32, (3, 3, 1), activation='relu', input_shape=(100, 100, 30, 1)))
        self.model.add(layers.MaxPooling3D((2, 2, 2)))
        self.model.add(layers.Conv3D(64, (3, 3, 1), activation='relu'))
        self.model.add(layers.MaxPooling3D((2, 2, 2)))
        self.model.add(layers.Conv3D(64, (3, 3, 1), activation='relu'))
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(64, activation='relu'))
        self.model.add(layers.Dense(4))

    def create_train_data(self):
        training_data = []

        for actor in tqdm(os.listdir(TRAIN_DATA_DIR)):
            for img in tqdm(os.listdir(TRAIN_DATA_DIR + actor)):
                label = img.split('-')[2]
                if (label == '02' or label == '03' or label == '04' or label == '05'):
                    emotion_path = TRAIN_DATA_DIR + actor + "/" + img + "/"
                    imgs = []
                    for frame in range(30):
                        path = emotion_path + str(frame) + ".png"
                        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                        img = cv2.bitwise_not(img)
                        img = cv2.resize(img, (self.imageSize, self.imageSize))
                        if (frame == 0):
                            imgs = img
                        else:
                            imgs = np.dstack((imgs, img))

                    training_data.append([np.array(imgs), np.array(int(label)-2)])
            if (actor == 'Actor_23'):
                break

        np.save('train_data.npy', training_data) 
        return training_data

    def process_test_data(self):
        testing_data = []
        
        for img in tqdm(os.listdir(TEST_DATA_DIR)):
                label = img
                if (len(label.split('-')) > 0):
                    label = '02'
            # if (label == '02' or label == '03' or label == '04' or label == '05'):
                emotion_path = TEST_DATA_DIR + img + "/"
                imgs = []
                for frame in range(1,31):
                    path = emotion_path + str(frame) + ".png"
                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    img = cv2.bitwise_not(img)
                    img = cv2.resize(img, (self.imageSize, self.imageSize)) 
                    if (frame == 1):
                        imgs = img
                    else:
                        imgs = np.dstack((imgs, img))
                testing_data.append([np.array(imgs), np.array(int(label)-2)])

        shuffle(testing_data)
        np.save('test_data.npy', testing_data)

        return testing_data

cnn = CNN()
train = cnn.create_train_data()
test = cnn.process_test_data()
# train = np.load("train_data.npy")
# test = np.load("test_data.npy")
train_data = train[4:] # leave 22 actors for training
test_data = train[:4] # leave 1 actor for validation
shuffle(train_data)

train_images = np.array([i[0]/255 for i in train_data]).reshape(-1, cnn.imageSize, cnn.imageSize, 30, 1)
train_label_arrays = [i[1] for i in train_data]
train_labels = []
for i in train_label_arrays:
    train_labels.append(int(i))

val_test_images = np.array([i[0]/255 for i in test_data]).reshape(-1, cnn.imageSize, cnn.imageSize, 30, 1)
val_test_label_arrays = [i[1] for i in test_data]
val_test_labels = []
for i in val_test_label_arrays:
    val_test_labels.append(int(i))

cnn.model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# cnn.model.load_weights('./checkpoints/batchsize_4_checkpoints/emotion-prediction-checkpoint')
history = cnn.model.fit(train_images, np.array(train_labels), batch_size=4, epochs=10, 
                    validation_data=(np.array(val_test_images), np.array(val_test_labels)))

test_images = np.array([i[0]/255 for i in test]).reshape(-1, cnn.imageSize, cnn.imageSize, 30, 1)
test_label_arrays = [i[1] for i in test]
test_labels = []
for i in test_label_arrays:
    test_labels.append(int(i))

test_loss, test_acc = cnn.model.evaluate(np.array(test_images), np.array(test_labels), verbose=2)
print(cnn.model.summary())
predictions = cnn.model.predict(test_images).argmax(axis=-1)
class_names = ['calm', 'happy', 'sad', 'angry']

for i in range(4):
    plt.figure()
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(test_images[i,:,:,16,0], cmap=plt.cm.binary, interpolation='nearest', aspect='auto')
    # The CIFAR labels happen to be arrays, 
    # which is why you need the extra index
    plt.xlabel(class_names[predictions[i]], fontsize=20)
    plt.show()

cnn.model.save_weights('./checkpoints/batchsize_4_checkpoints/emotion-prediction-checkpoint')