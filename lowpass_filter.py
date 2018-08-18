import numpy as np
from scipy.signal import butter, lfilter, argrelmax

"""
TODO: Replace all of these functions from scipy with my own.

"""


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def detect_peaks(data, min=None, dist=None, verbose=False):
    raw_peaks_ind = argrelmax(data)
    raw_peaks_ind = list(map(list, raw_peaks_ind))[0]
    if min:
        if verbose: print('MIN VALUE EXSISTS: ', min)
        peak_vals = [data[index] for index in raw_peaks_ind]
        min_peaks_ind = [raw_peaks_ind[i] for i, peak in enumerate(peak_vals) if peak > min]

        raw_peaks_ind = min_peaks_ind
    if dist:
        if verbose: print('DIST VALUE EXSISTS: ', dist)
        for i, index in enumerate(raw_peaks_ind):
            while (i + 1 < len(raw_peaks_ind)) and ((raw_peaks_ind[i + 1] - index) < dist):
                del raw_peaks_ind[i + 1]
    return raw_peaks_ind
#
# def locate_peaks(data, distance, prominence):
#     res = find_peaks(data, distance=distance, prominence=prominence)
#     return res
