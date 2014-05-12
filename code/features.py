import numpy as np

import audioprocessor as ap
import dirs
import util as ut

def get_wav_as_feature(filename):
    data = ap.get_wav_data(filename)
    left = ap.get_left(data)
    return ut.stft(left, 1024, 80)

def get_txt_as_label(filename, samplerate, framesamp, hopsamp, nwindows):
    assert dirs.get_ext(filename) == '.txt'
    data = np.array([[0 for i in range(88)] for i in range(nwindows)])
    with open(filename, 'r') as f:
        content = f.readlines()
        for i in range(1, len(content)):
            onset, offset, midipitch = content[i].split()


            startwindow = int(samplerate * float(onset))
            endwindow = 0

            for t in range(int(samplerate * float(onset)), int(samplerate * float(offset))):
                data[t][midipitch] = 1
    f.closed
    return data

def get_txt_as_label_for_note(filename, samplerate, nwindows, note):
    assert dirs.get_ext(filename) == '.txt'
    data = np.array([0 for i in range(nwindows)])
    with open(filename, 'r') as f:
        content = f.readlines()
        for i in range(1, len(content)):
            onset, offset, midipitch = content[i].split()
            for t in range(int(samplerate * float(onset)), int(samplerate * float(offset))):
                data[t] = int(midipitch == note)
    f.closed
    return data 

