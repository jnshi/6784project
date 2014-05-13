import matplotlib.pyplot as plt
import numpy as np
import pylab
from scikits.audiolab import play
import scipy
from sklearn.multiclass import OneVsRestClassifier
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

samples_per_file = 5

framesamp = 1024
hopsamp = 80

num = 0


def get_data(f, sub = True):
    global framesamp, hopsamp
    wav_filename = dirs.get_wav(f)
    txt_filename = dirs.get_txt(f)
    wav_data, samplerate = ap.get_wav_data(wav_filename)
    x = features.get_wav_data_as_feature(wav_data, framesamp, hopsamp, True)
    y = features.get_txt_as_label(txt_filename, samplerate/8, framesamp, hopsamp, len(x), True)

    if sub:
        start, end = ut.get_trim_indices(x)

        subx = x[start: end]
        suby = y[start: end]

        if (len(subx) > samples_per_file):
            ind = random.sample(range(len(subx)), samples_per_file)
            subx = [subx[i] for i in ind]
            suby = [suby[i] for i in ind]
    else:
        subx = x
        suby = y

    return (copy.deepcopy(subx), copy.deepcopy(suby))
   

#@profile
def per_file(f):
    global num, X, Y
    subx, suby = get_data(f, True)
    X.extend(copy.deepcopy(subx))
    Y.extend(copy.deepcopy(suby))

    num += 1
    if num % 10 == 0:
        print num

def svm_test(clf, files):
    tX = []
    tY = []

    for f in files:
        subx, suby = get_data(f, True)
        tX.extend(subx)
        tY.extend(suby)

    pY = clf.predict(tX)
    ptaf = 0 # predict, actual
    ptat = 0
    pfat = 0
    pfaf = 0
    for py, ty in zip(pY, ty):
        for i in range(len(py)):
            if py[i] and ty[i]:
                ptat += 1
            elif py[i] and not ty[i]:
                ptaf += 1
            elif not py[i] and ty[i]:
                pfat += 1
            else:
                pfaf += 1
    return (ptaf, ptat, pfat, pfaf)

#@profile
def test():
    notes_train = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/ISOL/NO'
    randomchords_train = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/RAND/M21-108'
    randomchords_test = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/RAND/M36-95'

    files = []
    files.extend(dirs.get_files_with_extension(notes_train, '.mid'))
    files.extend(dirs.get_files_with_extension(randomchords_train, '.mid'))
    print 'num files '+str(len(files))

    map(per_file, files)
   
    print len(X) 
    clf = svm.SVC(kernel='linear')
    clf = OneVsRestClassifier(svm.SVC(kernel='linear'))
    clf.fit(X, Y)

    results = svm_test(clf, dirs.get_files_with_extension(randomchords_test, '.mid'))
    print results

test()
# cProfile.run('re.compile(test())')
