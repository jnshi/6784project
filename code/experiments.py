import audioprocessor
import matplotlib.pyplot as plt
import util
import scipy
import pylab

def print_waveform(filename):
    f = audioprocessor.get_wav_file(filename)
    data = f.read_frames(f.nframes)

    plt.subplot(2, 1, 1)
    plt.plot(range(len(data)), map(lambda x: x[0], data), 'k-')
    plt.xlabel('Left speaker')
    plt.title('Wave form of M23 (AkPnCGdD)')
    plt.subplot(2, 1, 2)
    plt.plot(range(len(data)), map(lambda x: x[1], data), 'r-')
    plt.xlabel('Right speaker')
    plt.show()

def print_singlefreq(filename, title):
    f = audioprocessor.get_wav_file(filename)
    nframes = f.nframes
    data = f.read_frames(nframes)
    left = map(lambda x: x[0], data)
    right = map(lambda x: x[1], data)
    N = 1024
    hopsamp = 80

    X = util.stft(left, N, hopsamp)
    t = X[300].T

    plt.plot(range(len(t)), scipy.absolute(t))
    plt.xlabel('frequency')
    plt.ylabel('amplitude')
    plt.title(title)
    plt.show()

def print_mapfreq(filename, title):
    f = audioprocessor.get_wav_file(filename)
    nframes = f.nframes
    data = f.read_frames(nframes)
    left = map(lambda x: x[0], data)
    right = map(lambda x: x[1], data)
    N = 1024
    hopsamp = 80

    X = util.stft(left, N, hopsamp)

    pylab.figure()
    pylab.imshow(scipy.absolute(X.T), origin='lower', aspect='auto', interpolation='nearest')
    pylab.xlabel('Time')
    pylab.ylabel('Frequency')
    pylab.title(title)
    pylab.show()

'''
filename = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/ISOL/NO/MAPS_ISOL_NO_F_S0_M28_AkPnCGdD.wav'
print_mapfreq(filename, 'M23 (AkPnCGdD)')
'''
