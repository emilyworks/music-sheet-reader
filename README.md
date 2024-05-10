# AI Music Sheet Reader
We aim to leverage computer vision techniques to create music visual aids for piano players. At inference time, the input is a sheet music document and the output is a generated video (or series of images) demonstrating how to play the sheet music. An example of a similar output can be found at the following link: https://www.youtube.com/watch?v=aeEmGvm7kDk

The motivation behind this project is to address challenges faced by musicians at all levels in reading sheet music. By automating the process of sheet music recognition and offering visual aids, the project aims to make learning music more accessible to those who have not received classical training and/or are unable to read sheet music. Furthermore, the initial interest in the topic of the project stems from all three group members having played instruments and struggled with reading sheet music.

[**Presentation Slides**](https://docs.google.com/presentation/d/1fx8u-OTpy8S-db-NQWF3gvC4ufHszsWol67fGmVnLKA/edit#slide=id.g2cdcb7191f5_0_10)

[**Final Report**](https://drive.google.com/file/d/1w9hJSdY4xIqgYqVaoZkT2ClwYpKENwt6/view?usp=drive_link)

## Repo Overview

### BLIP Fine-tuning/Training

We finetuned BLIP, a generative image-to-text model from SalesForce, to output bekrn-notated text given images of musical scores as input. The model was evaluated on its WER score. 

The relevant files for this approach of the project is as follows:
- ```finetuning_blip.ipynb``` contains the end-to-end code necessary for producing the finetuned BLIP. It includes data processing code and model run and eval code. Please note that the notebook output from the training loop cell does not show the full training run (i.e. we trained for more than 2% of the training dataset); for a fuller output, see below.
- ```sample_test_run_prints.txt``` contains a fuller example of a running output from the training loop run. (There were multiple training runs primarily because colab sessions used for training timed out before training could completely finish. Model weights were reloaded from a checkpoint and training was resumed thereafter).
- ```sample_test_run_prints.txt``` contains an example running log from one of the test loops (There were multiple test loops due to session time-outs and other misc. like hyperparameter changes for training)

### Custom Model Architecture

As our second approach to OMR, we built a custom model that employs, under-the-hood, a DenseNet image encoder, GRU blocks, and multi-headed attention. Details on the exact architecture, its construction, as well as model performance can be found in the ```custom_music_model.ipynb```

### Visual/Audio Generation

Model outputs will need to transformed into a video that both plays and visualizes the appropriate notes in the proper sequence. The code for doing so can be found in the folder ```piano_vis```.
A sample output and script can be found in `piano_vis/sample`

```python
import piano_vis.keyboard
```
#### Dependencies
ffmpeg-python – Information on this package can be found at https://github.com/kkroening/ffmpeg-python  
pyfluidsynth – Information on this package can be found at https://github.com/nwhitehead/pyfluidsynth  
pillow  
numpy

#### Basic Usage

##### Creating a Keyboard
```python
keyboard = Keyboard(synth)
```
`synth` should be an active fluidsynth object. To work with the mp4 export, this should use `fs.start(driver="file")`  
Note: All testing was done using the GeneralUser soundfont from https://schristiancollins.com/generaluser.php, but any other soundfont should work.

##### Creating a note
To start playing notes, we must first create note objects. The note object is created through the constructer
```python
note = Note(midinum, start_time, duration)
```
Midinum represents the pitch of the note and corresponds to the midi number found here: https://en.wikipedia.org/wiki/Piano_key_frequencies.  
start_time represents when note key is pressed down. Start time begins at 0 and each increment corresponds to 1 second. Floats and integers are accepted.  
duration represents how long a key is pressed for. Each increment corresponds to 1 second of holding down the note. Floats and integers are accepted.  

##### Playing a note
Once you have a keyboard and note, you can begin playing notes. To play a note, use `keyboard.add_note(note)` function.  

Example:
```python
keyboard.add_note(Note(52, 0, 1))
```

##### Generating an output

Once notes have been added, we can generate a video output. Use the `keyboard.generate_mp4(frame_duration, outfile)` function.  

frame duration corresponds to `1/frames_per_second` in the output video. This frame rate also affects the frequency of checks in the audio generation, so this should be at least 1 frame per note/second. For example, if using eigth notes, you should have at least frames per second (`frame_duration = 0.5`).  
Outfile corresponds to the path in which to write the output file. 

Example usage:
```python
keyboard.generate_mp4(0.125, "movie.mp4")
```
