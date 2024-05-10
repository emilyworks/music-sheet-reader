import os
import time

import ffmpeg
import fluidsynth
import numpy as np
from PIL import Image

from get_keys import highlight_key, keys

default_image_path = (
    f"{os.path.dirname(os.path.abspath(__file__))}/images/keyboard_base.png"
)
default_image = np.array(Image.open(default_image_path).convert("RGB"))


class Note:
    """
    Note class for input in Keyboard object
    """

    def __init__(self, midinum, start_time, duration):
        self.midinum = midinum
        self.start_time = start_time
        self.duration = duration
        self.end_time = start_time + duration
        self.time_remaining = duration


class Keyboard:
    """
    Keyboard object for creating audio and video outputs
    Synth: fluidsynth object for audio generation
    """

    def __init__(self, synth, im=default_image, keys=keys):
        self.base_im = im
        self.keys = keys
        self.synth = synth
        self.to_play = {}
        self.images = {}
        self.active_notes = []

    def add_note(self, note):
        """
        Add a note to be played when output is generated
        """
        if note.start_time in self.to_play:
            self.to_play[note.start_time].append(note)
        else:
            self.to_play[note.start_time] = [note]

    def render_frames(self, frame_duration):
        """
        Render frame-by-frame output to be used in video generation
        frame_duration -> float: 1/frames per second of video output
        """
        frame_num = 0
        current_time = 0
        total_frames = self._get_last_note() / frame_duration
        for i in range(int(1 / frame_duration)):
            Image.fromarray(self.base_im).save(
                f"frames/frame_{str(frame_num).zfill(len(str(total_frames))+1)}.png"
            )
            frame_num += 1

        while current_time < self._get_last_note():
            im = self.base_im.copy()
            try:
                notes = self.to_play[current_time]
                for note in notes:
                    self.active_notes.append(note)

            except KeyError as e:
                pass

            for note in self.active_notes.copy():
                keys[note.midinum].highlight_key(im)
                note.time_remaining -= frame_duration
                if note.time_remaining <= 0:
                    self.active_notes.remove(note)
                    note.time_remaining = note.duration

            current_time += frame_duration
            im = Image.fromarray(im)
            im.save(
                f"frames/frame_{str(frame_num).zfill(len(str(total_frames))+1)}.png"
            )
            frame_num += 1

    def generate_audio(self, frame_duration):
        """
        Generate audio for use in vdeo output
        frame_duration -> float: 1/frames per second of video output
        """
        current_time = 0
        # time.sleep(frame_duration)
        while current_time <= self._get_last_note():
            try:
                notes = self.to_play[current_time]
                for note in notes:
                    self.active_notes.append(note)
            except KeyError as e:
                pass
            for note in self.active_notes.copy():
                if note.start_time == current_time:
                    keys[note.midinum].key_on(self.synth)
                    note.time_remaining -= frame_duration
                elif note.time_remaining <= 0:
                    print(f"{note.midinum} off: {current_time}")
                    self.active_notes.remove(note)
                    note.time_remaining = note.duration
                    keys[note.midinum].key_off(self.synth)
                else:
                    note.time_remaining -= frame_duration
            time.sleep(frame_duration)
            current_time += frame_duration

    def generate_mp4(self, frame_duration, outfile):
        """
        Generate video output for current notes
        frame_duration -> float: 1/frames per second of video output
        outfile -> string: filepath to save mp4 output
        """
        self.render_frames(frame_duration)
        self.generate_audio(frame_duration)
        input_audio = ffmpeg.input("fluidsynth.wav")
        input_video = ffmpeg.input(
            "frames/*.png", pattern_type="glob", framerate=1 / frame_duration
        )
        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(outfile).run()

    def _get_last_note(self):
        """
        Helper function to find last note in self.to_play()
        """
        end_time = 0
        for frame in self.to_play:
            for note in self.to_play[frame]:
                key_end = note.start_time + note.duration
                if key_end > end_time:
                    end_time = key_end
        return end_time
