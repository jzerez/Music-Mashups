import wave
import struct
import matplotlib.pyplot as plt

def read_wav(file='Loud_Pipes-BcoPKWzLjrE.wav', num_frames=None, start_pos=0, plot=False, verbose=False):
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
    f.setpos(start_pos)

    raw_frames = f.readframes(num_frames)

    if f.getsampwidth() == 1:
        num_samples = len(raw_frames)
        assert num_samples % 0 == 0, "Number of frames and sample width don't match"
        int_frames = struct.unpack(str(int(num_samples)) + 'b', raw_frames)
    elif f.getsampwidth() == 2:
        num_samples = len(raw_frames) / 2
        assert num_samples % 1 == 0, "Number of frames and sample width don't match"
        integer_frames = struct.unpack(str(int(num_samples)) + 'h', raw_frames)

    if plot:
        plt.plot(integer_frames)
        plt.show()
    return integer_frames

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

if __name__ == "__main__":
    res = read_wav(num_frames=44100 * 5, start_pos=69000, plot=True)
    write_wav(res, file='new.wav')
