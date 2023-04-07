#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 14:41:46 2019

@author: pierrekawak
"""

import numpy as np
import matplotlib.pyplot as plt

Nc = np.array([100, 200, 550, 1100, 2000, 5100, 9000, 30000])
Speedup = np.array([6.47355096669961, 13.34966664365, 14.8654560719417, 26.6416888295147, 28.4156758608265, 44.0851145678282, 60.3077010681407, 68.5971439448075])

fig = plt.figure(figsize=(4,3), constrained_layout=True)
ax = fig.add_subplot(111)
plt.xlabel('$N_{c}$', fontsize=12, labelpad=8)
plt.ylabel('Speedup', fontsize=12, labelpad=8)
plt.loglog(Nc, Speedup, 'o', markersize=10)
plt.xticks([100, 1000, 1e4, 1e5])
plt.yticks([1, 10, 100])
#plt.subplots_adjust(left=0.30, right=0.94, bottom=0.23, top=0.95)
fig.savefig('fig-speedup.pdf')
