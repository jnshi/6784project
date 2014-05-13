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
import sys

import audioprocessor as ap
import dirs
#import experiments as exp
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
    y = features.get_txt_as_label_for_note(txt_filename, 60, samplerate/8, framesamp, hopsamp, len(x))
#    y = features.get_txt_as_label_for_note(txt_filename, 102, samplerate/8, framesamp, hopsamp, len(x))
    start, end = ut.get_trim_indices(x)
    trunc = 2000
    if end-start > trunc:
        print("\t%d windows, truncated to %d" % (end-start, trunc))
    end = min(end, trunc+start)

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
    ntrain = nfiles
    ntest = 5*nfiles
    print("Training/testing with %d/%d files." % (ntrain,ntest))
    start = time.clock()   
 
    filename = '../maps/MAPS_AkPnCGdD_2/AkPnCGdD/MUS'
    #filename = '../maps/MAPS_AkPnCGdD_1/AkPnCGdD/ISOL/NO'
    files = dirs.get_files_with_extension(filename, '.mid')
    train_files = files[:ntrain]
    print("\t" + str(train_files))
    #test_files = files[ntrain:ntest+ntrain]
    # for legit testing
    test_files = files[-ntest:]
    map(per_file, train_files,
      it.repeat(X, ntrain), it.repeat(Y, ntrain))
    map(per_file, test_files,
      it.repeat(X_tst, ntest), it.repeat(Y_tst, ntest))

    end = time.clock()
    print("\tRead time: %f" % (end - start))
    print("\tnWindows train: " + str([X[i].shape[0] for i in range(len(X))]))
    start = time.clock()   

    crf = ChainCRF(n_states=2)
    clf = OneSlackSSVM(model=crf, C=100, n_jobs=-1,
          inference_cache=100, tol=.1)
    clf.fit(np.array(X), np.array(Y))

    end = time.clock()
    print("\tTrain time: %f" % (end - start))
    start = time.clock()   

    Y_pred = clf.predict(X_tst)
    comp = []
    for i in range(len(Y_tst)):
      for j in range(len(Y_tst[i])):
        comp.append((Y_tst[i][j], Y_pred[i][j]))
        print Y_tst[i][j],
      print
      for j in range(len(Y_tst[i])):
        print Y_pred[i][j],
      print
      print

    print("\tTrue positives: %d" % comp.count((1,1)))
    print("\tTrue negatives: %d" % comp.count((0,0)))
    print("\tFalse positives: %d" % comp.count((0,1)))
    print("\tFalse negatives: %d" % comp.count((1,0)))
    

    end = time.clock()
    print("\tTest time: %f" % (end - start))


#for i in range(1,100):
#  test(int(i*(i+1)/2))
test(int(sys.argv[1]))
# cProfile.run('re.compile(test())')
