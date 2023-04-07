#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Fri Apr 24 08:41:00 2022

@author: pierrekawak
"""

import pandas as pd
fytas_r2g_file_name   = "Fytas_Theo_r2g.out"
df_fytas_r2g = pd.read_csv(fytas_r2g_file_name, delimiter=" ", header=0)
df_fytas_r2g = df_fytas_r2g.sort_values(by = ['lambda', 'Temp'])
df_fytas_r2g_1p12 = df_fytas_r2g.loc[df_fytas_r2g['lambda'] == 1.12]
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6,4), constrained_layout=True)
Temp_ = df_fytas_r2g_1p12['Temp'].to_numpy()
r2g_  = df_fytas_r2g_1p12['r2g'].to_numpy()
r2g_orig = r2g_
ax.plot(Temp_, r2g_, label='0')
for i in [9]:
  r2g_  = gaussian_filter1d(r2g_orig, sigma=i)
  ax.plot(Temp_, r2g_, label=str(i))
  diff = r2g_ - r2g_orig
  diff /= r2g_orig
  diff = np.square(diff)
  diff = np.sqrt(diff)
  diff *= 100
  diff_tot = np.sum(diff)/len(diff)
  print(i, diff_tot)
  sorted_index_array = np.argsort(diff)
  sorted_diff = diff[sorted_index_array]
  sorted_Temp = Temp_[sorted_index_array]
  sorted_r2g_o = r2g_orig[sorted_index_array]
  sorted_r2g = r2g_[sorted_index_array]
#  print(sorted_diff)
#  print(sorted_diff[-10:])
  n = 3
  [ print( T, r, o, d ) for T,r,o,d in zip(sorted_Temp[-n:], sorted_r2g[-n:], sorted_r2g_o[-n:], sorted_diff[-n:]) ]
  if i == 15:
    for ii in range(n):
      iii = (ii+1)
     # print(sorted_Temp[-(i+1)])
      ax.vlines(sorted_Temp[-iii], 0, sorted_r2g[-iii])
    
 # ax.vlines(
ax.set_xlabel(r"$T$")
ax.set_ylabel(r"$\left<R^{2}_{g}\right>/\sigma^{2}$")
ax.legend(loc='best')
fig.savefig("sigmas.png")
