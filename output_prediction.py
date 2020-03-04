import numpy as np
import pickle
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

model = pickle.load(open("mrd_happy_angry_linear", "rb"))

model.X.mean[:, 4] += 10
newX = model.X.mean
newY = model.predict(newX, Yindex=0)
frames = newY[0].shape[0]
plt.xkcd()
for i in range(frames):
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111)
    frameCoords = newY[0][i].reshape(68,2)
    ax.scatter(frameCoords[:, 0], frameCoords[:, 1], marker='o', color='black')
    plt.gca().invert_yaxis()
    fig.savefig("./more_happy/" + str(i) + ".png")