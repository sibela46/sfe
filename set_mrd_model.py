import numpy as np
import os
import pickle
import GPy
from GPy import kern
from GPy.models import MRD
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

class SFE_MRD:
    def __init__(self, views, optimize=True, model_path=None, save_model=None):
        self.views = views
        self.model_path = model_path
        
        if (not optimize):
            self.model = pickle.load(open(self.model_path, "rb"))
            # self.model.plot_scales()
            # plt.show()
            self.getDiffInY(1)
            # self.plot_latent()
            # self.visualize(2)
            # self.outputAltered(0)
        else:
            self.optimize(views, save_model=save_model)
            # self.getDiffInY()
            self.plot_latent()
            self.model.plot_scales()
            plt.show()
            self.visualize(len(views))


    def optimize(self, views, num_inducing=30, latent_dims=7, messages=True, max_iters=8e3, save_model=False):
        k = kern.RBF(latent_dims, ARD=True) + kern.White(latent_dims, variance=1e-4) + GPy.kern.Bias(latent_dims)
        m = MRD(views, input_dim=latent_dims, num_inducing=num_inducing, kernel=k, normalizer=False)
        print("Optimizing Model...")
        m.optimize(messages=True, max_iters=8e3)
        
        if (save_model):
            pickle.dump(m, open(save_model, "wb"), protocol=2)
        
        self.model = m

    def getDiffInY(self, view):
        to_add_neutral = np.zeros(self.model.X.mean.shape)
        to_add_emotion = np.zeros(self.model.X.mean.shape)
        vip_dim = self.get_most_important_dim(view, 15)
        to_add_neutral[:, vip_dim] -= 2
        neutralX = self.model.X.mean + to_add_neutral
        oldY = self.model.predict(neutralX, Yindex=view)
        to_add_emotion[:, vip_dim] += 3
        happyX = self.model.X.mean + to_add_emotion
        newY = self.model.predict(happyX, Yindex=view)
        oldFrameCoords = oldY[0][15].reshape(68,2)
        newFrameCoords = newY[0][15].reshape(68,2)
        diff = (oldFrameCoords - newFrameCoords)
        with open("output.txt", "w") as txt_file:
            for i in diff:
                txt_file.write(str(i[0]) + ", " + str(i[1]) + ", ") # works with any number of elements in a line

    def plot_latent(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        sharedDims, privateDims = self.model.factorize_space()
        highest_dim_0 = self.get_most_important_dim(0, 15)
        highest_dim_1 = self.get_most_important_dim(1, 15)
        # x = np.delete(self.model.X.mean,(1), axis=1)
        ax.plot(self.model.X.mean)
        # print(privateDims)
        # for privateDim in (privateDims):
        #     i = privateDim[0]
        #     j = privateDim[1]
        #     ax.scatter(self.model.X.mean[:, i], self.model.X.mean[:, j])
        plt.show()

    def visualize(self, views):
        sharedDims, privateDims = self.model.factorize_space()
        newX = self.model.X.mean
        newY = self.model.predict(newX, Yindex=0)
        frames = newY[0].shape[0]
        i = 15
        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.25, bottom=0.25)
        axcolor = 'lightgoldenrodyellow'
        axmean = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
        axview = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
        axframe = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)

        smean = Slider(axmean, 'Mean', -10.0, 10.0, valinit=0)
        sview = Slider(axview, 'View', 0, views-1, valinit=0, valstep=1)
        sframe = Slider(axframe, "Frame", 1, frames, valinit=15, valstep=1)

        frameCoords = newY[0][int(sframe.val)].reshape(68,2)
        x = frameCoords[:, 0]*(-1)
        y = frameCoords[:, 1]*(-1)
        ax.scatter(x, y, marker='o', color='black')
        for i in range(frameCoords.shape[0]):
            ax.annotate(str(i), (x[i], y[i]), xytext=(10,10), textcoords='offset points')
            plt.scatter(x, y, marker='x', color='red')
        def update(val):
            to_add = np.zeros(self.model.X.mean.shape)
            vip_dim = self.get_most_important_dim(sview.val, sframe.val)
            to_add[:, vip_dim] += smean.val
            newX = self.model.X.mean + to_add
            newY = self.model.predict(newX, Yindex=int(sview.val))
            frameCoords = newY[0][int(sframe.val-1)].reshape(68,2)
            ax.clear()
            x = frameCoords[:, 0]*(-1)
            y = frameCoords[:, 1]*(-1)
            ax.scatter(x, y, marker='o', color='black')
            # for i in range(frameCoords.shape[0]):
            #     ax.annotate(str(i), (x[i], y[i]), xytext=(10,10), textcoords='offset points')
            #     plt.scatter(x, y, marker='x', color='red')
            fig.canvas.draw_idle()

        smean.on_changed(update)
        sview.on_changed(update)
        sframe.on_changed(update)

        resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
        button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

        def reset(event):
            smean.reset()
            sview.reset()
            sframe.reset()

        button.on_clicked(reset)
        plt.show()

    def get_most_important_dim(self, view, frame):
        sharedDims, privateDims = self.model.factorize_space()
        viewDims = privateDims[int(view)]
        frameVariances = self.model.X.variance[int(frame-1), :]
        maxDim = 0
        maxDimIndex = -1
        for dim in viewDims:
            if (frameVariances[dim] > maxDim):
                maxDim = frameVariances[dim]
                maxDimIndex = dim

        return maxDimIndex

    def outputAltered(self, view):
        new_dir = "mrd_testing/05"

        if (not os.path.isdir(new_dir)):
            os.makedirs(new_dir)

        for i in range(1, 31):
            to_add = np.zeros(self.model.X.mean.shape)
            vip_dim = self.get_most_important_dim(view, i)
            to_add[:, vip_dim] -= 5
            newX = self.model.X.mean + to_add
            newY = self.model.predict(newX, Yindex=view)
            frameCoords = newY[0][i-1].reshape(68,2)
            fig = plt.figure()
            plt.axis('off')
            ax = fig.add_subplot(111)
            x = frameCoords[:, 0]*(-1)
            y = frameCoords[:, 1]*(-1)
            ax.scatter(x, y, marker='o', color='black')
            plt.savefig("./" + new_dir + "/" + str(i) + ".png")
            plt.clf()
