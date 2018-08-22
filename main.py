from find_bpm import *
from audio_wav_test import *

files = [
    'Raw/Ratatat_-_Seventeen_Years.wav',
    'Raw/Childish_Gambino_-_Sweatpants.wav',
    'Raw/Childish_Gambino_-_Sweatpants_Vocals_Only_Acapella.wav'
]

CHANGE_BACKGROUND = False
BG_SCALE = 0.15
VOCALS_SCALE = 0.85

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
# change_playback_speed(file_to_change, bpm_factor, new_file=new_file_name)
#
# base_frames, base_framerate = read_wav(base_file)
# base_frames = list(base_frames)
# changed_frames, changed_framerate = read_wav(new_file_name)
# changed_frames = list(changed_frames)
# print(changed_framerate)
# print(type(changed_frames))
# print(type(changed_frames[0]))
# print(len(changed_frames))
# print(changed_frames[0])
#
# first_base_peak = find_first_beat(base_frames[::44], base_framerate / 44, verbose=False)
# first_changed_peak = find_first_beat(changed_frames[:44], changed_framerate / 44,verbose=True)
#
# base_frames = [int(frame*base_scale) for frame in base_frames]
# changed_frames = [int(frame*changed_scale) for frame in changed_frames]
#
#
# # print(first_base_peak, first_changed_peak)
#
# new_frames = [x+y for x,y in zip(base_frames, changed_frames)]
#
#
# write_wav(new_frames, file='FINAL.wav')

combine_wav(files[0], files[2], BG_SCALE, VOCALS_SCALE, 1, bpm_factor, extra_frames_factor = 3)
