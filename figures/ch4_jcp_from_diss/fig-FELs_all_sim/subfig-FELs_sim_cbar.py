#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 17:32:10 2021

@author: pierrekawak
"""
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
#from mpl_toolkits.axes_grid1 import make_axes_locatable
import sys
import json

dirnames  = ["Lx10.00/p373627_avg_mw2/" , "Lx10.33/p267_avg_mw2/"  , "Lx10.75/p22635_avg_mw2/", "Lx10.25/p290729_avg_mw2/", "Lx10.50/p247975_avg_mw2/"   ]
names     = [r"c) $\phi=0.471$"         , r"d) $\phi=0.428$"       , r"e) $\phi=0.379$"       , r"a) $\phi=0.438$"        , r"b) $\phi=0.407$"     ]
names_alt = ["p471"                     , "p428"                   , "p379"                   , "p438"                    , "p407"                 ]

vmin = 0
vmax = 400
dirs_count = len(dirnames)
#fig, ax = plt.subplots(1, 3, figsize=(6.5, 2.7))

ii = 0
j = 0
i = 0

for dir, name in zip(dirnames, names):
#  if i:
#    plt.show()
#    sys.exit()
  if j==0:
    #fig, ax = plt.subplots(1, 1, figsize=(2.3, 2.4))
    fig, ax = plt.subplots(1, 1, figsize=(3.185, 3.0))
  else:
    #fig, ax = plt.subplots(1, 1, figsize=(3.1, 2.6))
    fig, ax = plt.subplots(1, 1, figsize=(4.1, 3.15))

  with open(dir+"/params.json", "r+") as file_param:
    data = json.load(file_param)
  T = float(data["T"])

  with open(dir+"2d_plot_params.json", "r+") as file:
    data = json.load(file)
  start = int(data["start"])
  end   = int(data["end"])
  point_i = data["point_i"]
  point_j = data["point_j"]

  data = np.loadtxt(dir+"/lng_2d.out", skiprows=1)
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
#  print(np.amin(lng), np.amax(lng))
  lng_2d = np.reshape(lng, (-1, size2))
  if i == 0:
    vmin = min(lng)
    vmax = max(lng)
  im = ax.imshow(lng_2d, interpolation='bilinear', cmap=cm.get_cmap('coolwarm', 20),
                    vmin=vmin, vmax=vmax,
                    origin='lower', extent=[0,1,0,1])#,
#  ax.contour(lng_2d, cmap=cm.seismic,
##                vmin=vmin, vmax=vmax,
#                origin='lower', extent=[0,1,0,1])#,
  ax.autoscale(False)
  y_label_list = [ round((rangeh1-rangel1)/5*(i)+rangel1, 2) for i in range(6) ]
  x_label_list = [ round((rangeh2-rangel2)/5*(i)+rangel2, 3) for i in range(5) ]
  ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
#  if i == 0:
  ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
  ax.set_xticklabels(x_label_list, fontsize=8)
#  if i == 0:
  ax.set_yticklabels(y_label_list, fontsize=8)
#  else:
#    ax.set_yticklabels([])
  ax.set_xlabel(r"$Q_6$", fontsize=10, labelpad=5)
  if ii == 0:
    ax.set_ylabel(r"$P_2$", fontsize=10, labelpad=6)
#  ax.set_title(name, fontsize=10, pad=30.0)
  for iii in range(len(point_i)):
    ax.scatter((float(point_i[iii])+0.5)/np.shape(lng_2d)[1], (float(point_j[iii])+0.5)/np.shape(lng_2d)[0], c='k', s=20, marker='x')
  if j == 0:
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("top", size="5%", pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation="horizontal")
    cax.xaxis.set_ticks_position("top")
    cbar.ax.tick_params(labelsize=8)
    if ii == 0:
      plt.subplots_adjust(left=0.24, bottom=0.135, right=0.94, top=0.925)
    else:
      plt.subplots_adjust(left=0.25, bottom=0.07, right=0.94, top=1.00)
  else:
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = fig.colorbar(im, cax=cax)#, orientation='horizontal', pad=0.18)
    cbar.ax.tick_params(labelsize=8)
    if ii == 0:
      plt.subplots_adjust(left=0.195, bottom=0.14, right=0.915, top=0.97)
    else:
      plt.subplots_adjust(left=0.195, bottom=0.14, right=0.91, top=0.97)
  plt.savefig("subfig-FEL_"+names_alt[i]+"_sim_cbar.pdf")
#  if i == 4:
#    plt.show()
#    sys.exit()
#  plt.close()
  i+=1
  ii+=1
#  if True:#j:
#    plt.show()
#    sys.exit()
  if ii > 2:
   # plt.close()
   # fig, ax = plt.subplots(1, 2, figsize=(6.5, 2.3))
    j+= 1
    ii = 0
