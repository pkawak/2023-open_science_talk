#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Tue June 14 08:41:00 2021

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import random
import sys
import pandas as pd

melt_color  = 'r'
nema_color   = 'g'
crys_color = 'b'

fig, ax = plt.subplots(1, figsize=(0.2223,0.2223))
ax.scatter(1, 1, s=16, c = melt_color)
ax.set_ylim(0.9999, 1.0001)
ax.set_xlim(0.9999, 1.0001)
ax.axis('off')
plt.savefig("subfig-melt_color.pdf")

fig, ax = plt.subplots(1, figsize=(0.2223,0.2223))
ax.scatter(1, 1, s=16, c = nema_color)
ax.set_ylim(0.9999, 1.0001)
ax.set_xlim(0.9999, 1.0001)
ax.axis('off')
plt.savefig("subfig-nema_color.pdf")

fig, ax = plt.subplots(1, figsize=(0.2223,0.2223))
ax.scatter(1, 1, s=16, c = crys_color)
ax.set_ylim(0.9999, 1.0001)
ax.set_xlim(0.9999, 1.0001)
ax.axis('off')
plt.savefig("subfig-crys_color.pdf")
