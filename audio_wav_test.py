import wave
import struct
import matplotlib.pyplot as plt
from numpy import mean
import time

def read_wav(file='Loud_Pipes-BcoPKWzLjrE.wav', num_frames=None, start_pos=0, num_channels = None, plot=False, verbose=False):
    """
    This function takes a wave file and returns an tuple of amplitude integers
    corresponding to the bytes written in the wave file. Returns both left and
    right channels in the same array if the wave file is in stereo.
    """
    f = wave.open(file, 'rb')
    if verbose:
        print('file params are: ', f.getparams())

    if num_frames == None:
        num_frames = f.getnframes()

    if num_channels == None:
        offset = 1
    else:
        offset = f.getnchannels() / num_channels
        assert offset % 1 == 0, "Number of channels in output is invalid"
        offset = int(offset)
    f.setpos(start_pos)

    raw_frames = f.readframes(num_frames)

    if f.getsampwidth() == 1:
        num_samples = len(raw_frames)
        assert num_samples % 1 == 0, "Number of frames and sample width don't match"
        int_frames = struct.unpack(str(int(num_samples)) + 'b', raw_frames)
    elif f.getsampwidth() == 2:
        num_samples = len(raw_frames) / 2
        assert num_samples % 1 == 0, "Number of frames and sample width don't match"
        integer_frames = struct.unpack(str(int(num_samples)) + 'h', raw_frames)

    if plot:
        plt.plot(integer_frames)
        plt.show()
    return integer_frames[::offset], f.getframerate()

def write_wav(integer_frames, num_channels=2, sample_width=2, framerate=44100, file='test.wav'):
    """
    This function takes a tuple of amplitude intitude integers, converts them
    into a byte string, and generates a wav file.
    """
    num_frames = int(len(integer_frames) / num_channels)

    if sample_width == 1:
        bytes = struct.pack(str(len(integer_frames)) + 'b', *integer_frames)
    elif sample_width == 2:
        bytes = struct.pack(str(len(integer_frames)) + 'h', *integer_frames)

    f = wave.open(file, 'wb')
    f.setnchannels(num_channels)
    f.setsampwidth(sample_width)
    f.setframerate(framerate)
    f.setnframes(num_frames)
    f.writeframes(bytes)

def change_playback_speed(file, change_factor, num_channels=2, sample_width=2, new_file='test.wav'):
    frames, framerate = read_wav(file)
    new_framerate = int(framerate*change_factor)
    write_wav(frames, num_channels=num_channels, sample_width=sample_width, framerate=new_framerate, file=new_file)

def combine_wav(file1, file2, file1_scale, file2_scale, file1_bpm_factor, file2_bpm_factor, extra_frames_factor = 1, num_channels=2, sample_width=2, framerate=44100, new_file_name='FINAL.wav'):
    if sample_width == 2:
        AMPLITUDE_MAX = 32768
    elif sample_width == 1:
        AMPLITUDE_MAX = 128
    frames1, framerate1 = read_wav(file1)
    frames2, framerate2 = read_wav(file2)
    frames1 = list(frames1)
    frames2 = list(frames2)

    # Added interpolated data points to aid the addition process
    if extra_frames_factor != 1:

        new_frames1 = []
        new_frames2 = []

        for index, frame in enumerate(frames1):
            time_between_frames = 1 / framerate1
            new_frames1 += (linear_interp_multi(frames1[index - 1], frame, time_between_frames, extra_frames_factor))
        for index, frame in enumerate(frames2):
            time_between_frames = 1 / framerate2
            new_frames2 += (linear_interp_multi(frames2[index - 1], frame, time_between_frames, extra_frames_factor))

        frames1 = new_frames1
        frames2 = new_frames2

    # base_scale1 = (AMPLITUDE_MAX * 0.5) / mean([abs(frame) for frame in frames1])
    # base_scale2 = (AMPLITUDE_MAX * 0.5) / mean([abs(frame) for frame in frames2])
    base_scale1 = 1
    base_scale2 = 1
    timestep1 = 1 / (framerate1 * file1_bpm_factor)
    timestep2 = 1 / (framerate2 * file2_bpm_factor)

    final_scale1 = base_scale1 * file1_scale
    final_scale2 = base_scale2 * file2_scale

    new_frames = []
    time = 0


    print('timestep 1: ', timestep1)
    print('timestep 2: ', timestep2)
    if timestep1 > timestep2:
        print('timestep 1 is longer')
        short_frames = frames2
        long_frames = frames1
        short_timestep = timestep2
        long_timestep = timestep1
        short_scale = final_scale2
        long_scale = final_scale1
    else:
        print('timestep 2 is longer')
        short_frames = frames1
        long_frames = frames2
        short_timestep = timestep1
        long_timestep = timestep2
        short_scale = final_scale1
        long_scale = final_scale2

    offset = 0

    for index, frame in enumerate(short_frames):
        curr_time = index * short_timestep
        long_index = int(curr_time // long_timestep)

        long_index_time = long_index * long_timestep
        assert curr_time >= long_index_time
        long_frame_mag = 0
        if long_index < len(long_frames) - 1:
            long_frame_mag = linear_interp(long_frames[long_index], long_frames[long_index + 1], long_timestep, curr_time - long_index_time)
        new_frames.append(int(long_scale * long_frame_mag + short_scale * frame));
        # if (offset + 1) * long_timestep <= index * short_timestep and offset < len(long_frames):
        #     new_frames.append(int(long_scale * long_frames[offset]) + int(short_scale * short_frames[index]))
        #     offset += 1
        # else:
        #     new_frames.append(int(short_scale * short_frames[index]))

    write_wav(new_frames, num_channels=num_channels, sample_width=sample_width, framerate=int(1/short_timestep) * extra_frames_factor, file=new_file_name)

def linear_interp(p1, p2, sample_window, time_offset):
    slope = (p2 - p1) / sample_window
    magnitude = time_offset * slope + p1
    return int(magnitude)

def linear_interp_multi(p1, p2, sample_window, splice_number):
    slope = (p2 - p1) / sample_window
    return [int(sample_window * i / splice_number * slope + p1) for i in range(splice_number)]



def frames_to_secs(framerate, num_frames):
    return num_frames / framerate;

def secs_to_frames(framerate, num_secs):
    return framerate * num_secs;

if __name__ == "__main__":
    res = read_wav(num_frames=44100 * 5, start_pos=69000, plot=True)
    write_wav(res, file='new.wav')
