#Doppler shift script

import numpy as np
import scipy as sp
import astropy as ap
from astropy.table import Table, Column

#speed of light in km/s
c = 3e5

def nr_doppler(wl_rest, v):
    #assume stationary observer, utilize convention 
    #where positive velocity is away from observer
    if np.isscalar(wl_rest):
        wl_obs = (c/(c-v))*wl_rest
    else:
        wl_obs = []
        for i in range(len(wl_rest)-1):
            wl_obs[i] = (c/(c-v))*wl_rest
    return wl_obs    

def r_doppler(wl_rest, v):
    #assume stationary observer, utilize convention
    #where positive velocity is away from observer
    if np.isscalar(wl_rest):
        wl_obs = np.sqrt((1+(v/c))/(1-(v/c)))*wl_rest
    else:
        wl_obs = []
        for i in range(len(wl_rest)-1):
            wl_obs = np.sqrt((1+(v/c))/(1-(v/c)))*wl_rest
    return wl_obs

def rev_nr_doppler(wl_rest, wl_obs):
    #reverses nr_doppler formula above
    #positive velocity is away from observer
    if np.isscalar(wl_rest) and np.isscalar(wl_obs):
        v = c*(1-(wl_rest/wl_obs))
    elif np.isscalar(wl_rest) and (not np.isscalar(wl_obs)):
        v = []
        for i in range(len(wl_obs)-1):
            v = c*(1-(wl_rest/wl_obs))
    elif (not np.isscalar(wl_rest)) and np.isscalar(wl_obs):
        v=[]
        for i in range(len(wl_rest)-1):
            v = c*(1-(wl_rest/wl_obs))
    else:
        try:
            v=[]
            for i in range(len(wl_rest)-1):
                v = c*(1-(wl_rest/wl_obs))
        except:
            print('Array length mismatch')
    return v

def rev_r_doppler(wl_rest, wl_obs):
    #reverses r_doppler formula above
    #negative velocity is towards observer
    v = c*((((wl_obs/wl_rest)**2)-1)/(((wl_obs/wl_rest)**2)+1))
    return v

def deltav_from_specres(line, res):
    """Calculate the error in velocity space for a specified line
       given the resolution of a spectrograph"""

    #calculate spectral resolution in wavelgnth space
    dlam = line/res

    #calculate velocity difference from line
    perr = rev_r_doppler(line,line+dlam)
    nerr = rev_r_doppler(line,line-dlam)

    #get average value
    err = (np.abs(nerr)+np.abs(perr))/2.0

    return err

#wl = np.array([8000])
#wl=np.array([6355,6550,6783,7117,7234])
#v=np.array([1000,10000,10500,11000,11500,12000,12500,13000,13500,14000,14500,15000])
#v = np.array([15000,14000,13000,12000,11000,10000,9000,8000,7000,6000,5000,4000,3000,2000,1000])

#for i in range(len(v)):
#    wl_nrds = nr_doppler(wl, v[i])
#    wl_rds = r_doppler(wl,v[i])
#    print('At a velocity of',v[i],'km/s the doppler shifted velocities of the following lines are:')
#    print(wl)
#    print(wl_nrds)
#    print(wl_rds)

#v_nr = rev_nr_doppler(1550,1500)
#v_r = rev_r_doppler(1550,1500)
#print(1550,1500,'NR',v_nr)
#print(1550,1500,'R',v_r)
