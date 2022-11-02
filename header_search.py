#! /home/derkacy/programs/Python-3.6.2/built/bin

#script to search fits file headers for values in key words

import os
import astropy as ap
from astropy.io import fits

cwd = os.getcwd()
data_path = input('Path to data (cwd: '+cwd+'): ')

hline = input('Header line to retrieve: ')
hline = hline.upper()

hval = input('Header value to search for: ')

with os.scandir(data_path) as loc:
    for entry in loc:
        #print(entry)
        if entry.name.endswith('.fits') and entry.is_file():
            fname = data_path + entry.name
            hdul = fits.open(fname, mode='readonly')
            #print(hdul.info())
            val = hdul[0].header[hline]
            val = str(val)
            if val.find(hval) != -1:
                print(entry,val)
            #else:
            #    print(fname, 'Value Not Found!')
            hdul.close()
        else:
            continue
