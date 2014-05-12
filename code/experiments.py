import audioprocessor
import matplotlib.pyplot as plt

def print_waveform(filename):
    f = audioprocessor.get_data(filename)
    data = f.read_frames(f.nframes)

    plt.subplot(2, 1, 1)
    plt.plot(range(len(data)), map(lambda x: x[0], data), 'k-')
    plt.xlabel('Left speaker')
    plt.title('Wave form of M23 (AkPnCGdD)')
    plt.subplot(2, 1, 2)
    plt.plot(range(len(data)), map(lambda x: x[1], data), 'r-')
    plt.xlabel('Right speaker')
    plt.show()


