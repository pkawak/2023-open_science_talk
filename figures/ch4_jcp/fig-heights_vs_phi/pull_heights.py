#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 17:32:10 2021

@author: pierrekawak
"""
import numpy as np
import matplotlib.pyplot as plt

dirnames = ["Lx10.00/p373627_avg_mw2/", "Lx10.25/p290729_avg_mw2/", "Lx10.33/p267_avg_mw2/", "Lx10.50/p247975_avg_mw2/", "Lx10.75/p22635_avg_mw2/"]
names    = [0.471, 0.438, 0.428, 0.407, 0.379]
start    = []
heights  = []
end      = []

for dir in dirnames:
  with open(dir+"heights.out", "r+") as f:
    height = f.readline().split(' ')
  start.append(float(height[0]))
  heights.append(float(height[1]))
  end.append(float(height[2]))

np.savetxt("heights_phi.out", np.c_[names, start, heights, end])
