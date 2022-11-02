######################################################################
## Filename:      smooth_spex.py
# Author:        Eddie Baron <baron@ou.edu>
# Created at:    Fri Apr 19 10:35:11 2019
# Modified at:   Thu Jul  9 09:38:38 2020
# Modified by:   Eddie Baron <baron@ou.edu>
# Description:   example based on Semeli's code
######################################################################
from spextractor import Spextractor


def report(magnitude, error):
    for k in sorted(magnitude):
        print(k, magnitude[k], '+-', error[k])

def smooth_spex(data,z,sigma_outliers=6):
  


  spex = Spextractor(data=data, z=z, auto_prune=False)
  spex.create_model(sigma_outliers=sigma_outliers, downsampling=1,
                    model_uncertainty=False)

  model = spex.model
  w = spex.wave
  f = spex.flux

  lpred = len(w) * 4
  xpred = np.linspace(w[1].round(0), w[-2].round(0), lpred)
  mean, var = spex.predict(xpred)
  sigma = np.sqrt(var)

  return xpred,mean,sigma

if __name__ == "__main__":

  import my_funcs
  import numpy as np
  import pylab
  
  infile = input("Give spectrum: ")
  z = input("Give redshift: (return for none): ")
  if z == "":
    z = None
  else:
    z = float(z)
    
  #w,f = my_funcs.read_sp_data_fits(infile)
  w,f = my_funcs.read_sp_data(infile)
  data = np.stack((w,f),axis=1)
  xpred,mean,sigma = smooth_spex(data,z)
  fig = pylab.figure()
  ax = fig.add_subplot(111)
  if z is not None:
    ws = w/(1+z)
  else:
    ws = w
  ax.set_xlabel(r"$\mathrm{Rest\ wavelength}\ (\AA)$", size=14)
  ax.set_ylabel(r"$\mathrm{Normalised\ flux}$", size=14)
  ax.set_ylim([1.0e-5, 1.0])

  ax.plot(ws, f / f.max(), color='k', alpha=0.5)

  ax.plot(xpred, mean, color='red')
  ax.fill_between(xpred, mean - sigma,
                  mean + sigma, alpha=0.3, color='red')

  pylab.yscale('log')
  pylab.show()
  outfile = infile.rstrip(".fits") + "-smooth.dat"
  with open(outfile,'w') as fh:
    for x,y,z in zip(xpred,mean,sigma):
      print(x,y,z,file=fh)
      
