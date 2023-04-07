#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Tue June 07 01:41:00 2022

@author: pierrekawak
"""
import numpy as np
import matplotlib.pyplot as plt

def LJ(r, eps=1, sigma=1, rc=2.5):
  if rc > 2.5:
    return(0)
  return( 4 * eps * ( (sigma/r)**12 - (sigma/r)**6 ) )

def LJfast(r, eps=1, sigma=1, rc=2.5):
  ratio = sigma/r
  ratio = ratio**6
  return( 4 * eps * ( ratio**2 - ratio ) )

xlim1 = 0.78
xlim2 = 1.22

# WCA params
sigma   = 2**(-1/6)
rc      = 2.5
eps     = 1
rij_min = 0.5
rij_max = 3.0
# WCA potential
rij   = np.linspace(rij_min, rij_max, 1000)
U_WCA = np.asarray([ 99999 if r <= 0.5*sigma else LJfast(r, eps, sigma, rc)+eps if r <= 2**(1/6)*sigma else 0 for r in rij ])
# Harm stretching params
l_0 = 1
eps = 600
li_min = 0.8
li_max = 1.2
# harm stretching potential
li   = np.linspace(li_min, li_max, 1001)
U_harm  = eps/2*(li-l_0)**2

test = 0
# plot all U
fig, ax = plt.subplots(1, figsize=(3.00,2.00), constrained_layout=test)
ax.plot(rij, U_WCA, label=r"$U_{\mathrm{pair}}^{\mathrm{WCA}}\ \left(\sigma=2^{-1/6}a\right)$", ls='--')
ax.plot(li, U_harm, label=r"$U_{\mathrm{stretch}}^{\mathrm{harm}}\ \left(l_{0}=a\right)$")#, ls='--')

xticks = [ sigma, l_0 ]
xticklabels = [ r"$2^{-1/6}$", "1" ]
yticks = [ 0, 2, 4, 6, 8, 10 ]
ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels)
ax.set_yticks(yticks)
ax.set_xlabel(r"$r_{ij}\ [a]$", fontsize=10, labelpad=-3.5)
ax.xaxis.set_label_coords(0.93, -0.04)
ax.set_ylabel(r"$U\ [\epsilon]$", fontsize=10, labelpad=-1)

ax.set_xlim(xlim1, xlim2)
ax.set_ylim(0-0.2, 10+1.0)

ax.legend(loc='best', ncol=1, fontsize=10, frameon=True, borderpad=0.5, markerfirst=True, handlelength=1.5, handletextpad=0.5)
ax.tick_params(axis='x', labelsize=10, pad=3)
ax.tick_params(axis='y', labelsize=10, pad=0)
if test == 0:
  plt.subplots_adjust(left=0.117, top=0.998, bottom=0.110, right=0.998)
#  plt.subplots_adjust(left=0.138, top=0.999, bottom=0.095, right=0.948)

plt.savefig("fig-WCA_vs_harmStretch.pdf")
plt.close()
