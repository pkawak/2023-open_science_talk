#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Sat May 22 08:41:00 2021

@author: pierrekawak
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

phi_reg = np.array([0.379, 0.407, 0.428, 0.438, 0.471])
T_reg   = np.array([0.2262, 0.2480, 0.2633, 0.2907, 0.3736])

# the linregress fit line of data
slope, intercept, r_value, p_value, std_err = stats.linregress(phi_reg, T_reg)
phi_min = 0.35
phi_max = 0.55
phi_line = np.linspace(phi_min, phi_max, 1000)
T_line   = phi_line*slope + intercept

# spline fit
model = np.poly1d(np.polyfit(phi_reg, T_reg, 3))
phi_quad = phi_line
T_quad = model(phi_quad)
#min_T_id = np.argmin(T_quad)
#T_min = T_quad[min_T_id]
#print(min_T_id, T_quad[np.argmin(T_quad)], phi_quad[np.argmin(T_quad)])
#T_quad[0:min_T_id] = T_min

phi_scat = phi_reg
T_scat   = T_reg

phi_trip = 0.428

T_min = 0.0
T_max = 0.6
test = 0
fig, ax = plt.subplots(1, figsize=(4.50, 2.92), constrained_layout=test)

# paint regions
phi_below=[]
i = 0
region_1 = np.linspace(T_min, model(phi_trip), 100)
for i in range(len(region_1)):
  if region_1[i] < T_quad[0]:
    phi_below.append(0.35)
  else:
    idx = (np.abs(T_quad-region_1[i])).argmin()
   # print(region_1[i], idx, T_quad[idx])
    phi_below.append(phi_quad[idx])
ax.fill_between(region_1, phi_below, phi_trip, color=['#FFC947'], alpha=0.7)
ax.text(0.04, 0.17, 'Nematic (N)', weight='bold', color='g', fontsize=12, fontname='dejavusans', transform = ax.transAxes)

phi_below_2=[]
i = 0
region_2 = np.linspace(T_min, T_max, 100)
for i in range(len(region_2)):
  if region_2[i] < T_quad[0]:
    phi_below_2.append(phi_trip)
  else:
    idx = (np.abs(T_quad-region_2[i])).argmin()
    phi_quad_i = phi_quad[idx]
    if phi_quad_i < phi_trip:
      phi_below_2.append(phi_trip)
    else:
      phi_below_2.append(phi_quad_i)
ax.fill_between(region_2, phi_below_2, phi_max, color=['#185ADB'], alpha=0.5)
ax.text(0.60, 0.40 , 'Isotropic (I)'   , weight='bold', color='r', fontsize=12, fontname='dejavusans', transform = ax.transAxes)

ax.fill_between(T_quad, phi_min, phi_quad, color=['#EFEFEF'], alpha=0.5)
ax.text(0.21, 0.71, 'Crystal (C)', weight='bold', color='b', fontsize=12, fontname='dejavusans', transform = ax.transAxes)

#like S and P
T_SandP = np.linspace(0.01,0.6,1000)
th_s = np.arccos(0.9) #stepwise stiffness cutoff
th_m = 2.*np.pi/3. #max theta due to hard core restrictions
l = 1.0 #bond length
N = 10 #chain length
cos_theta_avg = 0.5*(np.exp(1./T_SandP)*np.sin(th_s)**2 + np.cos(th_s)**2 - np.cos(th_m)**2) / (np.exp(1./T_SandP)*(1-np.cos(th_s)) + np.cos(th_s) - np.cos(th_m)) #formula for thermal average for an isolated bond angle doi:10.1103/PhysRevE.97.042501
lk_by_l = ( (1+cos_theta_avg)/(1-cos_theta_avg) - 2./(N-1.) * (1-cos_theta_avg**(N-1))/(1-cos_theta_avg)**2 )
phi_SandP = 1.4/lk_by_l
#ax.plot(T_SandP, phi_SandP, color='m', ls=':', alpha=0.7, label='Shakirov and Paul')

ax.plot(T_quad, phi_quad, color='k', zorder=1)
ax.plot([T_min, model(phi_trip)], [phi_trip, phi_trip], ls='--', color='k', zorder=1, label="$\phi_{\mathrm{crit}}$")
ax.scatter(T_scat[phi_scat >= phi_trip], phi_scat[phi_scat >= phi_trip], marker='*', s=50, color='m', zorder=2, label="$T_{IC}$")
ax.scatter(T_scat[phi_scat < phi_trip] , phi_scat[phi_scat < phi_trip] , marker='o', color='m', zorder=2, label="$T_{IN}$")
ax.set_xlabel(r"Reduced Temperature, $T_{r}$", fontsize=12, labelpad=6)#, labelpad=0.3)
ax.set_ylabel(r"Volume Fraction, $\phi$", fontsize=12, labelpad=5.5)
ax.tick_params(axis='both', labelsize=10, pad=0)
ax.set_xlim(T_min, T_max)
ax.set_ylim(phi_min, phi_max)
ax.set_yticks([0.35, 0.4, 0.45, 0.5, 0.55])
ax.legend(loc='lower right')
plt.subplots_adjust(left=0.137, top=0.98, bottom=0.147, right=0.977)
#plt.show()
#sys.exit()
plt.savefig("fig-phase_diag.pdf")
plt.close()
