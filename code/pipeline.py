import midi

filename = '/home/charles/maps-data/maps/MAPS_AkPnStgb_1/AkPnStgb/ISOL/NO/MAPS_ISOL_NO_F_S0_M26_AkPnStgb.mid'
pattern = midi.read_midifile(filename)
print pattern
