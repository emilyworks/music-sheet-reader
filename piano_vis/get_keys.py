import numpy as np
from PIL import Image

from key_x_values import BLACK_KEY_X_VALUES, KEY_X_VALUES

"""Creates keys to use in keyboard object"""

KEY_BOTTOM = 256
Y_MIN = 4
BLACK_KEY_BOTTOM = 140
KEY_THRESH = 200


class Key:
    """
    Key class stores information and supports playing audio and highlighting keys
    """

    def __init__(self, midinum, color, x_values):
        self.color = color
        self.midinum = midinum
        self.x_values = x_values

    def highlight_key(self, im):
        im = highlight_key(self.midinum, im)
        # synth.noteon(0, self.midinum, 30)

    def key_on(self, synth):
        synth.noteon(0, self.midinum, 30)

    def key_off(self, synth):
        synth.noteoff(0, self.midinum)


def add_octave(midinum, idx1, idx2):
    def add_white_key(midinum, idx1):
        x_values = [
            KEY_X_VALUES[idx1],
            KEY_X_VALUES[idx1 + 1],
        ]
        key = Key(midinum, 1, x_values)
        keys[midinum] = key
        idx1 += 1
        midinum += 1
        return midinum, idx1

    def add_black_key(midinum, idx2):
        x_values = BLACK_KEY_X_VALUES[idx2]
        key = Key(midinum, 0, x_values)
        keys[midinum] = key
        idx2 += 1
        midinum += 1
        return midinum, idx2

    """Sadly this cant be a loop because it needs to 
    alternate properly through black and white keys"""
    midinum, idx1 = add_white_key(midinum, idx1)
    midinum, idx2 = add_black_key(midinum, idx2)
    midinum, idx1 = add_white_key(midinum, idx1)
    midinum, idx2 = add_black_key(midinum, idx2)
    midinum, idx1 = add_white_key(midinum, idx1)
    midinum, idx1 = add_white_key(midinum, idx1)
    midinum, idx2 = add_black_key(midinum, idx2)
    midinum, idx1 = add_white_key(midinum, idx1)
    midinum, idx2 = add_black_key(midinum, idx2)
    midinum, idx1 = add_white_key(midinum, idx1)
    midinum, idx2 = add_black_key(midinum, idx2)
    midinum, idx1 = add_white_key(midinum, idx1)

    return idx1, idx2


keys = {}
idx1 = 0
idx2 = 0
idx1, idx2 = add_octave(36, idx1, idx2)
idx1, idx2 = add_octave(48, idx1, idx2)
idx1, idx2 = add_octave(60, idx1, idx2)
idx1, idx2 = add_octave(72, idx1, idx2)


def highlight_key(idx, im):
    """Highlight a key in a given image"""
    x0 = keys[idx].x_values[0]
    x1 = keys[idx].x_values[1]
    if keys[idx].color:
        im[Y_MIN:KEY_BOTTOM, x0:x1] = np.where(
            im[Y_MIN:KEY_BOTTOM, x0:x1] > KEY_THRESH,
            [255, 0, 0],
            im[Y_MIN:KEY_BOTTOM, x0:x1],
        )
    else:
        im[Y_MIN:BLACK_KEY_BOTTOM, x0 + 1 : x1 - 1] = np.where(
            im[Y_MIN:BLACK_KEY_BOTTOM, x0 + 1 : x1 - 1] < KEY_THRESH,
            [255, 0, 0],
            im[Y_MIN:BLACK_KEY_BOTTOM, x0 + 1 : x1 - 1],
        )
    return im
