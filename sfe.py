import numpy as np
import argparse
from set_mrd_model import SFE_MRD
import get_low_dimension_frames as ldf

parser = argparse.ArgumentParser()

parser.add_argument("-o", "--optimize", help="optimize model", action="store_true")
parser.add_argument("-m", "--model-path", help="select a path to an optimized model")
parser.add_argument("-d", "--data-path", help="select path to the video frames data")
parser.add_argument("--actors", help="a number of actors to train the model with (min 2, max 24)")
parser.add_argument("--emotions", help="provide a list of emotions (strings separated by commas with no whitespace)")
parser.add_argument("--kernel", help="the kernel to use for training the MRD model, 'rbf' or 'linear'")
parser.add_argument("--lengthscale", help="lengthscale to use if an RBF kernel was selected")
parser.add_argument("--inducing-inputs", help="the number of inducing inputs to use when optimising the variational parameters, defaults to 10")
parser.add_argument("--save", help="provide the name for the model to save it in the /models folder")
args = parser.parse_args()

if args.optimize and not args.data_path:
    print("You need to specify a path to the video frames folder")
    exit()

if args.actors and (int(args.actors) < 2 or int(args.actors) > 24):
    print("The number of actors needs to be in the range 2-24")
    exit()

if not args.optimize and not args.model_path:
    print("You need to either specify that you want to optimize the model, or provide a path to an already optimized model.")
    exit()

def main():
    emotions = ["neutral", "calm", "happy", "sad", "angry", "fearful", "disgust", "surprised"]

    if (args.optimize):
        firstViews = np.array([]).reshape(0, 136)
        secondViews = np.array([]).reshape(0, 136)
        if (args.emotions and args.actors): # User has specified a number of actors to train, train all of them
            print("Selected number of actors to train: " + args.actors)
            chosen_emotions = args.emotions.split(",")  
            actors = int(args.actors)
            print("Chosen emotions: " + chosen_emotions[0] + " and " + chosen_emotions[1])
            for i in range(actors):
                print("Chosen actor: Actor " + str(i+1))
                chosen_emotions[0].replace(" ", "")
                firstView = ldf.get_random_emotion_shape(faces_folder_path=args.data_path, emotion=chosen_emotions[0], actor=i+1).T
                chosen_emotions[1].replace(" ", "")
                secondView = ldf.get_random_emotion_shape(faces_folder_path=args.data_path, emotion=chosen_emotions[1], actor=i+1).T
                firstViews = np.concatenate((firstViews, firstView), axis=0)
                secondViews = np.concatenate((secondViews, secondView), axis=0)
            
            mrd = SFE_MRD(views=[firstViews, secondViews], optimize=args.optimize, model_path=args.model_path, kernel=args.kernel, lengthscale=args.lengthscale, num_inducing=args.inducing_inputs, save_model=args.save)

        elif (args.emotions):
            print("No actors specified, training all")
            chosen_emotions = args.emotions.split(",")
            print("Chosen emotions: " + chosen_emotions[0] + " and " + chosen_emotions[1])
            for i in range(1, 25):
                chosen_emotions[0].replace(" ", "")
                firstView = ldf.get_random_emotion_shape(faces_folder_path=args.data_path, emotion=chosen_emotions[0], actor=i+1).T
                chosen_emotions[1].replace(" ", "")
                secondView = ldf.get_random_emotion_shape(faces_folder_path=args.data_path, emotion=chosen_emotions[1], actor=i+1).T
                firstViews = np.concatenate((firstViews, firstView), axis=0)
                secondViews = np.concatenate((secondViews, secondView), axis=0)
            
            mrd = SFE_MRD(views=[firstViews, secondViews], optimize=args.optimize, model_path=args.model_path, kernel=args.kernel, lengthscale=args.lengthscale, num_inducing=args.inducing_inputs, save_model=args.save)

        else: # User has not specified anything, train all actors for happy and angry emotions
            print("No emotions or actors specified, training all actors for happy and angry.")
            happyViews = np.array([]).reshape(0, 136)
            angryViews = np.array([]).reshape(0, 136)
            for i in range(1, 25):
                newHappy = ldf.get_random_emotion_shape(faces_folder_path=args.data_path, emotion="happy", actor=i).T
                newAngry = ldf.get_random_emotion_shape(faces_folder_path=args.data_path, emotion="angry", actor=i).T

                happyViews = np.concatenate((happyViews, newHappy), axis=0)
                angryViews = np.concatenate((angryViews, newAngry), axis=0)

            mrd = SFE_MRD(views=[happyViews, angryViews], optimize=args.optimize, model_path=args.model_path, kernel=args.kernel, lengthscale=args.lengthscale, num_inducing=args.inducing_inputs, save_model=args.save)
    else: # Load an existing model
        mrd = SFE_MRD(views=[], optimize=args.optimize, model_path=args.model_path)

if __name__ == "__main__":
    main()
