import numpy as np
import ast
import pylab


def get_dict(file):
  with open(file,'r') as fh:
    data = fh.readline()
  data = data.replace("# ","")
  return ast.literal_eval(data)

def get_spect(file):
  w,f,e,fs = np.loadtxt(file,unpack=True)
  d = dict()
  d['wl'] = w
  d['fl'] = f
  d['err'] = e
  d['fls'] = fs
  return d

def gauss(x,mean,std):
  x = np.asarray(x)
  # amplitudes returned by misfits include normalization
  _ = np.exp(-0.5*((x-mean)/std)**2) # /(np.sqrt(2*np.pi)*std)
  return _
             
def flatten_list(l):
  r"""flatten a list of lists
  """
#
# I would do it this way, but it only works if every element is a list
#
#  flattened = [ x for subl in l for x in subl ]

  try:
    from collections.abc import Iterable  # noqa
  except ImportError:
    from collections import Iterable  # noqa

  def iterable(obj):
    return isinstance(obj, Iterable)

  flattened = []
  for sublist in l:
    if iterable(sublist):
      for val in sublist:
        flattened.append(val)
    else:
      flattened.append(sublist)  
  return flattened

def bold_labels(ax,fontsize=None):
  if fontsize is None:
    fontsize = 14
  for tick in ax.xaxis.get_major_ticks():
    tick.label1.set_fontsize(fontsize)
    tick.label1.set_fontweight('bold')
  for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(fontsize)
    tick.label1.set_fontweight('bold')


def plot_2col(args,window=1,xlab='x (units)',ylab='y (units)',lab=None,figprops={},adjustprops={}):
  """ 
  plot_2col(args,window=1,xlab='x (units)',ylab='y (units)',figprops={},adjustprops={}):
  Takes arguments args which is a tuple of the form (x1,y1,x2,y2,...)
  """
  import pylab
  from matplotlib.ticker import AutoMinorLocator
  pylab.interactive(True)

  # One can supply an argument to AutoMinorLocator to
  # specify a fixed number of minor intervals per major interval, e.g.:
  # minorLocator = AutoMinorLocator(2)
  # would lead to a single minor tick between major ticks.

  minorLocator   = AutoMinorLocator()

  golden = (pylab.sqrt(5)+1.)/2.

  if not figprops:
    figprops = dict(figsize=(8., 8./ golden ), dpi=128)    # Figure properties for single and stacked plots 
    # figprops = dict(figsize=(16., 8./golden), dpi=128)    # Figure properties for side by sides

  if not adjustprops:
      adjustprops = dict(left=0.15, bottom=0.15, right=0.90, top=0.93, wspace=0.2, hspace=0.2)       # Subp

  fig1 = pylab.figure(window,**figprops)   # New figure
  fig1.subplots_adjust(**adjustprops)  # Tunes the subplot layout
  fig1.clf()

  ax1 = fig1.add_subplot(1, 1, 1)

  bold_labels(ax1)

  if lab:
    ps = ax1.plot(*args,linewidth=2.0,label=lab)
  else:
    ps = ax1.plot(*args,linewidth=2.0)

  ax1.set_ylabel(ylab,fontsize=18)
  ax1.set_xlabel(xlab,fontsize=18)

  ax1.xaxis.set_minor_locator(minorLocator)

  pylab.tick_params(which='both', width=2)
  pylab.tick_params(which='major', length=7)
  pylab.tick_params(which='minor', length=4, color='r')
  
  ax1.xaxis.grid(True,which='both')
  return fig1,ax1,ps

def plot_gauss(d1,d2):
  """
   d1 is the misfits dictionary
   d2 is the spectrum dictionary
  """
  fig,ax,ps = plot_2col((d2['wl'],d2['fls']),xlab=r'$\lambda$ ($\AA$)',ylab=r'$F_\lambda$')
  return fig,ax,ps

if __name__ == '__main__':
  import pylab
  import numpy as np

  infile = input("Give misfits file: ")
  d1 = get_dict(infile)
  d2 = get_spect(infile)
  fig,ax,ps = plot_gauss(d1,d2)
  stds = flatten_list(d1['velocity.gaussians.stddevs'])
  x0s = flatten_list(d1['velocity.gaussians.x0s'])
  limits = d1['velocity.gaussians.limits']
  vnp = -2  
  conts = np.poly1d(d1['velocity.gaussians.continuum'][vnp])
  amps = flatten_list(d1['velocity.gaussians.amplitudes'])
  x_values = np.arange(limits[vnp][0],limits[vnp][1],0.1)
  y_values = conts(x_values)+amps[vnp]*gauss(x_values,x0s[vnp],stds[vnp])
  p1, = ax.plot(x_values,y_values)
  pylab.show()
  # conts = np.poly1d(d1['velocity.gaussians.continuum'][0])
  # amps = flatten_list(d1['velocity.gaussians.amplitudes'])
  # x_values = np.arange(limits[0][0],limits[0][1],0.1)
  # y_values = conts[1]+amps[0]*gauss(x_values,x0s[0],stds[0])
  # p1, = ax.plot(x_values,y_values)
  # pylab.show()
