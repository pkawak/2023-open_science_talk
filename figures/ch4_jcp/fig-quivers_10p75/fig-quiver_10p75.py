#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 17:32:10 2022

@author: pierrekawak
"""

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

with open("2d_plot_params.json", "r+") as file:
  data = json.load(file)
start = int(data["start"])
end   = int(data["end"])
point_i = data["point_i"]
point_j = data["point_j"]
initialPoint_i = point_i[0]
initialPoint_j = point_j[0]
endPoint_i = point_i[1]
endPoint_j = point_j[1]

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

# get vector field
dir_F_q6  = np.empty(shape=(F_2d.shape))
dir_F_p2  = np.empty(shape=(F_2d.shape))
max_mag_F = np.empty(shape=(F_2d.shape))

dir_U_q6  = np.empty(shape=(F_2d.shape))
dir_U_p2  = np.empty(shape=(F_2d.shape))
max_mag_U = np.empty(shape=(F_2d.shape))

dir_mTS_q6  = np.empty(shape=(F_2d.shape))
dir_mTS_p2  = np.empty(shape=(F_2d.shape))
max_mag_mTS = np.empty(shape=(F_2d.shape))

for iy, ix in np.ndindex(F_2d.shape):
#  print(F_2d[iy, ix])
  min_F_val = F_2d[iy, ix]
  min_U_val = U_2d[iy, ix]
  min_mTS_val = mTS_2d[iy, ix]
  min_F_u = 0
  min_F_v = 0
  min_U_u = 0
  min_U_v = 0
  min_mTS_u = 0
  min_mTS_v = 0
  for u in [-1, 0, +1]:
    for v in [-1, 0, +1]:
      iyu = iy+u
      ixv = ix+v
      if iyu < 0 or ixv < 0 or iyu >= F_2d.shape[0] or ixv >= F_2d.shape[1]:
        continue
#      print("neigh:", iy+u, ix+v, F_2d[iy+u, ix+v])
      min_F_val = min(min_F_val, F_2d[iyu, ixv])
      if min_F_val == F_2d[iyu, ixv]:
        min_F_u = u
        min_F_v = v
      min_U_val = min(min_U_val, U_2d[iyu, ixv])
      if min_U_val == U_2d[iyu, ixv]:
        min_U_u = u
        min_U_v = v
      min_mTS_val = min(min_mTS_val, mTS_2d[iyu, ixv])
      if min_mTS_val == mTS_2d[iyu, ixv]:
        min_mTS_u = u
        min_mTS_v = v
#  print("for", iy, ix, F_2d[iy, ix], min_u, min_v, min_val)
  dir_F_q6[iy, ix] = min_F_v
  dir_F_p2[iy, ix] = min_F_u
  max_mag_F[iy, ix] = F_2d[iy, ix] - min_F_val
  dir_U_q6[iy, ix] = min_U_v
  dir_U_p2[iy, ix] = min_U_u
  max_mag_U[iy, ix] = U_2d[iy, ix] - min_U_val
  dir_mTS_q6[iy, ix] = min_mTS_v
  dir_mTS_p2[iy, ix] = min_mTS_u
  max_mag_mTS[iy, ix] = mTS_2d[iy, ix] - min_mTS_val
#  count+=1
#  if count == 10:
#    break

fontsize=10
pt = 1/72
x_figsize = 262
y_figsize = 210
fig, ax = plt.subplots(figsize=(x_figsize*pt,y_figsize*pt))#,constrained_layout=True)
#im0 = ax.imshow(F_2d, interpolation='bilinear', cmap=cm.get_cmap('coolwarm', 20),
#               origin='lower', extent=[0,1,0,1])
op1_mod = (op1-np.amin(op1))/(np.amax(op1)-np.amin(op1))
op2_mod = (op2-np.amin(op2))/(np.amax(op2)-np.amin(op2))
op1_mod_2d = np.reshape(op1_mod, (-1, size2))
op2_mod_2d = np.reshape(op2_mod, (-1, size2))
op1_ph  = []
op2_ph  = []
q6_ph = []
p2_ph = []
mag_ph = []
num_stuff = 30
skip = int(len(op2_mod_2d)/num_stuff)
for i in range(num_stuff):
#  print(op2_mod_2d[i*skip], op1_mod_2d[i*skip], i, i*skip)
  op1_ph.append(op1_mod_2d[i*skip])
  op2_ph.append(op2_mod_2d[i*skip])
  q6_ph.append(dir_F_q6[i*skip])
  p2_ph.append(dir_F_p2[i*skip])
  mag_ph.append(max_mag_F[i*skip])
  
op1_mod_2d = np.array(op1_ph)
op2_mod_2d = np.array(op2_ph)
dir_F_q6 = np.array(q6_ph)
dir_F_p2 = np.array(p2_ph)
max_mag_F = np.array(mag_ph)
arrow_widths = max_mag_F/np.amax(max_mag_F)
quiv = ax.quiver(op2_mod_2d, op1_mod_2d, dir_F_q6, dir_F_p2, arrow_widths, linewidths=arrow_widths.flatten(), cmap=cm.get_cmap('coolwarm', 20))
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.autoscale(False)
divider = make_axes_locatable(ax)
cax_quiv = divider.append_axes("right", size="5%", pad=0.05)
cbar_quiv = fig.colorbar(quiv, cax=cax_quiv, ticks=[])
cbar_quiv.ax.tick_params(labelsize=8)
num_x_points = 2
num_y_points = 3
y_label_list = [ round((rangeh1-rangel1)/(num_y_points-1)*(i)+rangel1, 2) for i in range(num_y_points) ]
x_label_list = [ round((rangeh2-rangel2)/(num_x_points-1)*(i)+rangel2, 3) for i in range(num_x_points) ]
ax.set_xticks(np.linspace(0,1,num_x_points).tolist())
ax.set_yticks(np.linspace(0,1,num_y_points).tolist())
ax.set_xticklabels(x_label_list, fontsize=8)
ax.set_yticklabels(y_label_list, fontsize=8)
ax.set_xlabel(r"Crystal Order ($Q_{6}$)", fontsize=fontsize, labelpad=-5)
ax.set_ylabel(r"Nematic Order ($P_{2}$)", fontsize=fontsize, labelpad=4)
plt.subplots_adjust(left=0.16, bottom=0.092, right=0.945, top=0.986, wspace=None, hspace=None)
ax.scatter((initialPoint_i+0.5)/np.shape(F_2d)[1], (initialPoint_j+0.5)/np.shape(F_2d)[0], c='#FF7600', s=30, marker='x', zorder=2)
ax.scatter((endPoint_i+0.5)/np.shape(F_2d)[1], (endPoint_j+0.5)/np.shape(F_2d)[0], c='#52006A', s=30, marker='x', zorder=2)
fig.savefig("fig-quiver_10.75.pdf")

fig, ax = plt.subplots(figsize=(x_figsize*pt,y_figsize*pt))#,constrained_layout=True)
op1_mod = (op1-np.amin(op1))/(np.amax(op1)-np.amin(op1))
op2_mod = (op2-np.amin(op2))/(np.amax(op2)-np.amin(op2))
op1_mod_2d = np.reshape(op1_mod, (-1, size2))
op2_mod_2d = np.reshape(op2_mod, (-1, size2))
op1_ph  = []
op2_ph  = []
q6_ph = []
p2_ph = []
mag_ph = []
num_stuff = 30
skip = int(len(op2_mod_2d)/num_stuff)
for i in range(num_stuff):
#  print(op2_mod_2d[i*skip], op1_mod_2d[i*skip], i, i*skip)
  op1_ph.append(op1_mod_2d[i*skip])
  op2_ph.append(op2_mod_2d[i*skip])
  q6_ph.append(dir_U_q6[i*skip])
  p2_ph.append(dir_U_p2[i*skip])
  mag_ph.append(max_mag_U[i*skip])
  
op1_mod_2d = np.array(op1_ph)
op2_mod_2d = np.array(op2_ph)
dir_U_q6 = np.array(q6_ph)
dir_U_p2 = np.array(p2_ph)
max_mag_U = np.array(mag_ph)
#print(op2_mod_2d)
#print(op2_ph)
arrow_widths = max_mag_U/np.amax(max_mag_U)
quiv = ax.quiver(op2_mod_2d, op1_mod_2d, dir_U_q6, dir_U_p2, arrow_widths, linewidths=arrow_widths.flatten(), cmap=cm.get_cmap('coolwarm', 20))
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.autoscale(False)
divider = make_axes_locatable(ax)
cax_quiv = divider.append_axes("right", size="5%", pad=0.05)
cbar_quiv = fig.colorbar(quiv, cax=cax_quiv, ticks=[])
cbar_quiv.ax.tick_params(labelsize=8)
num_x_points = 2
num_y_points = 3
y_label_list = [ round((rangeh1-rangel1)/(num_y_points-1)*(i)+rangel1, 2) for i in range(num_y_points) ]
x_label_list = [ round((rangeh2-rangel2)/(num_x_points-1)*(i)+rangel2, 3) for i in range(num_x_points) ]
ax.set_xticks(np.linspace(0,1,num_x_points).tolist())
ax.set_yticks(np.linspace(0,1,num_y_points).tolist())
ax.set_xticklabels(x_label_list, fontsize=8)
ax.set_yticklabels(y_label_list, fontsize=8)
ax.set_xlabel(r"Crystal Order ($Q_{6}$)", fontsize=fontsize, labelpad=-5)
ax.set_ylabel(r"Nematic Order ($P_{2}$)", fontsize=fontsize, labelpad=4)
plt.subplots_adjust(left=0.16, bottom=0.092, right=0.945, top=0.986, wspace=None, hspace=None)
ax.scatter((initialPoint_i+0.5)/np.shape(F_2d)[1], (initialPoint_j+0.5)/np.shape(F_2d)[0], c='#FF7600', s=30, marker='x', zorder=2)
ax.scatter((endPoint_i+0.5)/np.shape(F_2d)[1], (endPoint_j+0.5)/np.shape(F_2d)[0], c='#52006A', s=30, marker='x', zorder=2)
fig.savefig("fig-U_quiver_10.75.pdf")

fig, ax = plt.subplots(figsize=(x_figsize*pt,y_figsize*pt))#,constrained_layout=True)
#im0 = ax.imshow(mTS_2d, interpolation='bilinear', cmap=cm.get_cmap('coolwarm', 20),
#               origin='lower', extent=[0,1,0,1])
op1_mod = (op1-np.amin(op1))/(np.amax(op1)-np.amin(op1))
op2_mod = (op2-np.amin(op2))/(np.amax(op2)-np.amin(op2))
op1_mod_2d = np.reshape(op1_mod, (-1, size2))
op2_mod_2d = np.reshape(op2_mod, (-1, size2))
op1_ph  = []
op2_ph  = []
q6_ph = []
p2_ph = []
mag_ph = []
num_stuff = 30
skip = int(len(op2_mod_2d)/num_stuff)
for i in range(num_stuff):
#  print(op2_mod_2d[i*skip], op1_mod_2d[i*skip], i, i*skip)
  op1_ph.append(op1_mod_2d[i*skip])
  op2_ph.append(op2_mod_2d[i*skip])
  q6_ph.append(dir_mTS_q6[i*skip])
  p2_ph.append(dir_mTS_p2[i*skip])
  mag_ph.append(max_mag_mTS[i*skip])
  
op1_mod_2d = np.array(op1_ph)
op2_mod_2d = np.array(op2_ph)
dir_mTS_q6 = np.array(q6_ph)
dir_mTS_p2 = np.array(p2_ph)
max_mag_mTS = np.array(mag_ph)
#print(op2_mod_2d)
#print(op2_ph)
arrow_widths = max_mag_mTS/np.amax(max_mag_mTS)
quiv = ax.quiver(op2_mod_2d, op1_mod_2d, dir_mTS_q6, dir_mTS_p2, arrow_widths, linewidths=arrow_widths.flatten(), cmap=cm.get_cmap('coolwarm', 20))
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.autoscale(False)
divider = make_axes_locatable(ax)
cax_quiv = divider.append_axes("right", size="5%", pad=0.05)
cbar_quiv = fig.colorbar(quiv, cax=cax_quiv)
cbar_quiv.ax.tick_params(labelsize=8)
num_x_points = 2
num_y_points = 3
y_label_list = [ round((rangeh1-rangel1)/(num_y_points-1)*(i)+rangel1, 2) for i in range(num_y_points) ]
x_label_list = [ round((rangeh2-rangel2)/(num_x_points-1)*(i)+rangel2, 3) for i in range(num_x_points) ]
ax.set_xticks(np.linspace(0,1,num_x_points).tolist())
ax.set_yticks(np.linspace(0,1,num_y_points).tolist())
ax.set_xticklabels(x_label_list, fontsize=8)
ax.set_yticklabels(y_label_list, fontsize=8)
ax.set_xlabel(r"Crystal Order ($Q_{6}$)", fontsize=fontsize, labelpad=-5)
ax.set_ylabel(r"Nematic Order ($P_{2}$)", fontsize=fontsize, labelpad=4)
plt.subplots_adjust(left=0.16, bottom=0.092, right=0.945, top=0.986, wspace=None, hspace=None)
ax.scatter((initialPoint_i+0.5)/np.shape(F_2d)[1], (initialPoint_j+0.5)/np.shape(F_2d)[0], c='#FF7600', s=30, marker='x', zorder=2)
ax.scatter((endPoint_i+0.5)/np.shape(F_2d)[1], (endPoint_j+0.5)/np.shape(F_2d)[0], c='#52006A', s=30, marker='x', zorder=2)
fig.savefig("fig-mTS_quiver_10.75.pdf")
