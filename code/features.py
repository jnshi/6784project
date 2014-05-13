import numpy as np

import audioprocessor as ap
import dirs
import util as ut

downsample_rate = 8

def get_wav_file_as_feature(filename, framesamp, hopsamp, downsample=False):
    data, samplerate = ap.get_wav_data(filename)
    return get_wav_data_as_feature(data, framesamp, hopsamp, downsample)

def get_wav_data_as_feature(data, framesamp, hopsamp, downsample=False):
    left = ap.get_left(data)
    if downsample: left = ap.downsample(left, downsample_rate)
    return ut.stft(left, framesamp, hopsamp)

def get_txt_as_label(filename, samplerate, framesamp, hopsamp, nwindows, downsample=False):
    assert dirs.get_ext(filename) == '.txt'
    data = [[0 for i in range(88)] for j in range(nwindows)]
    with open(filename, 'r') as f:
        content = f.readlines()
        for i in range(1, len(content)):
            onset, offset, midipitch = content[i].split()
            sframe = int(float(onset) * samplerate)
            eframe = int(float(offset) * samplerate)
            swindow, _ = ut.frame_to_window(sframe, framesamp, hopsamp, nwindows)
            _, ewindow = ut.frame_to_window(eframe, framesamp, hopsamp, nwindows)
            for w in range(swindow, ewindow):
                data[w][int(midipitch)-21] = 1
    f.closed
    return data

def get_txt_as_label_for_note(filename, note, samplerate, framesamp, hopsamp, nwindows, downsample=False):
    assert dirs.get_ext(filename) == '.txt'
    data = np.array([0 for i in range(nwindows)])
    with open(filename, 'r') as f:
        content = f.readlines()
        for i in range(1, len(content)):
            onset, offset, midipitch = content[i].split()
            sframe = int(float(onset) * samplerate)
            eframe = int(float(offset) * samplerate)
            swindow, _ = ut.frame_to_window(sframe, framesamp, hopsamp, nwindows)
            _, ewindow = ut.frame_to_window(eframe, framesamp, hopsamp, nwindows)
            for w in range(swindow, ewindow):
                data[w] = int(int(midipitch) == note)
    f.closed
    return data 

