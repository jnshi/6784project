import audioprocessor
import matplotlib.pyplot as plt
import util
import scipy
import pylab
import numpy as np

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


def print_discriminitive_results():
    x = range(100, 1001, 100)
    ptat = [1001, 925, 1072, 1145, 980, 1166, 1036, 999, 1186, 1081]
    ptaf = [214, 269, 269, 328, 263, 284, 268, 238, 305, 266]
    pfat = [2724, 2800, 2774, 2580, 2745, 2559, 2689, 2726, 2539, 2644]
    pfaf = [3384, 3329, 3329, 3270, 3335, 3314, 3330, 3360, 3293, 3332]

    total = [float(ptat[i]+ptaf[i]+pfat[i]+pfaf[i]) for i in range(len(ptat))]
    perptat = [ptat[i]/total[i] for i in range(len(ptat))]
    perptaf = [ptaf[i]/total[i] for i in  range(len(ptaf))]
    perpfat = [pfat[i]/total[i] for i in range(len(ptaf))]
    perpfaf = [pfaf[i]/total[i] for i in range(len(pfaf))]
    plt.plot(x, perptat, 'ro-', label='ptat')
    plt.plot(x, perptaf, 'bo-', label='ptaf')
    plt.plot(x, perpfat, 'go-', label='pfat')
    plt.plot(x, perpfaf, 'yo-', label='pfaf')
    plt.title('Discriminitive one-vs-all performance')
    plt.xlabel('Number of samples in training set for one classification')
    plt.ylabel('Percentage')
    plt.legend(bbox_to_anchor=(1.02, 1), loc=2)
    plt.show()

def print_comparision_one():
    bar_width = .2
    index = np.arange(4)
    ptat = [223, 167, 450, 1804]
    pfaf = [620, 2516, 4804, 13619]
    ptaf = [1005, 3184, 387, 1465]
    pfat = [133, 1927, 359, 1112]
    total = [float(ptat[i]+ptaf[i]+pfat[i]+pfaf[i]) for i in range(len(ptat))]

    perptat = [ptat[i]/total[i] for i in range(len(ptat))]
    perptaf = [ptaf[i]/total[i] for i in  range(len(ptaf))]
    perpfat = [pfat[i]/total[i] for i in range(len(ptaf))]
    perpfaf = [pfaf[i]/total[i] for i in range(len(pfaf))]
    opacity = .4 

    rects1 = plt.bar(index, perptat, bar_width,
        color = 'r',
        alpha = opacity,
        label = 'Predict True, Actual True')
    rects2 = plt.bar(index + bar_width, perptaf, bar_width,
        color='b',
        alpha = opacity,
        label = 'Predict True, Actual False')
    rects3 = plt.bar(index + 2*bar_width, perpfat, bar_width,
        color='g',
        alpha = opacity,
        label = 'Predict False, Actual True')
    rects4 = plt.bar(index + 3*bar_width, perpfaf, bar_width,
        color='y',
        alpha = opacity,
        label= 'Predict False, Actual False')

    plt.xticks(index + 2*bar_width, ('dis 1/3', 'dis 3/9', 'struct 1/3', 'struct 3/9'))
    plt.xlabel('Group')
    plt.ylabel('Percentage')
    plt.title('One-vs-All SVM compared with Max-Margin Markov')
    plt.legend()
    plt.show()

def print_comparision_two():
    bar_width = .2
    index = np.arange(6)
    ptat = [233, 254, 142,333, 1488, 1650]
    pfaf = [1581, 2561, 3237,8785,15693,22549]
    ptaf = [1035, 1832, 3130, 365, 1420,2501]
    pfat = [142, 233, 158, 517, 1399,3300]
    total = [float(ptat[i]+ptaf[i]+pfat[i]+pfaf[i]) for i in range(len(ptat))]

    perptat = [ptat[i]/total[i] for i in range(len(ptat))]
    perptaf = [ptaf[i]/total[i] for i in  range(len(ptaf))]
    perpfat = [pfat[i]/total[i] for i in range(len(ptaf))]
    perpfaf = [pfaf[i]/total[i] for i in range(len(pfaf))]
    opacity = .4 

    rects1 = plt.bar(index, perptat, bar_width,
        color = 'r',
        alpha = opacity,
        label = 'Predict True, Actual True')
    rects2 = plt.bar(index + bar_width, perptaf, bar_width,
        color='b',
        alpha = opacity,
        label = 'Predict True, Actual False')
    rects3 = plt.bar(index + 2*bar_width, perpfat, bar_width,
        color='g',
        alpha = opacity,
        label = 'Predict False, Actual True')
    rects4 = plt.bar(index + 3*bar_width, perpfaf, bar_width,
        color='y',
        alpha = opacity,
        label= 'Predict False, Actual False')

    plt.xticks(index + 2*bar_width, ('dis 1/5', 'dis 2/10', 'dis 3/15', 'struct 1/5', 'struct 2/10', 'struct 3/15'))
    plt.xlabel('Group')
    plt.ylabel('Percentage')
    plt.title('One-vs-All SVM compared with Max-Margin Markov')
    plt.legend()
    plt.show()

'''
filename = '/home/charles/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/ISOL/NO/MAPS_ISOL_NO_F_S0_M28_AkPnCGdD.wav'
print_mapfreq(filename, 'M23 (AkPnCGdD)')
'''

print_comparision_two()
