#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 21:51:37 2020

@author: pkawak
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig_width = 2.4
fig_height = 2.7

np.random.seed(92932)
x = np.linspace(0,np.pi/2+0.5,10)
xlong = np.linspace(0,np.pi/2+0.5,1000)

width = 0.18*np.ones(len(x))
width2 = 0.23*np.ones(len(x))

rand_perturb = (np.random.rand(len(x))-0.5)*0.4
rand_perturb[0] = 0.

fig = plt.figure(figsize=(fig_width, fig_height), constrained_layout=True)
ax = fig.add_subplot(111)
ax.set_xlabel(r'Order Parameter $\xi$', fontsize=9, labelpad=4)
ax.set_ylabel(r'Free Energy = $-kT\ln Z(\xi, T)$', fontsize=9, labelpad=0.0)
#ax.set_xticks([xlong[0], xlong[int(len(xlong)/2)], xlong[-1]])
#ax.set_xticklabels([0, 0.5, 1])
ax.set_xticks([])
ax.set_yticks([])
plt.ylim(-1.2, 0.0)
plt.xlim(-0.1,np.pi/2+0.5+0.11)

plt.plot(xlong, -np.sin(xlong), label = 'real', c='k')
#plt.subplots_adjust(left=0.08, bottom=0.07, right=0.995, top=0.99)
#plt.subplots_adjust(left=0.1, bottom=0.1, right=0.995, top=0.99)
plt.savefig('fig-EXEDOS_traj.pdf')
plt.legend(loc='lower left',fontsize=8)
plt.savefig('fig-EXEDOS_traj_0.pdf')

plt.bar(x, -0.01*np.ones(len(x)), label = 'iteration 0', width=width, color='r')
plt.legend(loc='lower left',fontsize=8)
plt.savefig('fig-EXEDOS_traj_1.pdf')

plt.bar(x, -np.sin(x)+rand_perturb, label = 'iteration 15', width=width2, color='b', alpha=0.1)
plt.legend(loc='lower left',fontsize=8)
plt.savefig('fig-EXEDOS_traj_2.pdf')

plt.bar(x, -np.sin(x), label = 'iteration 26', width=width, color='b')
plt.bar(x, 0.01*np.ones(len(x)), width=width, color='r')
plt.legend(loc='lower left',fontsize=8)
plt.savefig('fig-EXEDOS_traj_3.pdf')

plt.close()

# setup the figure and axes
fig_height=2.4
fig = plt.figure(figsize=(fig_width, fig_height), facecolor='w')#, constrained_layout=True)
ax = fig.add_subplot(111, projection='3d')

# fake data
_x = np.arange(4)
_y = np.arange(5)
_xx, _yy = np.meshgrid(_x, _y)
x, y = _xx.ravel(), _yy.ravel()

top = x + y
bottom = np.zeros_like(top)
width = 1
depth = 1

ax.bar3d(x, y, bottom, width, depth, top, shade=True)
lblpd=-15
ax.set_xlabel(r"Crystal order ($Q_{6}$)"       , fontsize=9, labelpad=lblpd)
ax.set_ylabel(r"Nematic order ($P_{2}$)"       , fontsize=9, labelpad=lblpd)
#ax.set_zlabel(r"$\ln Z(Q_{6}, P_{2}, T)$", fontsize=10, labelpad=lblpd)
ax.set_title(r"$\ln Z(Q_{6}, P_{2}, T)$", fontsize=9, y=0.9)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
plt.subplots_adjust(left=-0.2, bottom=0.05, right=1.15, top=1.0)
plt.savefig('fig-EXEDOS_2D.pdf')
plt.close()
