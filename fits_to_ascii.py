#! /home/derkacy/programs/Python-3.6.2/built/bin/python3

#script to convert fits spectrum to ascii files using pyraf

import os
import subprocess
from subprocess import PIPE
import numpy as np
import astropy as ap
from astropy.io import fits

cwd = os.getcwd()

#Step 1 - Initialize IRAF

#scan working director for iraf directory. Create iraf 
#directory if needed, and change to iraf directory
with os.scandir(cwd) as loc:
    if os.path.isdir('iraf'):
        print('IRAF directory exists')
        os.chdir(cwd+'/iraf')
        cwd = os.getcwd()
        print('Working directory now: '+os.getcwd())
    else:
        print('IRAF directory not found!')
        print('Creating IRAF directory')
        os.mkdir('./iraf')
        os.chdir(cwd+'/iraf')
        cwd = os.getcwd()
        print('Working directory now: '+os.getcwd())

#initialize IRAF
with os.scandir(cwd) as loc2:
    if os.path.isfile('login.cl'):
        print('IRAF already initialized')
    else:
        try:
            subprocess.run("mkiraf", stdout=PIPE, stderr=PIPE, input='xgterm', universal_newlines=True, check=True)
        except:
            print('IRAF initialization failed. Exiting.')

#Step 2 - Examine header

#non-standard import placement to avoid cluttering drive with cache dirs
import pyraf
from pyraf import iraf

#get location to file
#data_dir = input('Input path to data_directory: ')
f = input('Input file name (cwd: '+cwd+'/ ): ')
#f = ftmp
#data_loc = data_dir+f

#print image header
iraf.imhead.longheader=True
iraf.imhead(f)

#Step 3 - Print spectrum to ascii file


#pester user for input to get correct location of spectral data
x = input('Input number of columns to output (default is *): ')
y = input('Input row number of output (default is 1, 3 for error): ')
z = input('Input z-location of output (default is 1 for spectra): ')

inname = f.rstrip('.fits')
outname = inname+'.txt'
fout = f+'['+str(x)+','+str(y)+','+str(z)+']'

iraf.wspectext(fout, output=outname, header=False)
print('File written to : '+outname)

#add additional steps if wanted (ex. dereddening), etc.

exit()
#EOF
