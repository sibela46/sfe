import numpy as np
import argparse
from set_mrd_model import SFE_MRD
from set_bgplvm_model import SFE_BGPLVM
import get_low_dimension_frames as ldf

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data-path", help="select path to the video frames data", required=True)
parser.add_argument("-o", "--optimize", help="optimize model", action="store_true")
parser.add_argument("-m", "--model-path", help="select a path to an optimized model")
parser.add_argument("--actors", help="two numbers from 1-24 for which actor's videos to use")
parser.add_argument("--emotions", help="provide a list of emotions (strings separated by commas with no whitespace)")
parser.add_argument("--save", help="provide the name for the model to save it in the /models folder")
args = parser.parse_args()

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
        # myiter = iter(range(1, 9))
        for i in range(1, 25):
            newHappy = ldf.get_random_emotion_shape(faces_folder_path=args.data_path, emotion="happy", actor=i).T
            newAngry = ldf.get_random_emotion_shape(faces_folder_path=args.data_path, emotion="angry", actor=i).T
            happyViews = np.concatenate((happyViews, newHappy), axis=0)
            angryViews = np.concatenate((angryViews, newAngry), axis=0)
            # next(myiter, None)

    mrd = SFE_MRD(views=[happyViews, angryViews], optimize=args.optimize, model_path=args.model_path, save_model=args.save)
    # bgplvm = SFE_BGPLVM(happyViews, optimize=args.optimize, model_path=args.model_path, save_model=args.save)

# data_path = "./3d_video_frames"
# def runEmotions(emotion1, emotion2, path):
#     happyViews = np.array([]).reshape(0, 136)
#     angryViews = np.array([]).reshape(0, 136)
#     for i in range(1, 9):
#         newHappy = ldf.get_random_emotion_shape(faces_folder_path=data_path, emotion=emotion1, actor=i).T
#         newAngry = ldf.get_random_emotion_shape(faces_folder_path=data_path, emotion=emotion2, actor=i).T
#         happyViews = np.concatenate((happyViews, newHappy), axis=0)
#         angryViews = np.concatenate((angryViews, newAngry), axis=0)
    
#     mrd = SFE_MRD(views=[happyViews, angryViews], optimize=True, save_model=path)

# runEmotions("neutral", "calm", "mrd_neutral_calm")
# print("Finished calm")
# runEmotions("neutral", "sad", "mrd_neutral_sad")
# print("Finished sad")
# runEmotions("neutral", "happy", "mrd_neutral_happy")
# print("Finished happy")
# runEmotions("neutral", "angry", "mrd_neutral_angry")
# print("Finished angry")
# runEmotions("neutral", "surprised", "mrd_neutral_surprised")
# print("Finished surprised")
# runEmotions("neutral", "disgust", "mrd_neutral_disgust")
# print("Finished disgust")
# runEmotions("neutral", "fearful", "mrd_neutral_fearful")
# print("Finished fearful")
if __name__ == "__main__":
    main()

