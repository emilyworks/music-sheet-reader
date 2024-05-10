# AI Music Sheet Reader
We aim to leverage computer vision techniques to create music visual aids for piano players. At inference time, the input is a sheet music document and the output is a generated video (or series of images) demonstrating how to play the sheet music. An example of a similar output can be found at the following link: https://www.youtube.com/watch?v=aeEmGvm7kDk

The motivation behind this project is to address challenges faced by musicians at all levels in reading sheet music. By automating the process of sheet music recognition and offering visual aids, the project aims to make learning music more accessible to those who have not received classical training and/or are unable to read sheet music. Furthermore, the initial interest in the topic of the project stems from all three group members having played instruments and struggled with reading sheet music.

[**Presentation Slides**](https://docs.google.com/presentation/d/1fx8u-OTpy8S-db-NQWF3gvC4ufHszsWol67fGmVnLKA/edit#slide=id.g2cdcb7191f5_0_10)

**Final Report**

## Repo Overview

### BLIP Fine-tuning/Training

We finetuned BLIP, a generative image-to-text model from SalesForce, to output bekrn-notated text given images of musical scores as input. The model was evaluated on its WER score. 

The relevant files for this approach of the project is as follows:
- ```finetuning_blip.ipynb``` contains the end-to-end code necessary for producing the finetuned BLIP. It includes data processing code and model run and eval code. Please note that the notebook output from the training loop cell does not show the full training run (i.e. we trained for more than 2% of the training dataset); for a fuller output, see below.
- ```sample_test_run_prints.txt``` contains a fuller example of a running output from the training loop run. (There were multiple training runs primarily because colab sessions used for training timed out before training could completely finish. Model weights were reloaded from a checkpoint and training was resumed thereafter).
- ```sample_test_run_prints.txt``` contains an example running log from one of the test loops (There were multiple test loops due to session time-outs and other misc. like hyperparameter changes for training)