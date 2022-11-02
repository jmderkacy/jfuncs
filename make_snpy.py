#script to create formatted inputs for SNooPy from indidivual band photometry
#files (typically from OSC or similar source)

import os
import numpy as np
import astropy as ap
from astropy.table import Table

cwd = os.getcwd()
data_path = input('Path to data (cwd: '+cwd+'): ')
#data_file = input('File to read: ')

#check file path for absolute or relative path
fpath=''
try:
    if data_path.starts_wth('~') or data_path.starts_with('/home'):
        fpath = data_path
    else:
        fpath = cwd+data_path
except:
    fpath=cwd
    
#open file to begin writing data

    
#scan working directory for photometry files
try:
    with os.scandir(fpath) as loc:
        for entry in loc:
            if entry.name.endswith('.dat'):
                continue
            else:
                continue
