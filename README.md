# Semantic Feature Extraction (SFE)

This source code is part of my dissertation in the University of Bristol. It involves using the Manifold Relevance Determination (MRD) model [Damianou et al., 2012](https://icml.cc/2012/papers/94.pdf) to extract semantics out of facial expressions and use the learnt information in Autodesk Maya so that a character's expression could be changed very easily.

I am using The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS) to train the model which can be downloaded from [here.](https://zenodo.org/record/1188976)

## Run Trained Models

This repository contains three trained models - two which are able to extract emotion and one which can deal with gender identities.

### Linear Emotion Model

This model has been trained with videos of 8 actors speaking angrily and happily, and with a linear kernel. To run an interactive window and test this model, just simply write:

```bash
python sfe.py -m ./models/mrd_happy_angry_linear
```

in the repository's main directory. You will have to install the GPy package (I've found that only python version 2 works with it)

### RBF Emotion Model

This model has been trained with the final model parameters as outlined in the dissertation - an RBF kernel, 30 inducing inputs, lengthscale of 10, 'concat' initialisation of the latent space and videos of all 24 actors speaking both angrily and happily. Again, just write:

```bash
python sfe.py -m ./models/mrd_happy_angry_all_rbf_concat_ind30_len10
```

in the source directory in order to run the model.

### Gender Identity Model

This model has been trained with videos of all 24 actors - 12 males and 12 females, saying the same sentence in a neutral expression. To run:

```bash
python sfe.py -m ./models/mrd_man_woman_all
```

## Train a new model

### Convert videos into frames
In order to train a new model, you first need to download the data set from this [link](https://zenodo.org/record/1188976). After which you can run the *get_frames_from_video.py* script to convert the video into frames like so:

```bash
python get_grames_from_video.py [path-to-data]
```

which will output the data into frames and save it in a folder "3d_video_frames".

### Optimise the model
You can now execute the *sfe.py* script with the arguments "-o" and "-d [path-to-data]" to optimise the model with the parameters of your choice. For example if you would like to train the model with an RBF kernel, a lengtscale of 10, 20 inducing inputs, using videos of 8 actors and the emotions calm and sad, run:

```bash
python get_grames_from_video.py -o -d "./3d_video_frames" --emotions happy,sad --actors 8 --kernel rbf --lengthscale 10 --inducing_inputs 20
```

## Running the plug-in
Download the 3D model Louise from [here](https://www.eisko.com/louise/virtual-model#download-louise) and open the scene *Eisko_Head_Rig_Datapack_VFX\Maya_Scene\Louise_Rig_VFX*. Upload the ChangeExpression.mll file into Autodesk Maya using the Plug-in Manager. In the Script Editor, type in:

```bash
changeExpression
```

to run the command which will turn the woman's expression into a happy one.

## Running the Emotion Detection Neural Network
To train the neural network, simply run:

```bash
python emotion_detection_cnn.py
```

which will create its own training data from the low-dimensional representations of the video frames (located in the low_dim_frames, which should have been created when training the MRD model, if not you can create it by executing the *get_low_dimension_frames.py* script)