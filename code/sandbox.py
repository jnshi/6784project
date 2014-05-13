import matplotlib.pyplot as plt
import numpy as np
import pylab
from scikits.audiolab import play
import scipy
from sklearn import svm
import random
import cProfile
import re
#from guppy import hpy
import gc
import copy
import time

import audioprocessor as ap
import dirs
import experiments as exp
import features
import util as ut
import itertools as it

from pystruct.models import ChainCRF
from pystruct.learners import OneSlackSSVM

samples_per_file = 10

def per_file(f, X, Y):
    wav_filename = dirs.get_wav(f)
    txt_filename = dirs.get_txt(f)
    wav_data, samplerate = ap.get_wav_data(wav_filename)
    framesamp = 1024
    hopsamp = 80
    x = features.get_wav_data_as_feature(wav_data, framesamp, hopsamp, True)
    y = features.get_txt_as_label_for_note(txt_filename, 60, samplerate, framesamp, hopsamp, len(x))
    start, end = ut.get_trim_indices(x)
    end = min(end, 100000)

    subx = x[start: end]
    suby = y[start: end]

    # get rid of complex complexities    
    subx = abs(subx)

#    ind = random.sample(range(len(subx)), samples_per_file)
#    subx = [subx[i] for i in ind]
#    suby = [suby[i] for i in ind]
    
    X.append(copy.deepcopy(subx))
    Y.append(copy.deepcopy(suby))



def test(nfiles):
    X = []
    Y = []
    X_tst = []
    Y_tst = []
    print("Training/testing with %d files." % nfiles)
    start = time.clock()   
 
    filename = '../maps/MAPS_AkPnCGdD_2/AkPnCGdD/MUS'
    files = dirs.get_files_with_extension(filename, '.mid')
    train_files = files[:nfiles]
    print("\t" + str(train_files))
    test_files = files[nfiles:2*nfiles]
    map(per_file, train_files,
      it.repeat(X, nfiles), it.repeat(Y, nfiles))
    map(per_file, test_files,
      it.repeat(X_tst, nfiles), it.repeat(Y_tst, nfiles))

    end = time.clock()
    print("\tRead time: %f" % (end - start))
    start = time.clock()   

    crf = ChainCRF(n_states=2)
    clf = OneSlackSSVM(model=crf, C=100, n_jobs=-1,
          inference_cache=100, tol=.1)
    clf.fit(X, Y)

    end = time.clock()
    print("\tTrain time: %f" % (end - start))
    start = time.clock()   

    score = clf.score(X_tst,Y_tst)

    end = time.clock()
    print("\tTest time: %f" % (end - start))
    print("\tCRF test set accuracy: %f" % score)


for i in range(1,100):
  test(int(i*(i+1)/2))
# cProfile.run('re.compile(test())')
