from lowpass_filter import *
from audio_wav_test import *
import matplotlib.pyplot as plt
from numpy import mean, std


N_FRAMES = 44100*10
DOWNSIZE_FACTOR = 44
TEMPO_MIN = 72
TEMPO_MAX = 168
integer_wav, base_framerate = read_wav(num_frames = None, num_channels = 1, start_pos = 69000)
framerate = base_framerate / DOWNSIZE_FACTOR
print('NEW FRAME RATE', framerate)
reduced_int_wav = integer_wav[::DOWNSIZE_FACTOR]
filtered_wav = butter_lowpass_filter(data=reduced_int_wav, cutoff=2, fs=framerate, order=1)

standard_deviation = std(filtered_wav)
average = mean(filtered_wav)
peaks = detect_peaks(filtered_wav, min=(average + 2 * standard_deviation), dist=framerate*0.4)

distance_hist = {}

for i, peak in enumerate(peaks):
    if i == len(peaks) - 3: break

    for neighbor in range(3):
        dist = peaks[i + 1 + neighbor] - peak

        if dist in distance_hist:
            distance_hist[dist] += 1
        else:
            distance_hist[dist] = 1

tempo_hist = {}
for key in distance_hist.keys():
    tempo = 60 / (key / framerate)
    while(tempo < TEMPO_MIN):
        tempo *= 2
    while(tempo > TEMPO_MAX):
        tempo /= 2
    tempo = round(tempo)
    tempo_hist[tempo] = tempo_hist.get(tempo, 0) + distance_hist[key]

print(sorted(tempo_hist.items(), key=lambda x:x[1])[-14:][::-1])
print(len(tempo_hist.keys()))



plt.plot(reduced_int_wav, 'b-')
plt.plot(filtered_wav, 'g-')
plt.plot(peaks, [filtered_wav[peak] for peak in peaks], 'ro')
plt.title("Raw vs. Filtered Data (Low pass filter)")
plt.show()

plt.bar(tempo_hist.keys(), tempo_hist.values())
plt.show()

# print(standard_deviation, average)
# print([filtered_wav[peak] for peak in peaks][0])
# print(max([filtered_wav[peak] for peak in peaks]))
