import numpy as np
import os
import pickle
import GPy
from GPy import kern
from GPy.models import MRD
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

class SFE_MRD:
    def __init__(self, views, optimize=True, model_path=None, kernel=None, lengthscale=None, num_inducing=20, save_model=None):
        self.views = views
        self.model_path = model_path
        self.kernel = kernel.lower()
        self.lengthscale = lengthscale
        self.num_inducing = int(num_inducing)

        if (not optimize): # In this case a path to a model was selected, so load the model
            self.model = pickle.load(open(self.model_path, "rb"))
            self.model.plot_scales()
            plt.show()
            self.getDiffInY(0)
            self.plot_latent()
            # self.outputAltered(0)
            self.visualize(2)
        else: # In this case begin training, and plot the results after that
            self.optimize(views, save_model=save_model)
            self.model.plot_scales()
            plt.show()
            self.getDiffInY(0)
            self.plot_latent()
            self.visualize(2)

    # Defines the MRD model with the chosen parameters and begins optimising it
    def optimize(self, views, latent_dims=7, messages=True, max_iters=8e3, save_model=False):
        if (self.kernel):
            if (self.kernel == 'rbf'):
                print("Chosen kernel: RBF")
                print("Chosen lengthscale: " + self.lengthscale)
                k = kern.RBF(latent_dims, ARD=True, lengthscale=self.lengthscale) + kern.White(latent_dims, variance=1e-4) + GPy.kern.Bias(latent_dims)
            elif (self.kernel == 'linear'):
                print("Chosen kernel: Linear")
                k = kern.Linear(latent_dims, ARD=True) + kern.White(latent_dims, variance=1e-4) + GPy.kern.Bias(latent_dims)
        else:
            print("No kernel or chosen - using RBF with lengthscale 10...")
            k = kern.RBF(latent_dims, ARD=True, lengthscale=10) + kern.White(latent_dims, variance=1e-4) + GPy.kern.Bias(latent_dims)
    
        print("Number of inducing inputs: " + str(self.num_inducing))
        m = MRD(views, input_dim=latent_dims, num_inducing=self.num_inducing, kernel=k, normalizer=False)
        print("Optimizing Model...")
        m.optimize(messages=True, max_iters=8e3)
        
        if (save_model):
            pickle.dump(m, open(save_model, "wb"), protocol=2)
        
        self.model = m

    # Generates two predictions from two latent spaces, finds the differences in coordinates of the
    # generated outputs and saves them in a .txt file which is then used by the C++ plug-in
    def getDiffInY(self, view):
        # Get the most important dimension for the particular view
        vip_dim = self.get_most_important_dim(view, 15)
        
        # Define a matrix with all zeros except for the vip dimension
        to_add_neutral = np.zeros(self.model.X.mean.shape)
        # Fill the vip dimension with some value to add to the latent space mean
        to_add_neutral[:, vip_dim] += 0

        # Generate a prediction that would serve as a base
        neutralX = self.model.X.mean + to_add_neutral
        oldY = self.model.predict(neutralX, Yindex=view)

        # Define another matrix with all zeros except for the vip dimension
        to_add_emotion = np.zeros(self.model.X.mean.shape)
        # Add onto that dimension in order to alter the latent space mean
        to_add_emotion[:, vip_dim] += 3

        # Generate a modified expression with the new mean
        happyX = self.model.X.mean + to_add_emotion
        newY = self.model.predict(happyX, Yindex=view)

        # Reshape the resulting predictions in order to output their coordinates
        oldFrameCoords = oldY[0][15].reshape(68,2)
        newFrameCoords = newY[0][15].reshape(68,2)

        # Find the difference in coordinates
        diff = (oldFrameCoords - newFrameCoords)

        # Save it in a text file
        with open("output.txt", "w") as txt_file:
            for i in diff:
                txt_file.write(str(i[0]) + ", " + str(i[1]) + ", ")

    # Plots the latent space manifold
    def plot_latent(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.model.X.mean)
        plt.show()

    # Displays the interactive window used to alter the mean, view and frame values and observe the new outputs
    def visualize(self, views):
        sharedDims, privateDims = self.model.factorize_space()
        newX = self.model.X.mean
        newY = self.model.predict(newX, Yindex=0)
        frames = newY[0].shape[0]

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

    # Finds the dimension with the highest ARD weight, given a particular view
    def get_most_important_dim(self, view, frame):
        sharedDims, privateDims = self.model.factorize_space()
        viewDims = privateDims[int(view)]
        # The ARD weight is expressed through the variance of the latent space
        frameVariances = self.model.X.variance[int(frame-1), :]
        maxDim = 0
        maxDimIndex = -1
        for dim in viewDims:
            if (frameVariances[dim] > maxDim):
                maxDim = frameVariances[dim]
                maxDimIndex = dim

        return maxDimIndex

    # Used to output data for testing the CNN
    def outputAltered(self, view):
        # What comes after the "/" needs to be the emotion identifier, so that it can
        # be correctly read by the CNN
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
