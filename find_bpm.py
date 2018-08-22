from lowpass_filter import *
from audio_wav_test import *
import matplotlib.pyplot as plt
from numpy import mean, std


def find_bpm(file, num_frames = None, downsize_factor=44, tempo_min=60,
            tempo_max=172, num_neighbors=4, filter_cutoff_hz=2,
            target_dist_secs=0.35, std_multiple=2.5, plot=False, verbose=False):

    integer_wav, base_framerate = read_wav(file=file, num_frames=num_frames, num_channels = 1, start_pos = 69000)
    framerate = base_framerate / downsize_factor
    if verbose: print('NEW FRAME RATE', framerate)
    reduced_int_wav = integer_wav[::downsize_factor]
    filtered_wav = butter_lowpass_filter(data=reduced_int_wav, cutoff=filter_cutoff_hz, fs=framerate, order=1)

    standard_deviation = std(filtered_wav)
    average = mean(filtered_wav)
    peaks = detect_peaks(filtered_wav, min=(average + std_multiple * standard_deviation), dist=framerate*target_dist_secs)

    distance_hist = {}

    for i, peak in enumerate(peaks):
        if i == len(peaks) - num_neighbors: break

        for neighbor in range(num_neighbors):
            dist = peaks[i + 1 + neighbor] - peak

            if dist in distance_hist:
                distance_hist[dist] += 1
            else:
                distance_hist[dist] = 1

    tempo_hist = {}
    for key in distance_hist.keys():
        tempo = 60 / (key / framerate)
        while(tempo < tempo_min):
            tempo *= 2
        while(tempo > tempo_max):
            tempo /= 2
        tempo = int(round(tempo))
        tempo_hist[tempo] = tempo_hist.get(tempo, 0) + distance_hist[key]

    sorted_tempo_hist = sorted(tempo_hist.items(), key=lambda x:x[1])
    if verbose: print('TOP TEMPOS: ', sorted_tempo_hist[-14:][::-1])

    if plot:
        plt.plot(reduced_int_wav, 'b-')
        plt.plot(filtered_wav, 'g-')
        plt.plot(peaks, [filtered_wav[peak] for peak in peaks], 'ro')
        plt.title("Raw vs. Filtered Data (Low pass filter)")
        plt.show()

        plt.bar(tempo_hist.keys(), tempo_hist.values())
        plt.show()
    return sorted_tempo_hist[-1][0]

def find_first_beat(integer_wav, framerate, verbose=False,
                    target_dist_secs=0.35, std_multiple=2.5, filter_cutoff_hz=2):

    filtered_wav = butter_lowpass_filter(data=integer_wav, cutoff=filter_cutoff_hz, fs=framerate, order=1)
    if verbose: print('filtered: ', filtered_wav)
    standard_deviation = std(filtered_wav)
    average = mean(filtered_wav)
    peaks = detect_peaks(filtered_wav, min=(average + std_multiple * standard_deviation), dist=framerate*target_dist_secs)
    if verbose: print(peaks)
    # return peaks[0]


if __name__ == "__main__":
    bpm = find_bpm('Raw/Childish_Gambino_-_Sweatpants.wav', plot=False)
    print(bpm)
    bpm = find_bpm('Raw/Ratatat_-_Seventeen_Years.wav', plot=False)
    print(bpm)
    frames, framerate = read_wav('Eminem_without_me_acapella_NEW_TEMPO.wav')
    # find_first_beat(frames[::44], framerate/44, verbose=True)
