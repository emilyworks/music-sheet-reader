import sys

import fluidsynth
import numpy as np
from PIL import Image

# setting path
sys.path.append("../")

from keyboard import Keyboard, Note

fs = fluidsynth.Synth()
fs.start(driver="file")
sfid = fs.sfload("gs.sf2")
fs.program_select(0, sfid, 0, 0)
keyboard = Keyboard(fs)
keyboard.add_note(Note(52, 0, 1))
keyboard.add_note(Note(50, 1, 1))
keyboard.add_note(Note(48, 2, 1))
keyboard.add_note(Note(50, 3, 1))
keyboard.add_note(Note(52, 4, 1))
keyboard.add_note(Note(52, 5, 1))
keyboard.add_note(Note(52, 6, 1))
keyboard.generate_mp4(0.125, "movie.mp4")
