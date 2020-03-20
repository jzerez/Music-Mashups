from find_bpm import *
from audio_wav_test import *
from datetime import datetime
startTime = datetime.now()

files = [
    'Raw/Ratatat_-_Allure.wav',
    'Raw/Post_MAlone_-_Go_Flex.wav',
    'Raw/Go_Flex.wav'
]

CHANGE_BACKGROUND = False
BG_SCALE = 0.35
VOCALS_SCALE = 1 - BG_SCALE

bg_bpm = find_bpm(file=files[0])
vocals_bpm = find_bpm(file=files[1])

print('track one bpm: ', bg_bpm)
print('track two bpm: ', vocals_bpm)

if CHANGE_BACKGROUND:
    bpm_factor = vocals_bpm / bg_bpm
    file_to_change = files[0]
    base_file = files[2]
    base_scale = VOCALS_SCALE
    changed_scale = BG_SCALE
else:
    bpm_factor = bg_bpm / vocals_bpm
    file_to_change = files[2]
    base_file = files[0]
    changed_scale = VOCALS_SCALE
    base_scale = BG_SCALE

print(bpm_factor)
new_file_name = file_to_change.split('/')[-1].split('.')[0]+'_NEW_TEMPO.wav'


combine_wav(files[0], files[2], BG_SCALE, VOCALS_SCALE, 1, bpm_factor, extra_frames_factor = 2)
print("Processed files in ", datetime.now() - startTime, " ms")
