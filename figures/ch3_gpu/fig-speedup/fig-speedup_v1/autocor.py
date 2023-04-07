#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys

from statsmodels.tsa.stattools import acf

def next_pow_two(n):
    i = 1
    while i < n:
        i = i << 1
    return i

def autocorr_func_1d(x, norm=True):
    x = np.atleast_1d(x)
    if len(x.shape) != 1:
        raise ValueError("invalid dimensions for 1D autocorrelation function")
    n = next_pow_two(len(x))

    # Compute the FFT and then (from that) the auto-correlation function
    f = np.fft.fft(x - np.mean(x), n=2*n)
    acf = np.fft.ifft(f * np.conjugate(f))[:len(x)].real
    acf /= 4*n
    
    # Optionally normalize
    if norm:
        acf /= acf[0]

    return acf

# Automated windowing procedure following Sokal (1989)
def auto_window(taus, c):
    m = np.arange(len(taus)) < c * taus
    if np.any(m):
        return np.argmin(m)
    return len(taus) - 1

# Following the suggestion from Goodman & Weare (2010)
#def autocorr_gw2010(y, c=5.0):
#    f = autocorr_func_1d(np.mean(y, axis=0))
#    taus = 2.0*np.cumsum(f)-1.0
#    window = auto_window(taus, c)
#    return taus[window]

def autocorr_new(y, c=5.0):
    f = np.zeros(len(y))
    f += autocorr_func_1d(y)
    taus = 2.0*np.cumsum(f)-1.0
    window = auto_window(taus, c)
    return taus[window]

filename='ESpaced.out'
data = np.loadtxt(filename, skiprows=1)
Nmca   = data[:, 0].astype(int)
coresp = data[:, 1].astype(int)
etot   = data[:, 2] 

# read Time/MCStepinSec from result.out and use to calc time array
tperMCstep = 0
with open("result.out") as f:
  tperMCstep = float(f.readlines()[1].split(' ')[1])
#print(tperMCstep)
tym    = coresp*tperMCstep
Nmca_orig = Nmca
etot_orig = etot
tym_orig  = tym

# check for errors
try:
	len(etot)
except TypeError:
	print("Single line ESpaced.out; exiting")
	sys.exit(1)
Npts = len(etot) # number of points in the energy file
if Npts < 5:
	print("There are less than 5 lines in ESpaced.out; exiting")
	sys.exit(1)

Nmc = Nmca[1] # number of MC moves per data point in file
Ncut = int(0.5*Npts) # cutoff to drop data that is still relaxing

etot = etot[Ncut:]
if len(np.unique(etot)) == 1:
#  print("scream")
  f = open("autocorr_result.out","w+")
  f.write("AutoCorrelationTime inf inf inf inf\n")
  f.write("R2 0 0 0 0\n")
  f.write("Emean " + "0.0" + " " + "0.0" + " " + "0.0" + " " + str(etot[0]) + "\n")
  f.write("num_ind_points " + str(1) +  " " + str(1) + " " + str(1) + " " + str(1) + "\n")
  f.write("Ese " + str(0) + " " + str(0) + " " + str(0) + " " + str(0) + "\n")
  f.write("Convergence_crit " + str(1) + " " + str(1) + " " + str(1) + " " + str(1) + "\n")
  sys.exit()

Nmca = Nmca[:Npts-Ncut]
coresp = coresp[:Npts-Ncut]

minuss = tym[Ncut]
tym = tym[Ncut:]-minuss

#calculate it for pair, bond, angle and total

theta_tot = autocorr_new(etot)
theta_MC_tot = Nmca[int(np.ceil(theta_tot))]
theta_act_tot = coresp[int(np.ceil(theta_tot))]
theta_tym_tot = tym[int(np.ceil(theta_tot))]

skip = int(np.ceil(theta_MC_tot/Nmc))
Eforavg_tot = []
for i in range(int(len(etot)/skip)):
  Eforavg_tot.append(etot[i*skip])
Eforavg_tot = np.asarray(Eforavg_tot)
Emean_tot = np.mean(Eforavg_tot)
Ese_tot = np.std(Eforavg_tot)/float(np.sqrt(len(Eforavg_tot)))

#plot total energy
# create figure and axis objects with subplots()
fig,ax = plt.subplots(constrained_layout=True)

ax.plot(Nmca_orig, etot_orig, label='tot', color="g", marker=".")
ax.hlines(Emean_tot,Nmca[0],Nmca[-1],colors='g',linestyles='dotted')
ax.hlines(Emean_tot+2.0*Ese_tot,Nmca[0],Nmca[-1],colors='g',linestyles='dotted')
ax.hlines(Emean_tot-2.0*Ese_tot,Nmca[0],Nmca[-1],colors='g',linestyles='dotted')
ax.set_xlabel('MC move', color="g")
ax.tick_params(axis='x', colors='g')
ax.set_ylabel('E(t)')
#ax.ticklabel_format(axis='y', style='sci')
import matplotlib.ticker as mtick
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))

## twin object for two different y-axis on the sample plot
#ax2=ax.twinx()
#ax2.plot(tym_orig, etot_orig, label='tot', color="blue", marker="o")
#ax2.set_xlabel('time (sec)', color="blue")

idx_xticks = [ np.abs(Nmca_orig-xx).argmin() for xx in ax.get_xticks() ]
idx_xticks = np.unique(idx_xticks)
#print(idx_xticks)
#print([ np.abs(Nmca_orig-2000).argmin() ])
secax = ax.secondary_xaxis('top')
secax.set_xticks(Nmca_orig[idx_xticks])
secax.set_xticklabels([ round(tt, 2) for tt in tym_orig[idx_xticks] ])
secax.set_xlabel('time (sec)', color="r")
secax.tick_params(axis='x', colors='r')

ax.autoscale(enable=False, axis='both')
y2 = ax.get_yticks()[1]
y1 = (ax.get_yticks()[0]+y2)/2
y  = (y1+y2)/2
x1 = ax.get_xticks()[-4]
#x2 = ax.get_xticks()[-3]
x2 = ax.get_xticks()[-4]+theta_MC_tot
x  = (x1+x2)/2
ax.vlines(x1, y1, y2)
ax.vlines(x2, y1, y2)
from matplotlib.patches import FancyArrowPatch
myArrow = FancyArrowPatch(posA=(x1, y), posB=(x2, y), arrowstyle='<|-|>', color='0.5',
                          mutation_scale=20, shrinkA=0, shrinkB=0)
ax.add_artist(myArrow)
ax.text(0.7*x+0.3*x1, y2+0.01*abs(y2), str(round(theta_tym_tot,2))+" secs")
ax.text(0.7*x+0.3*x1, y2+0.005*abs(y2), str(round(theta_MC_tot,2))+" sweeps")

# save the plot as a file
fig.savefig('Energy_plot.png')
plt.close()

#using statmodel's acf function as constant sanity check and to produce a metric for convergence.
acf_tot = acf(etot, fft="false")
last_stuff = acf_tot[-10:]
conv_tot = np.mean(last_stuff)
np.savetxt("acf.out", acf_tot)
num_tot = np.arange(len(acf_tot))
plt.plot(num_tot, acf_tot)
plt.savefig("acf.png");

f = open("autocorr_result.out","w+")
f.write("AutoCorrelationTime 0.0 0.0 0.0 " + str(theta_tym_tot) + "\n")
f.write("R2 0 0 0 0\n")
f.write("Emean 0.0 0.0 0.0 " + str(Emean_tot) + "\n")
f.write("num_ind_points 0 0 0 " + str(len(Eforavg_tot)) + "\n")
f.write("Ese 0.0 0.0 0.0 " + str(Ese_tot) + "\n")
f.write("Convergence_crit 0.0 0.0 0.0 " + str(conv_tot) + "\n")

# lets explore this later
#from statsmodels.graphics.tsaplots import plot_acf
#from statsmodels.graphics.tsaplots import plot_pacf
#fig = plt.figure()
#ax = fig.add_subplot(111)
##plot_acf(etot_orig, ax=ax, lags=60, label='all')
#plot_acf(etot, ax=ax, lags=60, label='acf')
#plot_pacf(etot, ax=ax, lags=60, label='pacf')
#plt.legend()
#plt.show()
