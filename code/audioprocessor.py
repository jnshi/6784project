from scikits.audiolab import *
import midi
import numpy as np
import scipy.signal

import dirs

def get_mid_data(filename):
    assert dirs.get_ext(filename) == '.mid'
    return midi.read_midifile(filename)

def get_wav_data(filename):
    assert dirs.get_ext(filename) == '.wav'
    f = Sndfile(filename, 'r')
    data = f.read_frames(f.nframes)
    samplerate = f.samplerate
    f.close()
    return (data, samplerate)

def get_wav_file(filename):
    assert dirs.get_ext(filename) == '.wav'
    return Sndfile(filename, 'r')

def compare_channels(data):
    for i in range(len(data)):
        if (data[i][0] != data[i][1]):
            return False
    return True

def get_left(data):
    return data[:,0]

def get_right(data):
    return data[:,1]

# works on single channel data only
def downsample(data, ntimes):
    return signal.decimate(data, ntimes)

def get_txt_data(filename, samplerate, numsamples):
    assert dirs.get_ext(filename) == '.txt'
    data = [[] for i in range(numsamples)]
    with open(filename, 'r') as f:
        content = f.readlines()
        for i in range(1, len(content)):
            onset, offset, midipitch = content[i].split()
            for t in range(int(samplerate * float(onset)), int(samplerate * float(offset))):
                data[t].append(midipitch)
    f.closed
    return data

def test():
    filename = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/ISOL/NO/MAPS_ISOL_NO_M_S0_M60_AkPnCGdD.wav'
    midi_file = dirs.get_midi(filename)
    wav_file = dirs.get_wav(filename)
    txt_file = dirs.get_txt(filename)
    wav_data = get_wav_data(wav_file)
    wf = get_wav_file(filename)
    samplerate = wf.samplerate
    nframes = wf.nframes
    data = get_wav_data(filename)
    txt_data = get_txt_as_label(txt_file, samplerate, nframes)

