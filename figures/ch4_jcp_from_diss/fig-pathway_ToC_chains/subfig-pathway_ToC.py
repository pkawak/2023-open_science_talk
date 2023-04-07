#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 17:32:10 2021

@author: pierrekawak
"""

import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import sys
import json

#this section just gets binSize and other params
with open("params.json", "r+") as file:
  data = json.load(file)
T = float(data["T"])

filename = "lng_2d.out"
start = 1700
end   = 15065
data = np.loadtxt(filename, skiprows=1)
data = data[start:end]

op1 = data[:,0]
rangel1 = min(op1)
rangeh1 = max(op1)
op2 = data[:,1]
rangel2 = min(op2)
rangeh2 = max(op2)
binSize2 = op2[1]-op2[0]
rangeh2 += binSize2
size2 = int(round((rangeh2-rangel2)/binSize2))
binSize1 = (rangeh1-rangel1)/len(op2)*size2/(1-size2/len(op2))
rangeh1 += binSize1
size1 = int(round((rangeh1-rangel1)/binSize1))
lng = data[:,2]

lng = -lng*T
lng -= np.amin(lng)
lng_2d = np.reshape(lng, (-1, size2))

#get path
data = np.loadtxt("MFEP_1d.out", skiprows=1)
P2 = data[:, 0]
Q6 = data[:, 1]
y  = data[:, 3].tolist()
P2 = P2[:-59]
Q6 = Q6[:-59]
y = y[:-59]

#
initialPoint_i = 1
initialPoint_j = 277
initialPoint   = (initialPoint_j, initialPoint_i)
endPoint_i     = 4
endPoint_j     = 2472
endPoint       = (endPoint_j, endPoint_i)
id_max = y.index(max(y))
transPoint   = (P2[id_max], Q6[id_max])

fig, ax = plt.subplots(figsize=(2,2))
im = ax.imshow(lng_2d, interpolation='bilinear', cmap=cm.get_cmap('coolwarm', 20),
               origin='lower', extent=[0,1,0,1])#,
ax.autoscale(False)
ax.plot([(i+0.5)/np.shape(lng_2d)[1] for i in Q6], [(i+0.5)/np.shape(lng_2d)[0] for i in P2], c='y', zorder=1)
ax.scatter((initialPoint_i+0.5)/np.shape(lng_2d)[1], (initialPoint_j+0.5)/np.shape(lng_2d)[0], c='#FF7600', s=30, marker='x', zorder=2)
ax.scatter((endPoint_i+0.5)/np.shape(lng_2d)[1], (endPoint_j+0.5)/np.shape(lng_2d)[0], c='#52006A', s=20, marker='x', zorder=2)
#ax.scatter((transPoint[1]+0.5)/np.shape(lng_2d)[1], (transPoint[0]+0.5)/np.shape(lng_2d)[0], c=[(0.5, 0, 0.5)], s=20, marker='x')
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar = fig.colorbar(im, cax=cax)
cbar.set_ticks([])
ax.set_xticks([])
ax.set_yticks([])
#ax.set_xlabel("Crystallinity", fontsize=7.5, labelpad=5)
#ax.set_ylabel("Alignment", fontsize=7.5, labelpad=5)
ax.set_xlabel("Crystalline Order", fontsize=7.5, labelpad=5)
ax.set_ylabel("Orientational Order", fontsize=7.5, labelpad=5)
ax.set_title("Minimum Free Energy Path", fontsize=7.5)
plt.subplots_adjust(left=0.09, bottom=0.035, right=0.98, top=0.965, wspace=None, hspace=None)
#plt.show()
#sys.exit()
fig.savefig("subfig-pathway_ToC.pdf")
plt.close()
