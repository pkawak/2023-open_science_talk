#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 21:51:37 2020

@author: pkawak
"""

import numpy as np
import matplotlib.pyplot as plt

fig_width = 2.4
fig_height = 2.7

np.random.seed(92932)
x = np.linspace(0,np.pi/2+0.5,10)
xlong = np.linspace(0,np.pi/2+0.5,1000)

width = 0.18*np.ones(len(x))
width2 = 0.23*np.ones(len(x))

rand_perturb = (np.random.rand(len(x))-0.5)*0.4
rand_perturb[0] = 0.

fig = plt.figure(figsize=(fig_width, fig_height))
ax = fig.add_subplot(111)

plt.xlabel('Energy', fontsize=10, labelpad=4)
plt.ylabel(r'Density of States$= \Omega$(Energy)', fontsize=10, labelpad=0.0)
plt.xticks([])
plt.yticks([])
plt.ylim(0, 1.2)
plt.xlim(-0.1,np.pi/2+0.5+0.11)

plt.plot(xlong, np.sin(xlong), label = 'real', c='k')
plt.subplots_adjust(left=0.095, bottom=0.07, right=0.995, top=0.99)
plt.savefig('fig-WL_DOS_traj.pdf')
plt.legend(loc='upper left',fontsize=8)
plt.savefig('fig-WL_DOS_traj_0.pdf')

plt.bar(x, 0.01*np.ones(len(x)), label = 'iteration 0', width=width, color='r')
plt.legend(loc='upper left',fontsize=8)
plt.savefig('fig-WL_DOS_traj_1.pdf')

plt.bar(x, np.sin(x)+rand_perturb, label = 'iteration 15', width=width2, color='b', alpha=0.1)
plt.legend(loc='upper left',fontsize=8)
plt.savefig('fig-WL_DOS_traj_2.pdf')

plt.bar(x, np.sin(x), label = 'iteration 26', width=width, color='b')
plt.bar(x, 0.01*np.ones(len(x)), width=width, color='r')
plt.legend(loc='upper left',fontsize=8)
plt.savefig('fig-WL_DOS_traj_3.pdf')
