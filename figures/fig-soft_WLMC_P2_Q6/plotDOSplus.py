#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 17:32:10 2019

@author: pierrekawak
"""
#--------------------------------------------
#THIS FILE PLOTS COMMON THERMODYNAMIC DISTROS GIVEN A PARAMS.DAT FILE AND A LNG.OUT FILE
#IT ALSO OUTPUTS THE CANONICAL DISTRO AND THE POTENTIAL ENERGY AT GIVEN TEMPERATURE RANGE
#--------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import gmpy2
from gmpy2 import mpfr
import scipy.signal
import json
import os
import sys

data = np.loadtxt('lng.out', skiprows=1, dtype=object)
E    = [ mpfr(i) for i in data[:, 0].tolist() ]
lng  = [ mpfr(i) for i in data[:, 1].tolist() ]
E    = np.asarray(E)
lng  = np.asarray(lng)

minlng   = np.amin(lng)
lng_norm = lng - minlng 
g_norm   = np.asarray( [ gmpy2.exp(i) for i in lng_norm.tolist() ] )

num_plot = 2
plt.subplot(num_plot,1,1)
plt.plot(E, lng_norm)                          
plt.xlabel('E')
plt.ylabel('lng(E)')

q6_dat = np.loadtxt("EvQ6.out", delimiter=" ", usecols=1)
P2_dat = np.loadtxt("EvP2.out", delimiter=" ", usecols=1)
clust_dat = np.loadtxt("Evclust.out", delimiter=" ", usecols=1)
endDist_dat = np.loadtxt("EvendDist.out", delimiter=" ", usecols=1)
gyrDist_dat = np.loadtxt("EvgyrDist.out", delimiter=" ", usecols=1)
MS_dat = np.loadtxt("EvMS.out", delimiter=" ", usecols=1)
op_dat = [ q6_dat, P2_dat, clust_dat, endDist_dat, gyrDist_dat, MS_dat ]
op_name = [r"$Q_{6}$", r"$P_{2}$", r"$n_{Q_{6}}$", r"$R^{2}_{e}$", r"$R^{2}_{g}$", r"$S_{MS}$" ]
op_num = len(op_dat)
#--------------------------------------------
#DEFINE TEMPERATURE HERE
lowT = 0.05
highT = 5.0
NumPoints = 1000
if os.path.isfile("t_range.json"):
  with open("t_range.json") as f:
    data = json.load(f)
  lowT = data["lowT"]
  highT = data["highT"]
  if "NumPoints" in data:
    NumPoints = data["NumPoints"]
#--------------------------------------------
T = np.linspace(lowT,highT,NumPoints)
U = []
heat_cap = []
numer = []
numer_Esq = []
denom = []
op=[ [] for i in range(op_num) ]
numer_op=[ [] for i in range(op_num) ]
Eg = E*g_norm

#print("lng:", len(lng))
#print("ops:", len(op_dat[0]))
#sys.exit()
for i in range(NumPoints):
  numer.append(mpfr(0.))
  numer_Esq.append(mpfr(0.))
  for ii in range(op_num):
    op[ii].append(mpfr(0.))
    numer_op[ii].append(mpfr(0.))
  denom.append(mpfr(0.))
  U.append(mpfr(0.))
  heat_cap.append(mpfr(0.))
  for j in range(len(lng)):
    E_T_ratio = mpfr(-E[j]/T[i])
    exp_E_T_ratio = gmpy2.exp(E_T_ratio)
    g_norm_exp = exp_E_T_ratio * mpfr(g_norm[j])
    numer[i] += mpfr(E[j])*g_norm_exp
    numer_Esq[i] += mpfr(E[j]**2.)*g_norm_exp 
    for ii in range(op_num):
      numer_op[ii][i] += mpfr(op_dat[ii][j])*g_norm_exp
    denom[i] += g_norm_exp
  U[i]=numer[i]/denom[i]
  heat_cap[i] = (numer_Esq[i]/denom[i] - U[i]**2.) / T[i]**2.
  for ii in range(op_num):
    op[ii][i] = numer_op[ii][i]/denom[i]

from math import log10, floor
def round_sig(x, sig=2):
   return round(x, sig-int(floor(log10(abs(x))))-1)

plt.subplot(num_plot,1,2)
plt.plot(T,U)
plt.xlabel('kT')
plt.ylabel('U(T)')

plt.savefig('lng_plot.png',dpi=600)
plt.close()

heat_cap_norm = np.asarray(heat_cap, dtype=np.float64)
peaks = scipy.signal.find_peaks(heat_cap_norm)
peak_strength = scipy.signal.peak_prominences(heat_cap_norm, peaks[0])[0]
print("Ts, Peak Strengths and Energies: ")
peakTs = T[peaks[0]]
peakUs = np.array(U)[peaks[0]].astype('float64')
#[ print(t, p, u)  for t,p,u in zip(peakTs, peak_strength, peakUs) ]
#uncomment to filter out peaks under filterT
filterT = 0.05*(highT-lowT)+lowT
filter_ids = [ 0 if i < filterT else 1 for i in peakTs ]
peakTs = np.array([ i for i, f in zip(peakTs, filter_ids) if f == 1 ])
peaks = np.array([ i for i, f in zip(peaks[0], filter_ids) if f == 1 ])
peakUs = np.array([ i for i, f in zip(peakUs, filter_ids) if f == 1 ])
peak_strength = np.array([ i for i, f in zip(peak_strength, filter_ids) if f == 1 ])
sorted_idx = np.argsort(peak_strength)
sorted_peakTs = peakTs[sorted_idx]
sorted_peakUs = peakUs[sorted_idx]
sorted_peak_strength = peak_strength[sorted_idx]
[ print(t, p, u)  for t,p,u in zip(sorted_peakTs, sorted_peak_strength, sorted_peakUs) ]
#print(*T[peaks[0]], sep = " ")
#print(*peak_strength, sep = " ")
#print(*np.array(U)[peaks[0]], sep = " ")

fig = plt.gcf()
ax = plt.subplot(211)
ax.set_xlabel('kT', fontsize=10)
ax.set_ylabel('C(T)', fontsize=10)
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#fig.set_size_inches(2,2, forward=True)
#for peak in peaks[0]:
#  ax.text(T[peak], 0.1, '%.3f' % (T[peak]), fontsize=8, ha='center')
#  ax.vlines(T[peak], 0, heat_cap_norm[peak], linestyles='dashed')
ax.plot(T, heat_cap_norm.tolist())
ax.set_yscale("log")
ax = plt.subplot(212)
ax.set_xlabel('kT', fontsize=10)
ax.set_ylabel('C(T)', fontsize=10)
ax.plot(T, heat_cap_norm.tolist())
plt.tight_layout()
fig.savefig('CvT.png', dpi=900)
plt.close()

fig, ax = plt.subplots()
ax.set_xlabel('kT', fontsize=10)
ax.set_ylabel('U(T)', fontsize=10)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#fig.set_size_inches(2,2, forward=True)
#for peak in peaks[0]:
#  ax.vlines(T[peak], U[0], U[peak], linestyles='dashed')
ax.plot(T, U)
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
only_first = max(int(0.03*len(T)), 10)
ax2 = plt.axes([0,0,1,1])
ip = InsetPosition(ax2, [0.4,0.2,0.5,0.5])
ax2.set_axes_locator(ip)
#mark_inset(ax, ax2, loc1=2, loc2=4, fc="none", ec='0.5')
ax2.plot(T[:only_first], U[:only_first])
#plt.subplots_adjust(left=0.3, right=0.96, bottom=0.25, top=0.89)
#plt.tight_layout()
fig.savefig('UvT.png', dpi=900)
plt.close()

conc = np.c_[T, U, heat_cap_norm]
np.savetxt('canon_distro.out', conc)
for i in range(op_num):
  conc = np.c_[conc, op[i]]
np.savetxt('ext_canon_distro.out', conc)

plt.rcParams['font.size'] = '12'
howmany_peaks_label = min(5, len(sorted_peakTs))
fig, axs = plt.subplots(4, 2, sharex=True, figsize=(12, 10), constrained_layout=True)
for ii in range(op_num):
  iii = ii%4
  iij = int(ii/4)
  axs[iii][iij].set_ylabel(op_name[ii], rotation=0, labelpad=10)
  axs[iii][iij].plot(T, op[ii])
  axs[iii][iij].plot(T, (heat_cap_norm-np.amin(heat_cap_norm))*(np.amax(op[ii])-np.amin(op[ii]))/(np.amax(heat_cap_norm)-np.amin(heat_cap_norm))+np.amin(op[ii]), alpha=0.3)
  axs[iii][iij].plot(T, (np.array(op[1])-np.amin(op[1]))*(np.amax(op[ii])-np.amin(op[ii]))/(np.amax(op[1])-np.amin(op[1]))+np.amin(op[ii]), alpha=0.3)
  ylim = axs[iii][iij].get_ylim()
  axs[iii][iij].set_ylim(ylim)
  if howmany_peaks_label:
    sorted_peakOpii = np.array(op[ii])[peaks][sorted_idx].astype('float64')
    for i in range(howmany_peaks_label):
      axs[iii][iij].vlines(sorted_peakTs[-1-i], 0, sorted_peakOpii[-1-i], linestyles='dashed')

print("Sanity check, these two shouldn't be too different. Minimum U in solution:", min(U), "Minimum U studied:", E[0], "What about other side:", max(U), "and", E[-1])
axs[op_num%4][1].set_ylabel('U', rotation=0, labelpad=10)
axs[op_num%4][1].plot(T, U)
axs[op_num%4][1].plot(T, (heat_cap_norm-np.amin(heat_cap_norm))*(np.amax(U)-np.amin(U))/(np.amax(heat_cap_norm)-np.amin(heat_cap_norm))+np.amin(U), alpha=0.3)
axs[op_num%4][1].plot(T, (np.array(op[1])-np.amin(op[1]))*(np.amax(U)-np.amin(U))/(np.amax(op[1])-np.amin(op[1]))+np.amin(U), alpha=0.3)
ylim = axs[op_num%4][1].get_ylim()
axs[op_num%4][1].set_ylim(ylim)
for i in range(howmany_peaks_label):
  axs[op_num%4][1].vlines(sorted_peakTs[-1-i], 0, sorted_peakUs[-1-i], linestyles='dashed')

axs[op_num%4+1][1].set_xlabel('kT')
axs[op_num%4+1][0].set_xlabel('kT')
axs[op_num%4+1][1].set_ylabel(r'$C_v$', rotation=0, labelpad=10)
axs[op_num%4+1][1].set_yscale("log")
axs[op_num%4+1][1].plot(T, heat_cap_norm.tolist())
#axs[op_num%4+1][1].plot(T, heat_cap_norm*np.amax(U)/np.amax(heat_cap_norm), alpha=0.3)
axs[op_num%4+1][1].plot(T, (np.array(op[1])-np.amin(op[1]))*(np.amax(heat_cap_norm)-np.amin(heat_cap_norm))/(np.amax(op[1])-np.amin(op[1]))+np.amin(heat_cap_norm), alpha=0.3)
ylim = axs[op_num%4+1][1].get_ylim()
axs[op_num%4+1][1].set_ylim(ylim)
if howmany_peaks_label:
  yy=80
  sorted_peakCvs = heat_cap_norm[peaks][sorted_idx].astype('float64')
  for i in range(howmany_peaks_label):
    axs[op_num%4+1][1].text(sorted_peakTs[-1-i], yy, '%.3f' % (sorted_peakTs[-1-i]), fontsize=7)
    axs[op_num%4+1][1].vlines(sorted_peakTs[-1-i], 0, sorted_peakCvs[-1-i], linestyles='dashed')
    yy+=10
#plt.subplots_adjust(left=0.2, bottom=0.08, right=0.95, top=0.97, wspace=None, hspace=None)
#plt.tight_layout()
#plt.show()
plt.savefig("canon_anal.pdf")
#plt.close()

##computing probability at any T
##get lowest and highest energy
#Evals = np.loadtxt("EvQ6.out", delimiter=" ", usecols=0)
#maxE = max(Evals)
#minE = min(Evals)
#
#Prob = np.zeros(len(E))
#
##choose your T
#Tchoice = 0.526
#idx = (np.abs(T - Tchoice)).argmin()
#
##compute the probability distro
#for j in range(len(E)):
#    E_T_ratio = mpfr(-E[j]/T[idx])
#    exp_E_T_ratio = gmpy2.exp(E_T_ratio)
#    g_norm_exp = exp_E_T_ratio * mpfr(g_norm[j])
#    Prob[j] = g_norm_exp / denom[idx]
#
#fig = plt.gcf()
#plt.subplot(num_plot,1,1)
#plt.plot(E, Prob)                          
#plt.xlabel('E')
#plt.ylabel('P(E, T)')
#fig.savefig('Prob.png', dpi=900)
#plt.close()
