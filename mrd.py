import numpy as np
import get_low_dimension_frames as ldf
import GPy
import sys
import pickle
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

plt.xkcd()

emotion1 = None
emotion2 = None
if (len(sys.argv) < 2):
    print("You need to specify path to 3d face frames")
    exit()
if (len(sys.argv) == 2):
    print("You haven't picked an emotion, so a random one will be chosen instead")
if (len(sys.argv) == 3):
    print("You can specify emotions for both views. Choosing random for second one...")
    emotion1 = sys.argv[2]
if (len(sys.argv) == 4):
    emotion1 = sys.argv[2]
    emotion2 = sys.argv[3]

# face_folder_path = sys.argv[1]

# shape1 = ldf.get_random_emotion_shape(face_folder_path, emotion1).T
# shape2 = ldf.get_random_emotion_shape(face_folder_path, emotion2).T

# difference = len(shape1) - len(shape2)
# if (difference > 0): #shape1 is bigger than shape2
#     shape1 = shape1[:-(difference)]
# elif (difference < 0):
#     shape2 = shape2[:difference]

# from GPy import kern
# from GPy.models import MRD

# num_inducing, Q = 30, 7
# Ylist = shape1, shape2

# k = kern.Linear(Q, ARD=True) + kern.White(Q, variance=1e-4) + GPy.kern.Bias(Q)
# m = MRD(Ylist, input_dim=Q, num_inducing=num_inducing, kernel=k, normalizer=False, initx='concat')

# print("Optimizing Model:")
# m.optimize(messages=True, max_iters=8e3)

# pickle.dump(m, open("mrd_sad_fearful", "wb"), protocol=2)
m = pickle.load(open("./models/mrd_happy_angry_linear", "rb"))
sharedDims, privateDims = m.factorize_space(printOut=True)

newX = m.X.mean
newY = m.predict(newX, Yindex=0)
frames = newY[0].shape[0]

i = 15
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
frameCoords = newY[0][i].reshape(68,2)
ax.scatter(frameCoords[:, 0]*(-1), frameCoords[:, 1]*(-1), marker='o', color='black')
ax.margins(x=0)
axcolor = 'lightgoldenrodyellow'
axmean = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axview = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

smean = Slider(axmean, 'Mean', -10.0, 10.0, valinit=0)
sview = Slider(axview, 'View', 0, 1, valinit=0, valstep=1)

def update(val):
    to_add = np.zeros(m.X.mean.shape)
    to_add[:, 4] += smean.val
    newX = m.X.mean + to_add
    newY = m.predict(newX, Yindex=sview.val)
    frameCoords = newY[0][i].reshape(68,2)
    ax.clear()
    ax.scatter(frameCoords[:, 0]*(-1), frameCoords[:, 1]*(-1), marker='o', color='black')
    fig.canvas.draw_idle()

smean.on_changed(update)
sview.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    smean.reset()

button.on_clicked(reset)

plt.show()