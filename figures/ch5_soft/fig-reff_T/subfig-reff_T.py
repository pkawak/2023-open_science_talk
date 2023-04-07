#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Sat June 22 08:41:00 2022

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

def WCA(r, eps=1.0, sig=2**(-1/6), rc=1.0):
  if r > rc:
    return(0)
  sigbyr6 = sig/r
  sigbyr6 = sigbyr6**6
  return(4*eps*(sigbyr6**2 - sigbyr6) + eps)

def return_reff_diff(reff, T, eps=1.0):
  target = 1.0*T
  return(WCA(reff) - target)

a_nom = 1
T_min = 0.00001
T_max = 1.0
T    = np.linspace(T_min, T_max, 1000)
a_eff = a_nom * [ fsolve(return_reff_diff, 0.8, args=(Ti))[0] for Ti in T ]

test = 0
fig, ax = plt.subplots(1, 1, figsize=(2.5,3.0), constrained_layout=test)
ax.plot([T_min, T_max], [a_nom, a_nom], label='Hard beads')
ax.plot(T, a_eff, label='Soft beads')
#plt.hlines(2**(-1/6), np.amin(T), np.amax(T))
#plt.hlines(1.0, np.amin(T), np.amax(T))

ax.set_xlabel(r"$k_{B}T$", fontsize=12, labelpad=-2)#, labelpad=0.3)
ax.set_ylabel(r"$\sigma_{\mathrm{eff}}/\sigma_{\mathrm{Hard}}$", fontsize=12, labelpad=-6)
ax.tick_params(axis='both', labelsize=10, pad=0)
ax.set_xticks([0.0, 1.0])
ax.set_yticks([1.0, 0.9])
#ax.set_xlim(T_min-0.004, T_max)
#ax.set_ylim(phi_min, phi_max)
ax.legend(loc='lower left')

#plt.subplots_adjust(left=0.156, top=0.98, bottom=0.135, right=0.974)
if test == 0:
  plt.subplots_adjust(left=0.142, top=0.996, bottom=0.103, right=0.996)
#plt.show()
#sys.exit()
plt.savefig("subfig-reff_T.pdf")
plt.close()
