#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 17:32:10 2021

@author: pierrekawak
"""
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("heights_phi.out")
names = data[:, 0]
start = data[:, 1]
heights = data[:, 2]
end = data[:, 3]

fig, ax = plt.subplots(figsize=(3.3,2.8))
ax.scatter(names, heights-start, marker='*', label='Ordering')
ax.scatter(names, heights-end, marker='o', facecolors='none', edgecolors='r', label='Melting')
ax.set_yscale('log')
ax.set_xlabel(r"Volume Fraction, $\phi$", fontsize=12, labelpad=6)
ax.set_ylabel(r"$\Delta F^{\dagger}/k_{B}T$", fontsize=12, labelpad=1)
ax.set_yticks([0.1, 1, 10])
ax.set_yticklabels([r"0.1", r"1", r"10"])
ax.axvline(0.428, 0.01, max(np.amax(heights-start), np.amax(heights-end)), color='dimgray', ls='--', alpha=0.6)
t = ax.text(0.380, 10, "Nematic""\n""Transitions, IN", fontsize=11, color='w')
t.set_bbox(dict(facecolor='g', alpha=0.5))
t = ax.text(0.433, 0.8, "Crystal""\n""Transitions, IC", fontsize=11, color='w')
t.set_bbox(dict(facecolor='b', alpha=0.5))
ax.tick_params(axis='both', which='major', labelsize=10, pad=0)
plt.subplots_adjust(left=0.143, bottom=0.155, right=0.998, top=0.997)
ax.legend(loc='lower right')
fig.savefig("fig-heights_vs_phi.pdf")
