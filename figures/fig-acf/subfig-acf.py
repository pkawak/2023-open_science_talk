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
        raise ValueError('invalid dimensions for 1D autocorrelation function')
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

filename='ESpaced.orig.out'
data = np.loadtxt(filename, skiprows=1)
sweeps = data[:, 0].astype(int)
time   = data[:, 10]
tries  = data[:, 1].astype(int)
etot   = data[:, 8] 
#
#num_points = 175
#skip_ = int(len(sweeps)/num_points)
#sweeps = np.asarray([ sweeps[i*skip_] for i in range(int(len(etot)/skip_)) ])
#time   = np.asarray([ time[i*skip_] for i in range(int(len(etot)/skip_)) ])
#tries  = np.asarray([ tries[i*skip_] for i in range(int(len(etot)/skip_)) ])
#etot   = np.asarray([ etot[i*skip_] for i in range(int(len(etot)/skip_)) ])

sweeps_orig = sweeps
etot_orig = etot
time_orig  = time

Nmc = sweeps[0] # number of MC moves per data point in file
Npts = len(etot) # number of points in the energy file
Ncut = int(0.5*Npts) # cutoff to drop data that is still relaxing

etot = etot[Ncut:]
sweeps = sweeps[:Npts-Ncut]
tries = tries[:Npts-Ncut]
minuss = time[Ncut]
time = time[Ncut:]-minuss

tau = autocorr_new(etot)
tau_sweeps = sweeps[int(np.ceil(tau))]
tau_tries = tries[int(np.ceil(tau))]
tau_time = time[int(np.ceil(tau))]

skip = int(np.ceil(tau_sweeps/Nmc))
Eforavg_tot = np.asarray([ etot[i*skip] for i in range(int(len(etot)/skip)) ])
Emean_tot = np.mean(Eforavg_tot)
Ese_tot = np.std(Eforavg_tot)/float(np.sqrt(len(Eforavg_tot)))

## plot total energy
#fig, ax = plt.subplots(figsize=(3.25,2.80), constrained_layout=True)
#ax.plot(sweeps_orig, etot_orig, label='U', color='blue', marker='o', zorder=1, linewidth=0.5, markersize=3)#, s=5)
## average and 2 standard error labeling
#ax.hlines(Emean_tot,             sweeps_orig[0], sweeps_orig[-1], colors='red', linestyles='-', zorder=2, label=r'$\mu(U)$')
#ax.hlines(Emean_tot+2.0*Ese_tot, sweeps_orig[0], sweeps_orig[-1], colors='red', linestyles='dotted', zorder=2, label=r'$\mu(U) \pm 2\sigma_{M}(U)$')
#ax.hlines(Emean_tot-2.0*Ese_tot, sweeps_orig[0], sweeps_orig[-1], colors='red', linestyles='dotted', zorder=2)
#from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition,
#                                                  mark_inset)
##ax3 = plt.axes([0,0,1,1])
##ip = InsetPosition(ax3, [0.1,0.25,0.7,0.7])
##ax3.set_axes_locator(ip)
##mark_inset(ax, ax3, loc1=2, loc2=4, fc='none', ec='0.5')
##rangel = 1150
###print(rangel)
##rangeh = rangel+20
##ax3.plot(sweeps_orig[rangel:rangeh], etot_orig[rangel:rangeh])
#
#ax.set_yticks([etot_orig[0], Emean_tot])
#ax.set_yticklabels([r"$U_{0}$", r"$\langle U\rangle$"])
#ax.set_xticks([])
#ax.set_xlabel('t (snapshot number)')
#ax.set_ylabel('U(t)')
##ax.legend(loc='best')
#fig.savefig('subfig-UvsNum.pdf')
#plt.close()

#using statmodel's acf function as constant sanity check and to produce a metric for convergence.
acf_tot = acf(etot, fft='false')
num_tot = np.arange(len(acf_tot))
ylim1 = min(0, np.amin(acf_tot))-0.03
ylim2 = 1+0.15
test = 0
fig, ax = plt.subplots(figsize=(2.25,2.80), constrained_layout=test)
ax.scatter(num_tot, acf_tot, color='b')
ax.vlines(tau, ylim1, ylim2, color='g', ls='--')#, label=r'$\tau=$'+str(int(tau))+'='+str(round(tau_time))+' seconds')
ax.plot(num_tot, np.exp(-num_tot/tau), color='r', label=r'$\exp\left(-\Delta t/\tau\right)$')
#if np.amin(acf_tot) < 0:
#  ax.hlines(0, 0, num_tot[-1], color='k', ls='--')
ax.set_xlabel(r'$\Delta t$', fontsize=10, labelpad=-5)
#ax.fill_between([num_tot[-1]-10, num_tot[-1]], min(0, np.amin(acf_tot)), 1, color='m', alpha=0.2)
#ax.set_ylabel(r'$\mathrm{acf}\left(\Delta t\right) = \mathrm{acf}\left(U\left(t+\Delta t\right), U\left(t\right)\right)$', fontsize=10, labelpad=5)
ax.set_ylabel(r'$\mathrm{acf}\left(\Delta t\right)$', fontsize=10, labelpad=-3)
ax.tick_params(axis='both', labelsize=10, pad=0)
ax.legend(loc='best', fontsize=10)
ax.set_ylim(ylim1, ylim2)
ax.set_xlim(0-0.1, 15)#num_tot[-1])
ax.set_yticks([0,1])
ax.set_xticks([tau])
ax.set_xticklabels([r'$\tau$'])
#ax.set_xlim(0, 20)#num_tot[-1])
#plt.show()
if test == 0:
  plt.subplots_adjust(left=0.106, bottom=0.076, right=0.995, top=0.998)
plt.savefig('subfig-acf.pdf');
plt.close()
