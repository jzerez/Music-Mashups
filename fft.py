from scipy.fftpack import fft
from audio_wav_test import *
import matplotlib.pyplot as plt
import numpy as np
import math;

pi = math.pi
highest_tempo = 250;
BPM_TO_HZ = 1/60;


[frames, Fs] = read_wav("./Raw/Loud_Pipes.wav");
N = len(frames)
freq_shift = Fs * (np.linspace(-pi/2, pi/2, N) - ((pi/N)*(N%2))) / (2*pi)

fq_frames = np.absolute(fft(frames))
print(freq_shift[np.argmax(fq_frames[int(1.5*Fs):])])
plt.plot(freq_shift, fq_frames)
plt.show()
