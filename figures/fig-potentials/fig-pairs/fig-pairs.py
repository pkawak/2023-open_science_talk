#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Fri May 13 01:41:00 2022

@author: pierrekawak
"""
import numpy as np
import matplotlib.pyplot as plt

sigma   = 1
rc      = 2.5
eps     = 1

rij_min = 0.5
rij_max = 3.0

def LJ(r, eps=1, sigma=1, rc=2.5):
  if rc > 2.5:
    return(0)
  return( 4 * eps * ( (sigma/r)**12 - (sigma/r)**6 ) )

def LJfast(r, eps=1, sigma=1, rc=2.5):
  ratio = sigma/r
  ratio = ratio**6
  return( 4 * eps * ( ratio**2 - ratio ) )

rij   = np.linspace(rij_min, rij_max, 1000)
U_HS  = np.asarray([ 99999 if r <= sigma else 0 for r in rij ])
U_SW  = np.asarray([ 99999 if r <= sigma else -eps if r <= rc else 0 for r in rij ])
U_LJ  = np.asarray([ 99999 if r <= 0.5*sigma else LJfast(r, eps, sigma, rc) if r <= rc else 0 for r in rij ])
U_WCA = np.asarray([ 99999 if r <= 0.5*sigma else LJfast(r, eps, sigma, rc)+eps if r <= 2**(1/6)*sigma else 0 for r in rij ])

tenkt_LJ  = np.argmin(np.abs(U_LJ-10*eps))
tenkt_WCA = np.argmin(np.abs(U_WCA-10*eps))

test = 0
# plot all U
fig, ax = plt.subplots(1, figsize=(3.800,3.000), constrained_layout=test)
ax.plot(rij, U_HS , label=r"$U^{\mathrm{HS}}$" , ls='-' )
ax.plot(rij, U_SW , label=r"$U^{\mathrm{SW}}$" , ls=':' )
ax.plot(rij, U_LJ , label=r"$U^{\mathrm{LJ}}$" , ls='-.')
ax.plot(rij, U_WCA, label=r"$U^{\mathrm{WCA}}$", ls='--')

xticklabels = [ r"$0.7\sigma$", r"$\sigma$", r"$r_{c}$" ]#, r"$0.78\sigma$"]
xticks      = [ 0.7*sigma     , sigma      , rc         ]#, 0.78*sigma     ]
ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels)

yticklabels = [ r"$-\epsilon$", r"$0$", r"$10\epsilon$" ]
yticks      = [ -eps          , 0     , 10*eps    ]
ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)

ax.set_xlim(0.7, 2.8)
ax.set_ylim(-1.5*eps, 10*eps+1.5*eps)

ax.legend(loc='best', ncol=2, fontsize=12, frameon=True, borderpad=0.5, markerfirst=True, handlelength=1.5, handletextpad=0.5)
ax.set_xlabel(r"$r_{ij}$", fontsize=12, labelpad=-3.5)
ax.set_ylabel(r"$U_{\mathrm{pair}}$", fontsize=12, labelpad=-12)
ax.tick_params(axis='both', labelsize=12, pad=0)
if test == 0:
  plt.subplots_adjust(left=0.100, top=0.999, bottom=0.106, right=0.999)

# inset zoomed in on sigma
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
#ax3 = plt.axes([0,0,1.3,0.8])
#ip = InsetPosition(ax3, [0.15,0.17,0.7,0.75])
#ax3.set_axes_locator(ip)
#mark_inset(ax, ax3, loc1=2, loc2=4, fc='none', ec='0.5')
##ax3.plot(sweeps_orig[rangel:rangeh], etot_orig[rangel:rangeh], color='blue')
##ax3.hlines(Emean_tot, ax3.set_xlim()[0], ax3.set_xlim()[1], colors='black', linestyles='--', zorder=2, label=r'$\mu(U)$')
ax3 = ax.inset_axes([0.41, 0.22, 0.56, 0.50])
ax3.plot(rij, U_HS , label=r"$U^{\mathrm{HS}}$" , ls='-' )
ax3.plot(rij, U_SW , label=r"$U^{\mathrm{SW}}$" , ls=':' )
ax3.plot(rij, U_LJ , label=r"$U^{\mathrm{LJ}}$" , ls='-.')
ax3.plot(rij, U_WCA, label=r"$U^{\mathrm{WCA}}$", ls='--')
x1, x2, y1, y2 = sigma-0.05, sigma+0.3, -eps-0.1, 2*eps+0.1
xticklabels = [ r"$0.7\sigma$", r"$\sigma$", r"$2^{1/6}\sigma$" ]#, r"$0.78\sigma$"]
xticks      = [ 0.7*sigma     , sigma      , 2**(1/6)*sigma         ]#, 0.78*sigma     ]
ax3.set_xticks(xticks)
ax3.set_xticklabels(xticklabels)
yticklabels = [ r"$-\epsilon$", r"$0$", r"$2\epsilon$" ]
yticks      = [ -eps          , 0     , 2*eps    ]
ax3.set_yticks(yticks)
ax3.set_yticklabels(yticklabels)
ax3.set_xlim(x1, x2)
ax3.set_ylim(y1, y2)
ax3.set_facecolor('#0000001a')
ax3.tick_params(axis='both', labelsize=10, pad=0)
#ax.indicate_inset_zoom(ax3, edgecolor="black")

#plt.show()
plt.savefig("fig-pairs.pdf")
plt.close()
