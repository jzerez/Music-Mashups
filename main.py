from lowpass_filter import *
from audio_wav_test import *
import matplotlib.pyplot as plt
from numpy import mean, std

N_FRAMES = 44100*10
DOWNSIZE_FACTOR = 44
integer_wav, base_framerate = read_wav(num_frames = N_FRAMES, num_channels = 1, start_pos = 69000)
framerate = base_framerate / DOWNSIZE_FACTOR
print(framerate)
reduced_int_wav = integer_wav[::DOWNSIZE_FACTOR]
filtered_wav = butter_lowpass_filter(data=reduced_int_wav, cutoff=2, fs=framerate, order=2)

standard_deviation = std(filtered_wav)
average = mean(filtered_wav)
peaks = detect_peaks(filtered_wav)[0]

print(peaks)
distance_hist = {}

for i, peak in enumerate(peaks):
    if i == len(peaks) - 1: break

    dist = peaks[i + 1] - peak

    if dist in distance_hist:
        distance_hist[dist] += 1
    else:
        distance_hist[dist] = 1

tempo_hist = {}
for key in distance_hist.keys():
    tempo = 60 / (key / framerate)
    tempo_hist[tempo] = distance_hist[key]

print(sorted(tempo_hist.items(), key=lambda x:x[1])[-14:])



plt.plot(reduced_int_wav, 'b-')
plt.plot(filtered_wav, 'g-')
plt.plot(peaks, [filtered_wav[peak] for peak in peaks], 'ro')
plt.title("Raw vs. Filtered Data (Low pass filter)")
plt.show()

print(standard_deviation, average)
