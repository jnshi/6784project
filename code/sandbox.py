from scikits.audiolab import *
import pylab
import numpy as np
import matplotlib.pyplot as plt
from scikits.audiolab import play
import scipy
from sklearn import svm

import audioprocessor as ap
import dirs
import experiments as exp
import features
import util

filename = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/ISOL/NO'

X = []
Y = []

files = dirs.get_files_with_extension(filename, '.mid')
print len(files)

for f in files:
    wav_filename = dirs.get_wav(f)
    txt_filename = dirs.get_txt(f)
    wf = ap.get_wav_file(wav_filename)
    framesamp = 1024
    hopsamp = 80
    x = features.get_wav_as_feature(wav_filename)
    y = features.get_txt_as_label_for_note(txt_filename, 60, wf.samplerate, len(x))
    print len(x)
    X.extend(x)
    Y.extend(y)
    break


filename = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/ISOL/NO/MAPS_ISOL_NO_F_S0_M21_AkPnCGdD.mid'
