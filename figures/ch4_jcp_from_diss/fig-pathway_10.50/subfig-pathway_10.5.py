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
import os

#this section just gets binSize and other params
with open("params.json", "r+") as file:
  data = json.load(file)
T = float(data["T"])

plot_MFEP = 0
if os.path.exists("2d_plot_params.json"):
  plot_MFEP = 1

start = 0
end   = -1
if plot_MFEP:
  with open("2d_plot_params.json", "r+") as file:
    data = json.load(file)
  start = int(data["start"])
  end   = int(data["end"])
  point_i = data["point_i"]
  point_j = data["point_j"]

filename = "lng_2d.out"
data = np.loadtxt(filename, skiprows=1)
if end == -1:
  end = len(data)
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
if plot_MFEP:
  data = np.loadtxt("MFEP_1d.out", skiprows=1)
  P2 = data[:, 0]
  Q6 = data[:, 1]
  x  = data[:, 2]
  y  = data[:, 3].tolist()

fig, ax = plt.subplots(figsize=(3.25,2.75))
im = ax.imshow(lng_2d, interpolation='bilinear', cmap=cm.get_cmap('coolwarm', 20),
               origin='lower', extent=[0,1,0,1])#,
ax.autoscale(False)
if plot_MFEP:
  for i in range(len(point_i)):
    ax.scatter((point_i[i]+0.5)/np.shape(lng_2d)[1], (point_j[i]+0.5)/np.shape(lng_2d)[0], c='k', s=20, marker='x')
  ax.plot([(i+0.5)/np.shape(lng_2d)[1] for i in Q6], [(i+0.5)/np.shape(lng_2d)[0] for i in P2], c='y')
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar = fig.colorbar(im, cax=cax)
cbar.ax.tick_params(labelsize=8)
y_label_list = [ round((rangeh1-rangel1)/5*(i)+rangel1, 2) for i in range(6) ]
x_label_list = [ round((rangeh2-rangel2)/5*(i)+rangel2, 3) for i in range(6) ]
ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_xticklabels(x_label_list, fontsize=8)
ax.set_yticklabels(y_label_list, fontsize=8)
ax.set_xlabel(r"$Q_6$", fontsize=10, labelpad=5)
ax.set_ylabel(r"$P_2$", fontsize=10, labelpad=5)
plt.subplots_adjust(left=0.172, bottom=0.15, right=0.915, top=0.98, wspace=None, hspace=None)
#plt.show()
#sys.exit()
fig.savefig("subfig-pathway_10.5.pdf")
plt.close()
