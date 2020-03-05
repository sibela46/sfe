import numpy as np
import argparse
from set_model import SFE
import get_low_dimension_frames as ldf

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data-path", help="select path to the video frames data", required=True)
parser.add_argument("-o", "--optimize", help="optimize model", action="store_true")
parser.add_argument("-m", "--model-path", help="select a path to an optimized model")
parser.add_argument("--actor", help="number from 1-24 for which actor's videos to use")
parser.add_argument("--emotion1", help="provide an emotion for the view")
parser.add_argument("--emotion2", help="provide a second emotion for a view")
args = parser.parse_args()

if not args.optimize and not args.model_path:
    print("You need to either specify that you want to optimize the model, or provide a path to an already optimized model.")
    exit()

def main():
    view_1 = ldf.get_random_emotion_shape(faces_folder_path=args.data_path, emotion=args.emotion1, actor=args.actor).T
    view_2 = ldf.get_random_emotion_shape(faces_folder_path=args.data_path, emotion=args.emotion2, actor=args.actor).T
    mrd = SFE(views=[view_1, view_2], optimize=args.optimize, model_path=args.model_path)
    
if __name__ == "__main__":
    main()