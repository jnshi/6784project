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
import util

filename = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/ISOL/NO/MAPS_ISOL_NO_M_S0_M60_AkPnCGdD.wav'

def train_single_svm(note, files):
    X = []
    Y = []
    for f in files:
        file_info = dirs.parse_file(f)
        if (file_info['mm'] == note):
            Y.append(1)
        else:
            Y.append(0)

        data = ap.get_data(filename)
        left = ap.get_left(data)
        trim = ut.trim_array(left)
        x = ut.stft(trim, 1024, 80)
        X.append(x)

X = [x]
y = [1]

clf = svm.SVC()
clf.fit()
