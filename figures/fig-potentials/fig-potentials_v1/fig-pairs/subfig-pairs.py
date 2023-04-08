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

# plot all U
fig, ax = plt.subplots(1, figsize=(2.167,3.000), constrained_layout=True)
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
ax.set_ylim(-1.5*eps, 10*eps+1.0*eps)

#ax.legend(loc='best', fontsize=10)
#(0.600,0.665)
ax.legend(loc='best', fontsize=9, frameon=True, borderpad=0.5, markerfirst=True, handlelength=1.5, handletextpad=0.5)
ax.set_xlabel(r"$r_{ij}$", fontsize=10, labelpad=-6)
ax.set_ylabel(r"$U_{\mathrm{pair}}$", fontsize=10, labelpad=-12)
ax.tick_params(axis='both', labelsize=8)
#plt.subplots_adjust(left=0.175, top=0.99, bottom=0.28, right=0.99)
#plt.show()
plt.savefig("subfig-pairs.pdf")
plt.close()
