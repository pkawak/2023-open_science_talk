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

fontsize=11
pt = 1/72
x_figsize = 223
y_figsize = 210
fig, ax = plt.subplots(figsize=(x_figsize*pt,y_figsize*pt),constrained_layout=True)
im = ax.imshow(lng_2d, interpolation='bilinear', cmap=cm.get_cmap('coolwarm', 20),
               origin='lower', extent=[0,1,0,1])#,
ax.autoscale(False)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
#cbar = fig.colorbar(im, cax=cax, ticks=[0,0.1,0.2])
#cbar.ax.tick_params(labelsize=8)
cbar = fig.colorbar(im, cax=cax)
#cbar.set_ticks([])
y_label_list = [ round((rangeh1-rangel1)/5*(i)+rangel1, 2) for i in range(6) ]
x_label_list = [ round((rangeh2-rangel2)/5*(i)+rangel2, 3) for i in range(6) ]
#ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
#ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_xticks([])
ax.set_yticks([])
#ax.set_xticklabels(x_label_list, fontsize=8)
#ax.set_yticklabels(y_label_list, fontsize=8)
ax.set_xlabel(r"Crystal Order ($Q_{6}$)", fontsize=fontsize, labelpad=5)
ax.set_ylabel(r"Nematic Order ($P_{2}$)", fontsize=fontsize, labelpad=5)
#plt.subplots_adjust(left=0.172, bottom=0.09, right=0.915, top=0.988, wspace=None, hspace=None)
fig.savefig("subfig-pathway_ToC.pdf")
ax.scatter((initialPoint_i+0.5)/np.shape(lng_2d)[1], (initialPoint_j+0.5)/np.shape(lng_2d)[0], c='#FF7600', s=30, marker='x', zorder=2)
ax.scatter((endPoint_i+0.5)/np.shape(lng_2d)[1], (endPoint_j+0.5)/np.shape(lng_2d)[0], c='#52006A', s=20, marker='x', zorder=2)
fig.savefig("subfig-pathway_ToC_mark.pdf")
ax.plot([(i+0.5)/np.shape(lng_2d)[1] for i in Q6], [(i+0.5)/np.shape(lng_2d)[0] for i in P2], c='y', zorder=1)
fig.savefig("subfig-pathway_ToC_MFEP.pdf")
plt.close()
