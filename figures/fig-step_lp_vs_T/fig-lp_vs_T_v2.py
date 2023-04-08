#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Sat May 22 08:41:00 2021

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from scipy.interpolate import make_interp_spline

l = 1.0 #bond length
N = 10 #chain length

#theoretical lp
T = np.linspace(0.01,1.0,10000)
th_s = np.arccos(0.9) #stepwise stiffness cutoff
th_m = math.pi#2.*np.pi/3. #max theta due to hard core restrictions
cosT = 0.5*(np.exp(1./T)*np.sin(th_s)**2 + np.cos(th_s)**2 - np.cos(th_m)**2) / (np.exp(1./T)*(1-np.cos(th_s)) + np.cos(th_s) - np.cos(th_m)) #formula for thermal average for an isolated bond angle doi:10.1103/PhysRevE.97.042501
lp = 0.5 * l * ( (1+cosT)/(1-cosT) )

##get cos_theta data
#data = np.loadtxt("cosTvsT.avg.out")
#df = pd.DataFrame({
#                   'T':    [ float(d) for d in data[:, 0] ],
#                   'cosT': [ float(d) for d in data[:, 1] ]
#                   })
#res = df.groupby(['T']).mean().reset_index()
#sem = df.groupby(['T']).sem().reset_index()

#get lp data
data = np.loadtxt("lpvsT.avg.out")
df = pd.DataFrame({
                   'T': [ float(d) for d in data[:, 0] ],
                   'lp':    [ float(d) for d in data[:, 1] ]
                   })
res = df.groupby(['T']).mean().reset_index()
sem = df.groupby(['T']).sem().reset_index()

#print("idx", "T_data", "-lp_data+", "T_fit", "lp_fit")
#for i in range(len(res['T'])):
#  idx = find_nearest(T, res['T'][i])
#  print(i, res['T'][i], res['lp'][i]-1.96*sem['lp'][i], "<", res['lp'][i], "<", res['lp'][i]+1.96*sem['lp'][i], T[idx], lp[idx])

fig, ax = plt.subplots(1, figsize=(2.5,1.8))
#plt.plot(T, -1/np.log(cosT), label=r"$\frac{-1}{\ln(\cos\theta)}$")
ax.plot(T, lp, label=r"$\frac{1}{2}\frac{1+\cos\theta}{1-\cos\theta}$")
ax.errorbar(res["T"], res["lp"], yerr=sem["lp"], fmt='.', color='m')
ax.set_yscale('log')
ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=6)
ax.set_ylabel(r"$l_{p}/\sigma$", fontsize=10, labelpad=3)
ax.tick_params(axis='both', labelsize=8)
#plt.legend(loc='best')
plt.subplots_adjust(left=0.21, top=0.99, bottom=0.23, right=0.985)

#plt.show()
#sys.exit()
plt.savefig("fig-lp_vs_T.pdf")
plt.close()
