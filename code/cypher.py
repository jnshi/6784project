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
import shutil

import audioprocessor as ap
import dirs
import features
import util as ut

posX = []
posY = []
negX = []
negY = []

positive_samples_per_file = 20000
negative_samples_per_file = 20000

windows_per_file = 2000

framesamp = 1024
hopsamp = 80

num = 0

def get_data(f, note, sub = True):
    global framesamp, hopsamp
    wav_filename = dirs.get_wav(f)
    txt_filename = dirs.get_txt(f)
    wav_data, samplerate = ap.get_wav_data(wav_filename)
    x = features.get_wav_data_as_feature(wav_data, framesamp, hopsamp, True)
    y = features.get_txt_as_label_for_note(txt_filename, note, samplerate/8, framesamp, hopsamp, len(x), True)

    start, end = ut.get_trim_indices(x)
    end = min(end, windows_per_file + start)
    x = x[start:end]
    y = y[start:end]

    posx = []
    posy = []
    negx = []
    negy = []

    # balance
    for i in range(len(x)):
        if y[i]:
            posx.append(x[i])
            posy.append(y[i])
        else:
            negx.append(x[i])
            negy.append(y[i])

    return (copy.deepcopy(posx), copy.deepcopy(posy), copy.deepcopy(negx), copy.deepcopy(negy))
   

#@profile
def per_file(note):
    global num, posX, posY, negX, negY
    def per_file_help(f):
        posx, posy, negx, negy = get_data(f, note, True)
        if (len(posx) > positive_samples_per_file):
            indices = random.sample(range(len(posx)), positive_samples_per_file)
        else:
            indices = range(len(posx))
        posX.extend([posx[i] for i in indices])
        posY.extend([posy[i] for i in indices])
        
        if (len(negx) > negative_samples_per_file):
            indices = random.sample(range(len(negx)), negative_samples_per_file)
        else:
            indices = range(len(negx))

        negX.extend([negx[i] for i in indices])
        negY.extend([negy[i] for i in indices])

    return per_file_help

def svm_test(clf, note, files):
    posX = []
    posY = []
    negX = []
    negY = []

    for f in files:
        posx, posy, negx, negy = get_data(f, note, True)

        if (len(posx) > positive_samples_per_file):
            indices = random.sample(range(len(posx)), positive_samples_per_file)
        else:
            indices = range(len(posx))

        posX.extend([posx[i] for i in indices])
        posY.extend([posy[i] for i in indices])

        if (len(negx) > negative_samples_per_file):
            indices = random.sample(range(len(negx)), negative_samples_per_file)
        else:
            indices = range(len(negx))

        negX.extend([negx[i] for i in indices])
        negY.extend([negy[i] for i in indices])


    tX = []
    tX.extend(posX)
    tX.extend(negX)
    tY = []
    tY.extend(posY)
    tY.extend(negY)

    pY = clf.predict(np.array(tX))
    ptaf = 0 # predict, actual
    ptat = 0
    pfat = 0
    pfaf = 0
    for py, ty in zip(pY, tY):
        if py and ty:
            ptat += 1
        if py and not ty:
            ptaf += 1
        if not py and ty:
            pfat += 1
        if not py and not ty:
            pfaf += 1
    return (ptat, ptaf, pfat, pfaf)

#@profile
def test():
    global posX, negX, posY, negY
#    train_dir = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/ISOL'
#    test_dir = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/RAND'
#    train_file = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_2/AkPnCGdD/MUS/MAPS_MUS-chpn_op10_e12_AkPnCGdD.mid'
#    test_file = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_2/AkPnCGdD/MUS/MAPS_MUS-grieg_kobold_AkPnCGdD.mid'
    filename = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_2/AkPnCGdD/MUS'
    files = dirs.get_files_with_extension(filename, '.mid')        
    note = 60
    
    for nindex in range(1, 100):
        posX = []
        negX = []
        posY = []
        negY = []

        nfiles = int(nindex*(nindex+1)/2)
        ntrain = nfiles
        ntest = 3*nfiles

        train_files = files[:nfiles]
#        print 'train_files: ' + str(train_files)

        map(per_file(note), train_files)

        print len(posX)
        print len(negX)  
        ind = random.sample(range(len(negX)), len(posX))

        X = []
        X.extend(posX)
        X.extend([negX[i] for i in ind])

        Y = []
        Y.extend(posY)
        Y.extend([negY[i] for i in ind])

        clf = svm.SVC(kernel='linear')
        clf.fit(np.array(X), np.array(Y))

        test_files = files[nfiles:nfiles+ntrain]
#        print 'test_files: ' + str(test_files)
        results = svm_test(clf, note, test_files)
        print str(nfiles) + ' ' + ' '.join([str(r) for r in results])

test()
# cProfile.run('re.compile(test())')
