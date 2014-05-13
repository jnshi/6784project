import numpy as np
import scipy, pylab
import scipy.signal

def frame_to_window(frame, framesamp, hopsamp, nwindows):
    swindow = (frame - framesamp) / hopsamp + 1
    swindow = swindow if swindow > 0 else 0
    ewindow = frame / hopsamp
    ewindow = ewindow if ewindow < nwindows else nwindows
    return (swindow, ewindow)

def trim_array(X):
    start, end = get_trim_indices(X)
    return X[start:end]

def get_trim_indices(X):
    start = 0
    end = len(X)
    for i in range(len(X)):
        if (np.count_nonzero(X[i]) != 0):
            start = i
            break
    for i in range(len(X)-1, -1, -1):
        if (np.count_nonzero(X[i]) != 0):
            end = i
            break
    return (start-1, end+1)

# http://docs.scipy.org/doc/scipy-0.13.0/reference/generated/scipy.signal.decimate.html#scipy.signal.decimate
def downsample(x, q):
    return scipy.signal.decimate(x, q)

# https://ccrma.stanford.edu/~jos/parshl/Short_Time_Fourier_Transform_STFT.html
# Poliner: framesamp = 1024, hopsamp = 80
def stft(x, framesamp, hopsamp):
    w = scipy.hamming(framesamp)
    X = scipy.array([np.fft.rfft(w*x[i:i+framesamp]) 
                     for i in range(0, len(x)-framesamp, hopsamp)])
    return X

def istft(X, fs, T, hop):
    x = scipy.zeros(T*fs)
    framesamp = X.shape[1]
    hopsamp = int(hop*fs)
    for n,i in enumerate(range(0, len(x)-framesamp, hopsamp)):
        x[i:i+framesamp] += scipy.real(scipy.ifft(X[n]))
    return x

'''
def frames_to_windows(frame, framesamp, hopsamp):
    window = 0
    swindow = -1
    sframe = window * hopsamp
    while frame > sframe:
        sframe = window * hopsamp
        eframe = sframe + framesamp
        if frame < eframe and swindow == -1:
            swindow = window
        window +=1
    ewindow = window - 1
    return (swindow, ewindow)
'''



