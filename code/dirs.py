from os import listdir
from os.path import isfile, join, splitext
import math
import ntpath
import random

def folder_contents(directory, absolute=True):
    add_path = lambda f: join(directory, f) if absolute else f
    files = [add_path(f) for f in listdir(directory) if isfile(join(directory, f))]
    directories = [add_path(d) for d in listdir(directory) if not isfile(join(directory, f))]   
    return (files, directories)

def get_files(directory, recursive=True, absolute=True): 
    files, directories = folder_contents(directory, absolute)
    while recursive and directories:
        d = directories.pop()
        fs, ds = folder_contents(d, absolute)
        files.extend(fs)
        directories.extend(ds)
    return files

def get_files_with_extension(directory, extension, recursive=True, absolute=True):
    return filter(lambda x: get_ext(x) == extension, get_files(directory, recursive, absolute))

def order_files_by_extension(directory, recursive=True, absolute=True):
    files = get_files(directory, recursive, absolute)
    dic = {}
    for f in files:
        ext = get_ext(f)
        if ext not in dic:
            dic[ext] = []
        dic[ext].append(f)
    return dic

def segment_files_by_percentage(split, files):
    number = map(lambda x: int(math.floor(x * len(files))), split)
    total = sum(number)
    return segment_files_by_number(number, files) 

def segment_files_by_number(split, files):
    assert sum(split) <= len(files)
    i = 0
    segments = []
    random.shuffle(files)
    for s in split:
        segments.append(files[i:i+s])
        i += s
    return (segments, files[i:len(files)])

'''AkPnCGdD - Concert Grand D - studio - Akoustik Piano'''
base = '/home/charles'
data_isol = '%(base)s/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/ISOL' % {'base' : base}
data_rand = '%(base)s/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/RAND' % {'base' : base}
data_ucho = '%(base)s/maps-data/maps/MAPS_AkPnCGdD_1/AkPnCGdD/UCHO' % {'base' : base}
data_mus = '%(base)s/maps-data/maps/MAPS_AkPnCGdD_2' % {'base' : base}

'''subdirectories of isol'''
chromatic = 'CH'
notes = 'NO'
repeated = 'RE'
trill1 = 'TR1'
trill2 = 'TR2'
staccato = 'ST'

'''Used for ISOL'''
def parse_filename(path):
    name = ntpath.basename(path)
    name = name[0:len(name)-3] # remove extension
    div = name.split('_')
    return {'ps' : div[2], 'i0' : div[3], 'ss' : int(div[4][1:]), 'mm' :  int(div[5][1:])}

def get_ext(filename):
    return splitext(filename)[1]

def set_ext(filename, ext):
    return splitext(filename)[0] + ext

def get_midi(filename):
    return set_ext(filename, '.mid')

def get_wav(filename):
    return set_ext(filename, '.wav')

def get_txt(filename):
    return set_ext(filename, '.txt')



'''Standard train and test data'''


dir_notes = join(data_isol, notes)


    

'''Test method'''
def test():
    files = get_files(join(data_isol, notes), False, True)
    f = files[0]
    print f
    print parse_file(f)
