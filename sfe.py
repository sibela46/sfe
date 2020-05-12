import numpy as np
import argparse
from set_mrd_model import SFE_MRD
import get_low_dimension_frames as ldf

parser = argparse.ArgumentParser()

parser.add_argument("-o", "--optimize", help="optimize model", action="store_true")
parser.add_argument("-m", "--model-path", help="select a path to an optimized model")
parser.add_argument("-d", "--data-path", help="select path to the video frames data", required=True)
parser.add_argument("--actors", help="two numbers from 1-24 for which actor's videos to use")
parser.add_argument("--emotions", help="provide a list of emotions (strings separated by commas with no whitespace)")
parser.add_argument("--save", help="provide the name for the model to save it in the /models folder")
args = parser.parse_args()

if args.optimize and not args.data_path:
    print("You need to specify a path to the video frames folder")
    exit()

if not args.optimize and not args.model_path:
    print("You need to either specify that you want to optimize the model, or provide a path to an already optimized model.")
    exit()

def main():
    emotions = ["neutral", "calm", "happy", "sad", "angry", "fearful", "disgust", "surprised"]
    happyViews = np.array([]).reshape(0, 136)
    angryViews = np.array([]).reshape(0, 136)
 
    if (args.emotions and args.optimize):
        actors = [None] * (len(args.actors))
        if (args.actors):
            actors = args.actors.split(",")
            emotions = args.emotions.split(",")  
        for i in range(0, 2):
            emotions[i].replace(" ", "")
            actors[i].replace(" ", "")
            print("Chosen emotion: " + emotions[i])
            print("Chosen actor: " + actors[i])
            view = (ldf.get_random_emotion_shape(faces_folder_path=args.data_path, emotion=emotions[i], actor=actors[i]).T)
            views.append(view)
    elif (args.optimize):
        for i in range(1, 25):
            newHappy = ldf.get_random_emotion_shape(faces_folder_path=args.data_path, emotion="happy", actor=i).T
            newAngry = ldf.get_random_emotion_shape(faces_folder_path=args.data_path, emotion="angry", actor=i).T

            happyViews = np.concatenate((happyViews, newHappy), axis=0)
            angryViews = np.concatenate((angryViews, newAngry), axis=0)

    mrd = SFE_MRD(views=[happyViews, angryViews], optimize=args.optimize, model_path=args.model_path, save_model=args.save)

if __name__ == "__main__":
    main()
