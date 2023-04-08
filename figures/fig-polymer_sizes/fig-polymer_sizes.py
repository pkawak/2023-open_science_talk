#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Sat June 02 08:41:00 2022

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import random

random.seed(718)
#random.seed(20)
dim = 2
Nb  = 20
Lx  = 10
l0  = 1.0 #bond length
sig = 1.0

def calculateDist(ri, rj):
  dr = [ (ri[i] - rj[i])**2 for i in range(len(ri)) ]
  return np.sum(dr)

def get_com(R):
  rmean = np.mean(R)

R = np.zeros(shape=(Nb, dim))
for nb in range(Nb):
  overlap = True;
  while overlap:
    overlap = False
    if nb == 0:
      origin = np.array([ (random.random()-0.5)*Lx for i in range(dim) ])
    else: 
      origin = np.array([ R[nb-1, i] for i in range(dim) ])
    theta = 2.*np.pi*(random.random());
    if dim == 2:
      new = np.array([ l0*np.cos(theta)+origin[0], l0*np.sin(theta)+origin[1] ])
    else:
      phi = np.arccos(2.*(random.random())-1.);
      new = np.array([ l0*np.cos(theta)*np.sin(phi)+origin[0], l0*np.sin(theta)*np.sin(phi)+origin[1], l0*np.cos(phi)+origin[2] ])
    # check overlaps
    for nb2 in range(nb-1):
      dr2 = calculateDist(new, R[nb2])
      if dr2 - sig**2 < 0.0-1e-6:
     #   print("overlap", dr2, sig**2, "this:", dr2-sig**2, nb, nb2, dr2)
        overlap = True
        break
  R[nb] = new
  print(nb, "accepted")
  for nb2 in range(nb):
    dr2 = calculateDist(new, R[nb2])
    print("dist:", nb, R[nb, 0], R[nb,1], nb2, R[nb2, 0], R[nb2, 1], dr2, dr2-sig**2)
  print()

#print(R)
#print(np.mean(R, axis=0))
Rmean = np.mean(R, axis=0)
R2g   = np.sum([ np.sum( (R[i] - Rmean)**2 ) for i in range(len(R)) ])/len(R)
Rg    = np.sqrt(R2g)
R2e   = np.sum( (R[0] - R[-1])**2 )
Re    = np.sqrt(R2e)

import matplotlib.colors as pltc
test = 0
chain_color = '#B96D40'
bead_color  = '#D039BF'
Re_color    = '#2D2E2E'
Rg_color    = '#296EB4'
fig, ax = plt.subplots(1, figsize=(5.0, 4.05), constrained_layout=True)
#plt.plot(T, -1/np.log(cosT), label=r"$\frac{-1}{\ln(\cos\theta)}$")
ax.plot(R[:, 0], R[:, 1], linewidth=5, marker='o', c=chain_color, markersize=43, markerfacecolor=pltc.to_rgba(bead_color, alpha=0.4), markeredgecolor=bead_color, markeredgewidth=5)
ax.scatter(Rmean[0], Rmean[1])
Rg_circle = plt.Circle((Rmean[0], Rmean[1]), Rg, color=Rg_color, ls='--', fill=False, linewidth=5)
Re_circle = plt.Circle((Rmean[0], Rmean[1]), Re, color=Re_color, ls='--', fill=False, linewidth=5)
ax.set_aspect(1)
ax.add_artist(Rg_circle)
ax.add_artist(Re_circle)
ax.plot([R[0, 0], R[-1, 0]], [R[0, 1], R[-1, 1]], c=Re_color, lw=3)
ax.plot([Rmean[0], Rmean[0]], [Rmean[1], Rmean[1]-Rg], c=Rg_color, lw=3)
#ax.text(np.amin(R[:, 0])+0.9, np.amax(R[:, 1])-0.5, r'$R_{g}$', c=Rg_color, fontsize=20)
#ax.text(np.amax(R[:, 0])-1.0, np.amin(R[:, 1])+0.05, r'$R_{e}$', c=Re_color, fontsize=20)
ax.text(np.amin(R[:, 0])+1.5, np.amax(R[:, 1])-1.1, r'$R_{g}$', c=Rg_color, fontsize=20)
ax.text(Rmean[0], np.amin(R[:, 1])-0.55, r'$R_{e}$', c=Re_color, fontsize=20)
#ax.plot([Rmean[0], Rmean[0]], [Rmean[1], Rmean[1]-Re], c='r')
#ax.scatter(R[:, 0], R[:, 1], marker='o', s=6000, alpha=0.5)
if False:
  for i in range(len(R)):
    ax.text(R[i, 0], R[i, 1], str(i))
ax.set_xlim(np.amin(R[:, 0]) - 1, np.amax(R[:, 0]) + 1)
ax.set_ylim(np.amin(R[:, 1]) - 1, np.amax(R[:, 1]) + 1)
ax.tick_params(axis='both', labelsize=8)
#plt.legend(loc='best')
if test == 0:
  plt.subplots_adjust(left=-0.06, top=1.2, bottom=-0.20, right=1.06)

ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.spines.left.set_visible(False)
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.spines.bottom.set_visible(False)

plt.savefig("fig-polymer_sizes.pdf")
plt.close()
