from scikits.audiolab import *
import pylab
import numpy as np
import matplotlib.pyplot as plt
from scikits.audiolab import play
import scipy

import audioprocessor
import experiments
import util

filename = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/ISOL/NO/MAPS_ISOL_NO_M_S0_M60_AkPnCGdD.wav'

# Sndfile(filename, mode=r, Format format=None, int channels=0, int samplerate=0)

f = audioprocessor.get_data(filename)
nframes = f.nframes
data = f.read_frames(nframes)
left = map(lambda x: x[0], data)
right = map(lambda x: x[1], data)
fs = f.samplerate
N = 1024
hopsamp = 80

X = util.stft(left, N, hopsamp)


pylab.figure()
pylab.imshow(scipy.absolute(X.T), origin='lower', aspect='auto', interpolation='nearest')
pylab.xlabel('Time')
pylab.ylabel('Frequency')
pylab.title('C4 - M60 (AkPnCGdD)')
pylab.show()


'''
X = util.stft(data, fs, framesz, hop)

pylab.figure()
pylab.imshow(scipy.absolute(X.T), origin='lower', aspect='auto', interpolation='nearest')
pylab.xlabel('Time')
pylabel.ylabel('Frequency')
pylab.show()

xhat = util.istft(X, fs, T, hop)

T1 = int(.1*fs)

pylab.figure()
pylab.plot(t[:T1], x[:T1], t[:T1], xhat[:T1])
pylab.xlabel('Time (seconds)')

pylab.figure()
pylab.plot(t[-T1:], x[-T1:], t[-T1:], xhat[-T1:])
pylab.xlabel('Time (seconds)')
'''

# output one second of stereo gaussian white noise at 48000 hz
#play(np.rot90(data))
#play(0.05 * np.random.randn(2, 48000))


def processWav(filename, channel):
    """
    filename: path to a wav file
    Channel: 1 for left, 2 for right
    Returns centroids, frequencies, volumes
    """
    #open file
    audio_file = sndfile(filename, 'read')
    #should be length of audiofile in seconds * 60. will fix this later
    import contextlib
    import wave
    with contextlib.closing(wave.open(filename, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    duration *= 30 #30 data points for every second of audio yay
    duration = int(duration) #can only return an integer number of frames so yeah
    #print duration
    #Not really samples per pixel but I'll let that slide
    samples_per_pixel = audio_file.get_nframes() / float(duration)
    #some rule says this frequency has to be half of the sample rate
    nyquist_freq = (audio_file.get_samplerate() / 2) + 0.0
    #fft_size stays 4096
    processor = AudioProcessor(audio_file, 2048, channel, numpy.hanning)

    centroids = []
    frequencies = []
    volumes = []

    for x in range(duration):
        seek_point = int(x * samples_per_pixel)
        next_seek_point = int((x + 1) * samples_per_pixel)
        (spectral_centroid, db_spectrum) = processor.spectral_centroid(seek_point)
        peaks = processor.peaks(seek_point, next_seek_point)      
        centroids.append(spectral_centroid)
        frequencies.append(db_spectrum)
        volumes.append(peaks)

    #print "Centroids:" + str(centroids)
    #print "Frequencies:" + str(frequencies)
    #print "Volumes:" + str(volumes)

    #convert volumes[] from peaks to actual volumes
    for i in range(len(volumes)):
        volumes[i] = abs(volumes[i][0]) + abs(volumes[i][1])
    #round frequencies to save resources
    for i in range(len(frequencies)):
        for j in range(len(frequencies[i])):
            frequencies[i][j] = round(frequencies[i][j], 4)
    return centroids, frequencies, volumes


