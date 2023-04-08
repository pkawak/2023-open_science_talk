#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Fri May 13 01:41:00 2022

@author: pierrekawak
"""
import numpy as np
import matplotlib.pyplot as plt

costs = 0.9
eps   = 1.0

ti_min = 0.0
ti_max = np.pi

ti     = np.linspace(ti_min, ti_max, 1001)
costi  = np.cos(ti)
U_step = np.asarray([ -eps if r >= costs else 0 for r in costi ])
U_harm = eps*(1-costi)-eps

tenkt_step  = np.argmin(np.abs(U_step-10))
tenkt_harm = np.argmin(np.abs(U_harm-10))

# plot all U
fig, ax = plt.subplots(1, figsize=(2.167,3.000), constrained_layout=True)
ax.plot(ti, U_step, label=r"$U^{\mathrm{step}}$")#, ls='-' )
ax.plot(ti, U_harm, label=r"$U^{\mathrm{harm}}-k_{b}$")#, ls='--')

xticklabels = [ r"$0$", r"$\theta_{s}$" , r"$\pi$" ]
xticks      = [ 0     , np.arccos(costs), np.pi    ]
ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels)

yticklabels = [ r"$-k_{b}$", r"$k_{b}$" ] #, r"$0$" ]
yticks      = [ -1*eps        , eps           ] #, 0      ]
ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)

ax.set_xlim(ti_min, ti_max)
ax.set_ylim(-1-0.05, 1+0.05)

#ax.legend(loc='best', fontsize=10)
ax.legend(loc='best', fontsize=9, frameon=True, borderpad=0.5, markerfirst=True, handlelength=0.7, handletextpad=0.5)
ax.set_xlabel(r"$\theta_{i}$", fontsize=10, labelpad=-8)
#ax.xaxis.set_label_coords(.7, -.05)
ax.set_ylabel(r"$U_{\mathrm{bend}}$", fontsize=10, labelpad=-12)
ax.tick_params(axis='both', labelsize=8)
#plt.subplots_adjust(left=0.175, top=0.99, bottom=0.28, right=0.99)
#plt.show()
plt.savefig("subfig-angles.pdf")
plt.close()
