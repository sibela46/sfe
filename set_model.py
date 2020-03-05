import numpy as np
import pickle
import GPy
from GPy import kern
from GPy.models import MRD
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

class SFE:

    def __init__(self, views, optimize=True, model_path=None):
        self.views = views
        self.model_path = model_path
        
        if (not optimize):
            self.model = pickle.load(open(self.model_path, "rb"))
        else:
            self.optimize(views)

        self.visualize()

    def optimize(self, views, num_inducing=30, latent_dims=7, messages=True, max_iters=8e3, save_model=False):
        k = kern.Linear(latent_dims, ARD=True) + kern.White(latent_dims, variance=1e-4) + GPy.kern.Bias(latent_dims)
        m = MRD(views, input_dim=latent_dims, num_inducing=num_inducing, kernel=k, normalizer=False, initx='concat')
        print("Optimizing Model...")
        m.optimize(messages=True, max_iters=8e3)
        
        if (save_model):
            pickle.dump(m, open("sfe_model", "wb"), protocol=2)
        
        self.model = m

    def visualize(self):
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
        sview = Slider(axview, 'View', 0, 1, valinit=0, valstep=1)
        sframe = Slider(axframe, "Frame", 1, frames, valinit=15, valstep=1)

        frameCoords = newY[0][int(sframe.val)].reshape(68,2)
        ax.scatter(frameCoords[:, 0]*(-1), frameCoords[:, 1]*(-1), marker='o', color='black')

        def update(val):
            to_add = np.zeros(self.model.X.mean.shape)
            vip_dim = self.get_most_important_dim(sview.val, sframe.val)
            to_add[:, 4] += smean.val
            newX = self.model.X.mean + to_add
            newY = self.model.predict(newX, Yindex=sview.val)
            frameCoords = newY[0][int(sframe.val-1)].reshape(68,2)
            ax.clear()
            ax.scatter(frameCoords[:, 0]*(-1), frameCoords[:, 1]*(-1), marker='o', color='black')
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