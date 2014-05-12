from scikits.audiolab import *
import midi

import dirs

def get_mid_data(filename):
    return midi.read_midifile(filename)

def get_wav_data(filename):
    f = Sndfile(filename, 'r')
    return f.read_frames(f.nframes)

def get_wav_file(filename):
    return Sndfile(filename, 'r')

def compare_channels(data):
    for i in range(len(data)):
        if (data[i][0] != data[i][1]):
            return False
    return True

def get_left(data):
    return map(lambda x: x[0], data)

def get_right(data):
    return map(lambda x: x[1], data)

''' 
fs = f.samplerate
nc = f.channels
enc = f.encoding
nframes = f.nframes
'''
