#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 17:32:10 2021

@author: pierrekawak
"""

import numpy as np
import matplotlib.pyplot as plt
import json

with open("2d_plot_params.json", "r+") as file:
  data = json.load(file)
start = int(data["start"])
end   = int(data["end"])
initialPoint_i = int(data["initialPoint_i"])
initialPoint_j = int(data["initialPoint_j"])
initialPoint   = (initialPoint_j, initialPoint_i)
endPoint_i     = int(data["endPoint_i"])
endPoint_j     = int(data["endPoint_j"])
endPoint       = (endPoint_j, endPoint_i)

#this section just gets binSize and other params
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

#get path
data = np.loadtxt("MFEP_1d.out", skiprows=1)
P2 = data[:, 0]
Q6 = data[:, 1]
x  = data[:, 2]
y  = data[:, 3].tolist()
id_max = y.index(max(y))
with open("heights.out", "w") as f:
  f.write(str(y[0]) + " " + str(np.amax(y)) + " " + str(y[-1]))

transPoint_r = ((P2[id_max]+0.5)*binSize1+rangel1, (Q6[id_max]+0.5)*binSize2+rangel2)
transPoint   = (P2[id_max], Q6[id_max])
initialPoint_r = ((initialPoint[0]+0.5)*binSize1+rangel1, (initialPoint[1]+0.5)*binSize2+rangel2)
endPoint_r = ((endPoint[0]+0.5)*binSize1+rangel1, (endPoint[1]+0.5)*binSize2+rangel2)

#1D curve
with open("params.json", "r+") as file:
  data = json.load(file)
T = float(data["T"])

#filename = "1d_P2_lng.out"
#start = 600
#end = 2781
#data = np.loadtxt(filename, skiprows=1)
#data = data[start:end]
#
#filename2 = "2d_P2_lng.out"
#data2 = np.loadtxt(filename2, skiprows=1)
#data2 = data2[start:end]
#
#data[:, 1] = -data[:, 1]*T
#data[:, 1] -= np.amin(data[:, 1])
#data2[:, 1] = -data2[:, 1]*T
#data2[:, 1] -= np.amin(data2[:, 1])
#with open("heights.out", "w") as f:
#  f.write(str(data2[:, 1][0]) + " " + str(np.amax(data2[:, 1])) + " " + str(data2[:, 1][-1]))

fig, ax = plt.subplots(figsize=(3.25,2.0))#figsize=(3.2,3.0))
ax.plot(x, y, c='b', label="MFEP")
#ax.plot(data[:, 0], data[:, 1], label="1D EXEDOS")
#ax.plot(data2[:, 0], data2[:, 1], label="1D proj. of 2D EXEDOS")
#linspace = np.linspace(0, 1, len(data[:, 1]))
#length = len(data[:, 1])
#divide = 50
#num = int(length/divide)
#subset_data = [ data[i*divide, 1] for i in range(num) ]
#subset_linspace = [ linspace[i*divide] for i in range(num) ]
#ax.scatter(subset_linspace, subset_data, marker=(5, 2), c='r', s=5, label="1D EXEDOS")
#ax.plot(np.linspace(0, 1, len(data[:, 1])), data[:, 1], ls='--', c='r', label="1D EXEDOS")
#ax.plot(np.linspace(0, 1, len(data2[:, 1])), data2[:, 1], ls='--', c='g', label="2D EXEDOS")
ax.tick_params(axis='both', labelsize=8)
ax.set_ylabel(r'$\Delta F/\epsilon$', fontsize=10, labelpad=6)
ax.set_xlabel(r'$\xi$'              , fontsize=10, labelpad=5)
#ax.scatter(0, y[0], c='m')
##ax.text(0.15, 0.1, "(" + str(round(initialPoint_r[0], 3)) + "," + str(round(initialPoint_r[1], 3)) + ")", transform=ax.transAxes, fontsize=8, c='m')
#ax.text(0.012, 0.3, "(" + str(round(initialPoint_r[0], 3)) + ",\n" + str(round(initialPoint_r[1], 3)) + ")", transform=ax.transAxes, fontsize=8, c='m')
#ax.scatter(x[id_max], y[id_max], c='r')
##ax.text(0.57, 0.7, "(" + str(round(transPoint_r[0], 3)) + ",\n" + str(round(transPoint_r[1], 3)) + ")", transform=ax.transAxes, fontsize=8, c='r')
#ax.text(0.4, 0.85, "(" + str(round(transPoint_r[0], 3)) + ",\n" + str(round(transPoint_r[1], 3)) + ")", transform=ax.transAxes, fontsize=8, c='r')
#ax.scatter(1, y[-1], c='g')
#ax.text(0.84, 0.3, "(" + str(round(endPoint_r[0], 3)) + ",\n" + str(round(endPoint_r[1], 3)) + ")", transform=ax.transAxes, fontsize=8, c='g')
#props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
#ax.text(0.8, 0.85, "(P2,Q6)", transform=ax.transAxes, fontsize=8, bbox=props)
plt.subplots_adjust(left=0.15, bottom=0.21, right=0.99, top=0.99)
#plt.legend(loc='best', prop={'size': 8})
##plt.show()
fig.savefig("subfig-2d_barrier_10.25_v2.pdf")
