#! /home/derkacy/programs/Python-3.6.2/built/bin/

# script to take PHOENIX synthetic spectra and convert to standard two column format
# file writes out in standard ascii format

import os
import numpy as np
import my_funcs
import astropy as ap
from astropy.table import Table

def read_phx (fname):
    """converts eddies my_funcs.rdsyngf function to astropy table format"""
    w, f = my_funcs.rdsyngf(fname)
    t = Table([w,f], names=['wl','flux'])
    return t

#get input data
cwd = os.getcwd()
path = input('Path to directory containing data (cwd: '+cwd+'): ') #USE RELATIVE PATH
#path='/'
synth_spec = input('PHOENIX spectrum: ')
phx_path = cwd+path+synth_spec
trim = input('Trim spectrum? (y/n): ')
trim = trim.lower()
if trim == 'y':
    xlow = input('Lower trim limit (in Angstroms): ')
    xlow = float(xlow)
    xhigh = input('Lower trim limit (in Angstroms): ')
    xhigh = float(xhigh)    

#read in table
tin = read_phx(phx_path)

#trim table (if necessary)
if trim == 'y':
    maskl = tin['wl'] > xlow
    tin = tin[maskl]
    maskh = tin['wl'] < xhigh
    tin = tin[maskh]

#write out table
if trim =='y':
    tname = synth_spec.split('.')[0]+'_'+str(xlow)+'-'+str(xhigh)+'_2col.dat'
else:
    tname = synth_spec.split('.')[0]+'_2col.dat'
Table.write(tin, tname, include_names=tin.colnames, format='ascii.no_header', delimiter=' ')
print('finished writing table to: '+cwd+'/'+tname)
