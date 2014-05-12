import matplotlib.pyplot as plt
import numpy as np
import pylab
from scikits.audiolab import play
import scipy
from sklearn import svm
import random
import cProfile
import re
from guppy import hpy
import gc
import copy

import audioprocessor as ap
import dirs
import experiments as exp
import features
import util as ut

X = []
Y = []

samples_per_file = 10

@profile
def per_file(f):
    wav_filename = dirs.get_wav(f)
    txt_filename = dirs.get_txt(f)
    wav_data, samplerate = ap.get_wav_data(wav_filename)
    framesamp = 1024
    hopsamp = 80
    x = features.get_wav_data_as_feature(wav_data, framesamp, hopsamp)
    y = features.get_txt_as_label_for_note(txt_filename, 60, samplerate, framesamp, hopsamp, len(x))
    start, end = ut.get_trim_indices(x)

    subx = x[start: end]
    suby = y[start: end]
    
    ind = random.sample(range(len(subx)), samples_per_file)
    subx = [subx[i] for i in ind]
    suby = [suby[i] for i in ind]
    
    X.extend(copy.deepcopy(subx))
    Y.extend(copy.deepcopy(suby))

@profile
def test():
    filename = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/ISOL/NO'

    files = dirs.get_files_with_extension(filename, '.mid')
    files = files[:80]

    map(per_file, files)

test()
# cProfile.run('re.compile(test())')
