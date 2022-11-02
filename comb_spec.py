import numpy as np
import astropy as ap
from astropy.table import Table

def combine_spec(bt, rt, cval):
    #cut tables at cval
    tbt = bt[bt['col1']<cval]
    trt = rt[rt['col1']>cval]
    #scale fluxes to match at cval
    msmin = min(tbt['col2'][len(tbt)-1],trt['col2'][0])
    msmax = max(tbt['col2'][len(tbt)-1],trt['col2'][0])
    if (tbt['col2'][len(tbt)-1]) == msmin:
        tbt['col2'] = (msmax/msmin)*tbt['col2']
    else:
        trt['col2'] = (msmax/msmin)*trt['col2']
    #write values to one table
    tf = Table(names=['wl', 'flux'], dtype=('float64','float64'))
    for i in range(len(tbt)):
        tf.add_row(tbt[i])
    for j in range(len(trt)):
        tf.add_row(trt[j])
    return tf
