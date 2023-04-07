#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 17:32:10 2019

@author: pierrekawak
"""
#--------------------------------------------
#THIS FILE PLOTS COMMON THERMODYNAMIC DISTROS GIVEN A PARAMS.DAT FILE AND A LNG.OUT FILE
#IT ALSO OUTPUTS THE CANONICAL DISTRO AND THE POTENTIAL ENERGY AT GIVEN TEMPERATURE RANGE
#--------------------------------------------
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import sys
import json
from matplotlib.colors import LogNorm

with open("params.json", "r+") as file:
  data = json.load(file)
T = float(data["T"])

start   = 0
end     = -1
if len(sys.argv) > 1:
  start = int(sys.argv[1].split(':')[0])
  end   = int(sys.argv[1].split(':')[1])

filename = "lng_2d.out"
U_file   = "op1_op2_etot.out"
data = np.loadtxt(filename, skiprows=1)
U_data = np.loadtxt(U_file, skiprows=1)
if end == -1:
  end = len(data)
data   = data[start:end]
U_data = U_data[start:end]

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
U   = U_data[:,2]

F = -lng*T
F -= np.amin(F)
S = (U-F)/T
mTS = F-U
F_2d = np.reshape(F, (-1, size2))
U_2d = np.reshape(U, (-1, size2))
S_2d = np.reshape(S, (-1, size2))
mTS_2d = np.reshape(mTS, (-1, size2))
fig0, ax0 = plt.subplots(1, 1, figsize=(3.25,3.1), constrained_layout=False)
im0 = ax0.imshow(F_2d, interpolation='bilinear', cmap=cm.get_cmap('coolwarm', 20),
               origin='lower', extent=[0,1,0,1])
ax0.set_title(r"$F/\epsilon$")

fig1, ax1 = plt.subplots(1, 1, figsize=(3.25,3.1), constrained_layout=False)
im1 = ax1.imshow(U_2d, interpolation='bilinear', cmap=cm.get_cmap('coolwarm', 20),
               origin='lower', extent=[0,1,0,1])#, norm=LogNorm(vmin=-730, vmax=-450))
ax1.set_title(r"$U/\epsilon$")

print(np.amin(mTS_2d), np.amax(mTS_2d))
fig2, ax2 = plt.subplots(1, 1, figsize=(3.25,3.1), constrained_layout=False)
im2 = ax2.imshow(mTS_2d, interpolation='bilinear', cmap=cm.get_cmap('coolwarm', 20),
               origin='lower', extent=[0,1,0,1], norm=LogNorm(vmin=682, vmax=988))
ax2.set_title(r"$-TS/\epsilon$")

y_label_list = [ round((rangeh1-rangel1)/5*(i)+rangel1, 2) for i in range(6) ]
x_label_list = [ round((rangeh2-rangel2)/4*(i)+rangel2, 3) for i in range(5) ]
xticks = [0.0, 0.25, 0.5, 0.75, 1.0]
yticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

for fig, im, ax in [(fig0, im0, ax0), (fig1, im1, ax1), (fig2, im2, ax2)]:
  divider = make_axes_locatable(ax)
  cax = divider.append_axes("right", size="5%", pad=0.05)
  cbar = fig.colorbar(im, cax=cax)
  cbar.ax.tick_params(labelsize=8)
  ax.autoscale(False)
  ax.set_xticks(xticks)
  ax.set_yticks(yticks)
  ax.set_xticklabels(x_label_list, fontsize=8)
  ax.set_yticklabels(y_label_list, fontsize=8)
  ax.set_xlabel(r"$Q_{6}$", fontsize=10, labelpad=-0.7)
  ax.set_ylabel(r"$P_{2}$", fontsize=10)
fig0.subplots_adjust(left=0.17, bottom=0.15, right=0.92, top=0.98, wspace=None, hspace=None)
fig1.subplots_adjust(left=0.17, bottom=0.15, right=0.87, top=0.98, wspace=None, hspace=None)
fig2.subplots_adjust(left=0.17, bottom=0.15, right=0.83, top=0.98, wspace=None, hspace=None)
fig0.savefig("USF_plot_0.pdf")
fig1.savefig("USF_plot_1.pdf")
fig2.savefig("USF_plot_2.pdf")
#plt.show()
