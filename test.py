
for i, index in enumerate(raw_peaks):
    while (i + 1 < len(raw_peaks)) and ((raw_peaks[i + 1] - index) < 10):
        del raw_peaks[i + 1]
