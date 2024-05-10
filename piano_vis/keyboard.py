import time

import ffmpeg
import fluidsynth
import numpy as np
from PIL import Image

from get_keys import highlight_key, keys

fs = fluidsynth.Synth()
fs.start(driver="file")  # use DirectSound driver

sfid = fs.sfload("gs.sf2")  # replace path as needed
fs.program_select(0, sfid, 0, 0)


class Note:
    def __init__(self, midinum, start_time, duration):
        self.midinum = midinum
        self.start_time = start_time
        self.duration = duration
        self.end_time = start_time + duration
        self.time_remaining = duration


class Keyboard:
    def __init__(self, im, keys, synth):
        self.base_im = im
        self.keys = keys
        self.synth = synth
        self.to_play = {}
        self.images = {}
        self.active_notes = []

    def add_note(self, note):
        if note.start_time in self.to_play:
            self.to_play[note.start_time].append(note)
        else:
            self.to_play[note.start_time] = [note]

    def render_frames(self, frame_duration):
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
        self.render_frames(frame_duration)
        self.generate_audio(frame_duration)
        input_audio = ffmpeg.input("fluidsynth.wav")
        input_video = ffmpeg.input(
            "frames/*.png", pattern_type="glob", framerate=1 / frame_duration
        )
        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(outfile).run()

    def _get_last_note(self):
        end_time = 0
        for frame in self.to_play:
            for note in self.to_play[frame]:
                key_end = note.start_time + note.duration
                if key_end > end_time:
                    end_time = key_end
        return end_time


im = Image.open("images/keyboard_base1.png")
im.convert("RGB")
im = np.array(im)
keyboard = Keyboard(im, keys, fs)
keyboard.add_note(Note(52, 0, 1))
keyboard.add_note(Note(50, 1, 1))
keyboard.add_note(Note(48, 2, 1))
keyboard.add_note(Note(50, 3, 1))
keyboard.add_note(Note(52, 4, 1))
keyboard.add_note(Note(52, 5, 1))
keyboard.add_note(Note(52, 6, 1))
keyboard.generate_mp4(0.125, "movie.mp4")
# keyboard.render_frames(0.125)
# keyboard.generate_audio(0.125)
fs.delete()
