import wave
import pickle
import struct
import time
import numpy as np
from scipy.fftpack import fft, fftfreq
from scipy.signal import stft, istft
from scipy.stats import mode
import matplotlib.pyplot as plt
import math
import pdb
from lowpass_filter import *
import os


class Song():
    def __init__(self, song_file):
        self.title = song_file
        # file_type = song_file[-3:]
        self.highest_tempo = 250
        self.BPM_TO_HZ = 1/60
        dir = "./Raw/"
        dirstuff = os.listdir(dir)
        if song_file + '.wav' in dirstuff:
            print("Reading Wav...")
            self.read_wav(dir + song_file + '.wav')
            self.calc_tempo()
            pickle_file = open(self.title + "txt", 'wb')
            self.remixes = set();
            pickle.dump(self.__dict__, pickle_file)
        elif song_file + ".txt" in dirstuff:
            print("Loading Pickle File...")
            f = open(dir + song_file + ".txt", 'rb')
            self.__dict__ = pickle.load(f)
        else:
            print("no file found")
            return
        self.take_stft(self)

    def read_wav(self, file):
        """
        Reads and parses through a given wav file. Populates attributes of the
        class based on the file's metadata.
        """
        f = wave.open(file, 'rb')
        print(f)

        self.num_frames = f.getnframes()
        self.num_channels = f.getnchannels()
        self.frame_rate = f.getframerate()
        print(f.getparams())
        raw_frames = f.readframes(self.num_frames)
        if f.getsampwidth() == 1:
            #If the wave file has a sample width of 1 (8bit encoding)
            num_samples = len(raw_frames)
            self.frames = struct.unpack(str(int(num_samples)) + 'b', raw_frames)
        elif f.getsampwidth() == 2:
            #If the wave file has a sample width of 2 (16bit encoding)
            num_samples = len(raw_frames) / 2
            self.frames = struct.unpack(str(int(num_samples)) + 'h', raw_frames)
        self.secs = self.num_frames / self.frame_rate;

    def calc_tempo(self):
        """
        Calculates the tempo of the song using fft
        """
        pi = math.pi

        down_frames, _ = self.downsample(self.highest_tempo * self.BPM_TO_HZ)
        N = len(down_frames)
        freq_shift = fftfreq(N, d=1/(self.highest_tempo * self.BPM_TO_HZ * 2))

        print(fft(down_frames))
        fq_frames = np.absolute(fft(down_frames))
        max_amp = max(fq_frames)
        fq_frames /= max_amp
        plt.plot(freq_shift, fq_frames)
        fq_frames = [self.low_pass(frame)+2 for frame in fq_frames]

        fqs = freq_shift[len(freq_shift)//2:]
        # plt.plot(freq_shift, fq_frames)
        # plt.show()
        self.tempo = round(abs(fqs[np.argmax(fq_frames[len(fq_frames)//2:])]) * 60)

    def low_pass(self, x):
        if x < 0.3:
            return 0
        else:
            return x
        # return 1/(1+math.e**(14*(x-0.4)));

    def downsample(self, max_freq):
        """
            Takes maximum expected frequency (HZ) as argument
            returns the downsampled time series for analysis
        """
        # Nyquist sampling frequency for highest reasonable tempo
        nyquist = max_freq * 2;

        assert nyquist < self.frame_rate
        down_sample_factor = int(self.frame_rate / nyquist)

        return [self.frames[::down_sample_factor], down_sample_factor]


    def take_stft(self, x):
        TIME_WINDOW = 0.1       # SECONDS
        HIGHTEST_NOTE = 4000    # HZ
        down_frames, down_sample_factor = self.downsample(HIGHTEST_NOTE)

        fr = self.frame_rate / down_sample_factor
        frames_per_seg = fr * TIME_WINDOW

        N = len(down_frames)
        freq_shift = fftfreq(N, d=1/(self.BPM_TO_HZ * HIGHTEST_NOTE * 2))
        f, t, Zxx = stft(down_frames, fs = fr, nperseg = int(frames_per_seg))

        mag = np.abs(Zxx)
        mag_avg = mag.mean()
        mag_std = mag.std()
        all_notes = [None] * t.size
        stds = [None] * t.size
        total_mags = [None] * t.size
        note_dict = {}
        plt.figure()
        for frame in range(t.size):
            mags = mag[:, frame]
            total_mags[frame] = np.sum(mags)
            stds[frame] = mags.std()

            peak_freqs = f[np.where(mags > mag_avg + 6 * mag_std)]
            peak_freqs = peak_freqs[np.where(freqs > 200)]
            np.sort(peak_freqs)
            all_notes[frame] = self.calc_note(peak_freqs[:5].tolist())
            for note in all_notes[frame]:
                if note in note_dict:
                    note_dict[note] += 1
                else:
                    note_dict[note] = 1
            plt.scatter(t[frame] * np.ones(np.shape(peak_freqs[:5])), all_notes[frame], 9)
        plt.figure()
        sorted_note_hist = sorted(note_dict.items(), key=lambda x:x[1])
        print('most common notes: ')
        print(sorted_note_hist[-1][0])
        print(sorted_note_hist[-2][0])
        print(sorted_note_hist[-3][0])
        print(sorted_note_hist[-4][0])
        print(sorted_note_hist[-5][0])
        lp = butter_lowpass_filter(data=stds, cutoff=0.3, fs=1/t[1]-t[0], order=6)
        plt.plot(t,lp)
        plt.scatter(t[detect_peaks(lp)], lp[detect_peaks(lp)])
        plt.figure()

        print("num peaks: ", len(detect_peaks(lp)))
        #
        # plt.figure()
        # plt.plot(total_mags)
        # plt.figure()
        print(mode([f for array in all_notes for f in array]))
        # plt.pcolormesh(t, f[:300], mag[:300, :], vmin=0, vmax=np.amax(mag))
        # for i, frame in enumerate(all_notes):
        #     plt.scatter(t[i] * np.ones(np.shape(frame)), frame, s=9, c="red")

        plt.show()

    def calc_note(self, freq):
        ROOT_FREQ = np.log2(440)        # HZ
        ROOT_NUM = 49                   # A440 is the 49th note on the piano
        dist = np.log2(freq) - ROOT_FREQ
        num_semitones = dist * 12
        return np.round(num_semitones + ROOT_NUM)



class PhaseVocoder():
    def __init__(self, song, speed_factor):
        self.speed_factor = speed_factor
        self.song = song
    def timeshift(self):
        """
        * Use speed factor and nyquist freq to determine how big each "short time" frame should be
        * assume 30% overlap between subsequent frames?
        * take fourier transform,
        """

if __name__ == "__main__":
    a = Song("Lex")
