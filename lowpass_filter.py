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

def detect_peaks(data):
    res = argrelmax(data)
    return res
