#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Fri May 13 01:41:00 2022

@author: pierrekawak
"""
import numpy as np
import matplotlib.pyplot as plt

l_0 = 1
eps = 600

li_min = 0.8
li_max = 1.2

li   = np.linspace(li_min, li_max, 1001)
U_tang  = np.asarray([ 99999 if r != l_0 else 0 for r in li ])
U_harm  = eps/2*(li-l_0)**2

tenkt_tang  = np.argmin(np.abs(U_tang-10))
tenkt_harm = np.argmin(np.abs(U_harm-10))

# plot all U
fig, ax = plt.subplots(1, figsize=(2.167,3.000), constrained_layout=True)
ax.plot(li, U_tang, label=r"$U^{\mathrm{rod}}$")#, ls='-' )
ax.plot(li, U_harm, label=r"$U^{\mathrm{harm}}$")#, ls='--')

xticklabels = [ r"$l_{0}$", r"$0.8l_{0}$", r"$1.2l_{0}$" ]# r"$\frac{4l_{0}}{5}$", r"$\frac{6l_{0}}{5}$"]
xticks      = [ l_0       , 0.8*l_0       ,  1.2*l_0       ]
ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels)

yticklabels = [ r"$0$", r"$10kT$" ]
yticks      = [ 0     , 10        ]
ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)

ax.set_xlim(li_min, li_max)
ax.set_ylim(0, 10+1.0)

#ax.legend(loc='best', fontsize=10)
ax.legend(loc=(0.09,0.81), fontsize=9, frameon=True, borderpad=0.5, markerfirst=True, handlelength=0.7, handletextpad=0.5)
ax.set_xlabel(r"$l_{i}$", fontsize=10, labelpad=-3)
ax.xaxis.set_label_coords(.7, -.05)
ax.set_ylabel(r"$U_{\mathrm{bond}}$", fontsize=10, labelpad=-12)
ax.tick_params(axis='both', labelsize=8)
#plt.subplots_adjust(left=0.175, top=0.99, bottom=0.28, right=0.99)
#plt.show()
plt.savefig("subfig-bonds.pdf")
plt.close()
