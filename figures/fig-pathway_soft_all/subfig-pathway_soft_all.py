#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 17:32:10 2022

@author: pierrekawak
"""

import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import sys
import json
import os

vmin = 0
vmax = 0.6
rangel1 = 0.11520
rangeh1 = 0.95424
binSize1 = 0.00032
size1 = int(round((rangeh1-rangel1)/binSize1))


jsons     = ["p044044_2d_plot_params.json", "p111371_2d_plot_params.json"]
lng_files = ["p044044_lng_2d.out"         , "p111371_lng_2d.out"         ]
Ts        = [0.044044                     , 0.111371                     ]
MFEP_files = ["p044044_MFEP_1d.out"         , "p111371_MFEP_1d.out"         ]

# make background
data = np.loadtxt(lng_files[0], skiprows=1)
lng = data[:,2] - np.amin(data[:,2]) + 100
op2 = data[:,1]
rangel2 = min(op2)
rangeh2 = max(op2)
binSize2 = op2[1]-op2[0]
rangeh2 += binSize2
size2 = int(round((rangeh2-rangel2)/binSize2))
lng_2d_orig = np.reshape(lng, (-1, size2))

fig, ax = plt.subplots(figsize=(3.7,3.2))
im = ax.imshow(lng_2d_orig, interpolation='bilinear', cmap=cm.get_cmap('coolwarm', 20),
               vmin = vmin, vmax = vmax,
               origin='lower', extent=[0,1,0,1])#,
ax.autoscale(False)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar = fig.colorbar(im, cax=cax)
cbar.ax.tick_params(labelsize=8)

y_label_list = [ round((rangeh1-rangel1)/5*(i)+rangel1, 2) for i in range(6) ]
ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(y_label_list, fontsize=8)
ax.set_ylabel(r"$P_2$", fontsize=10, labelpad=5)

x_label_list = [ round((rangeh2-rangel2)/5*(i)+rangel2, 2) for i in range(6) ]
ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_xticklabels(x_label_list, fontsize=8)
ax.set_xlabel(r"$Q_6$", fontsize=10, labelpad=5)

c = ['darkorange', 'lime']
file_idx = -1
for T, js, filename, MFEP in zip(Ts, jsons, lng_files, MFEP_files):
  file_idx+=1
  
  plot_MFEP = 0
  if os.path.exists(js):
    plot_MFEP = 1
  
  start = 0
  end   = -1
  if plot_MFEP:
    with open(js, "r+") as file:
      data = json.load(file)
    start = int(data["start"])
    end   = int(data["end"])
    point_i = data["point_i"]
    point_j = data["point_j"]
  
  data = np.loadtxt(filename, skiprows=1)
  if end == -1:
    end = len(data)
  data = data[start:end]
  
  op1 = data[:,0]
  rangel1_ = min(op1)
  rangeh1_ = max(op1)
  op2 = data[:,1]
  rangel2_ = min(op2)
  rangeh2_ = max(op2)
  binSize2 = op2[1]-op2[0]
  rangeh2_ += binSize2
  size2 = int(round((rangeh2_-rangel2_)/binSize2))
  binSize1_ = (rangeh1_-rangel1_)/len(op2)*size2/(1-size2/len(op2))
  rangeh1_ += binSize1_
  size1_ = int(round((rangeh1_-rangel1_)/binSize1_))
  lng = data[:,2]
  
  lng = -lng*T
  lng -= np.amin(lng)
  lng_2d = np.reshape(lng, (-1, size2))
  
  # find position relative to y axis
  skip = int( round( (rangel1_-rangel1)/binSize1_ ) ) / size1
  stop = int( round( (rangeh1_-rangel1)/binSize1_ ) ) / size1
#  print(T, skip, stop)
#  #get path
#  if plot_MFEP:
#    data = np.loadtxt("MFEP_1d.out", skiprows=1)
#    P2 = data[:, 0]
#    Q6 = data[:, 1]
  im = ax.imshow(lng_2d, interpolation='bilinear', cmap=cm.get_cmap('coolwarm', 20),
                 vmin = vmin, vmax = vmax,
                 origin='lower', extent=[0,1,skip,stop])#,

  # get path
  if plot_MFEP:
    with open(js, "r+") as file:
      data = json.load(file)
    start = int(data["start"])
    end   = int(data["end"])
    point_i = data["point_i"]
    point_j = data["point_j"]
#    data = np.loadtxt(MFEP, skiprows=1)
#    P2 = data[:, 0]
#    Q6 = data[:, 1]
#    x  = data[:, 2]
#    y  = data[:, 3].tolist()
    for i in range(len(point_i)):
      ax.scatter((point_i[i]+0.5)/np.shape(lng_2d_orig)[1], (point_j[i]+0.5)/np.shape(lng_2d_orig)[0], c=c[file_idx], s=30, marker='x')
#    ax.plot([(i+0.5)/np.shape(lng_2d)[1] for i in Q6], [(i+0.5)/np.shape(lng_2d)[0] for i in P2], c='y')

plt.subplots_adjust(left=0.151, bottom=0.12, right=0.927, top=0.99, wspace=None, hspace=None)

fig.savefig(os.path.basename(__file__).split('.py')[0]+".pdf")
plt.close()
