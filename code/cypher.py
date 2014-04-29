from scikits.audiolab import *
import util
import pylab

filename = '/home/charles/maps-data/maps/MAPS_AkPnStgb_1/AkPnStgb/ISOL/NO/MAPS_ISOL_NO_F_S0_M26_AkPnStgb.wav'

# Sndfile(filename, mode=r, Format format=None, int channels=0, int samplerate=0)
f = Sndfile(filename, 'r')

fs = f.samplerate
nc = f.channels
enc = f.encoding
nframes = f.nframes

hop = .020
framesz = nframes/float(fs)

data = f.read_frames(nframes)

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
