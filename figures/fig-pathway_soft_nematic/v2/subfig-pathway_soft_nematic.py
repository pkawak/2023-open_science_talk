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

#with open("2d_plot_params.json", "r+") as file:
#  data = json.load(file)
#start = int(data["start"])
#end   = int(data["end"])
#point_i = data["point_i"]
#point_j = data["point_j"]
#initialPoint_i = point_i[0]
#initialPoint_j = point_j[0]
#endPoint_i = point_i[1]
#endPoint_j = point_j[1]
start = 0
end   = -1

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

fontsize=10
pt = 1/72
x_figsize = 262
y_figsize = 210
fig, ax = plt.subplots(figsize=(x_figsize*pt,y_figsize*pt))#,constrained_layout=True)
im = ax.imshow(lng_2d, interpolation='bilinear', cmap=cm.get_cmap('coolwarm', 20),
               vmin=0, vmax=2,
               origin='lower', extent=[0,1,0,1])#,
ax.autoscale(False)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar = fig.colorbar(im, cax=cax, ticks=[0,1,2])
cbar.ax.tick_params(labelsize=8)
num_x_points = 2
num_y_points = 5
y_label_list = [ round((rangeh1-rangel1)/(num_y_points-1)*(i)+rangel1, 2) for i in range(num_y_points) ]
x_label_list = [ round((rangeh2-rangel2)/(num_x_points-1)*(i)+rangel2, 3) for i in range(num_x_points) ]
ax.set_xticks(np.linspace(0,1,num_x_points).tolist())
ax.set_yticks(np.linspace(0,1,num_y_points).tolist())
ax.set_xticklabels(x_label_list, fontsize=8)
ax.set_yticklabels(y_label_list, fontsize=8)
ax.set_xlabel(r"Crystal Order ($Q_{6}$)", fontsize=fontsize, labelpad=-5)
ax.set_ylabel(r"Nematic Order ($P_{2}$)", fontsize=fontsize, labelpad=4)
plt.subplots_adjust(left=0.145, bottom=0.092, right=0.925, top=0.986, wspace=None, hspace=None)
fig.savefig("subfig-pathway_soft_nematic.pdf")

x_figsize = 200
y_figsize = 160
fig.set_size_inches(x_figsize*pt, y_figsize*pt, forward=True)
plt.subplots_adjust(left=0.21, bottom=0.092, right=0.925, top=0.986, wspace=None, hspace=None)
fig.savefig("subfig-pathway_soft_nematic_small.pdf")

fontsize=7
x_figsize = 140
y_figsize = 100
fig.set_size_inches(x_figsize*pt, y_figsize*pt, forward=True)
ax.set_xticklabels(x_label_list, fontsize=6)
ax.set_yticklabels(y_label_list, fontsize=6)
ax.set_xlabel(r"$Q_{6}$", fontsize=fontsize, labelpad=-5)
ax.set_ylabel(r"$P_{2}$", fontsize=fontsize, labelpad=4)
cbar.ax.tick_params(labelsize=6)
plt.subplots_adjust(left=0.21, bottom=0.145, right=0.925, top=0.975, wspace=None, hspace=None)
fig.savefig("subfig-pathway_soft_nematic_smaller.pdf")
#ax.scatter((initialPoint_i+0.5)/np.shape(lng_2d)[1], (initialPoint_j+0.5)/np.shape(lng_2d)[0], c='#FF7600', s=30, marker='x', zorder=2)
#ax.scatter((endPoint_i+0.5)/np.shape(lng_2d)[1], (endPoint_j+0.5)/np.shape(lng_2d)[0], c='#52006A', s=30, marker='x', zorder=2)
#fig.savefig("subfig-pathway_soft_nematic_mark.pdf")

##get path
#data = np.loadtxt("MFEP_1d.out", skiprows=1)
#P2 = data[:, 0]
#Q6 = data[:, 1]
#y  = data[:, 3].tolist()
#ax.plot([(i+0.5)/np.shape(lng_2d)[1] for i in Q6], [(i+0.5)/np.shape(lng_2d)[0] for i in P2], c='y', zorder=1)
#fig.savefig("subfig-pathway_soft_nematic_MFEP.pdf")
plt.close()
