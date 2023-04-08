#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Sat May 22 08:41:00 2021

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

T = np.linspace(0.01,1.0,10000)
th_s = np.arccos(0.9) #stepwise stiffness cutoff
th_m = 2.*np.pi/3. #max theta due to hard core restrictions
l = 1.0 #bond length
N = 10 #chain length
cos_theta_avg = 0.5*(np.exp(1./T)*np.sin(th_s)**2 + np.cos(th_s)**2 - np.cos(th_m)**2) / (np.exp(1./T)*(1-np.cos(th_s)) + np.cos(th_s) - np.cos(th_m)) #formula for thermal average for an isolated bond angle doi:10.1103/PhysRevE.97.042501
lk_by_l = ( (1+cos_theta_avg)/(1-cos_theta_avg) - 2./(N-1.) * (1-cos_theta_avg**(N-1))/(1-cos_theta_avg)**2 )
lp_by_l = 0.5*lk_by_l
fig, ax = plt.subplots(1, figsize=(2.5,1.5))
ax.plot(T, lp_by_l)
ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=6)#, labelpad=0.3)
ax.set_ylabel(r"$l_{p}/\sigma$", fontsize=10, labelpad=6.5)
ax.tick_params(axis='both', labelsize=8)
plt.subplots_adjust(left=0.175, top=0.99, bottom=0.28, right=0.99)
#plt.show()
sys.exit()
#plt.savefig("fig-lp_vs_T.pdf")
plt.close()
