from scikits.audiolab import *

def get_data(filename):
    f = Sndfile(filename, 'r')
    
    fs = f.samplerate
    nc = f.channels
    enc = f.encoding
    nframes = f.nframes
    return f
