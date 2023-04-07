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

Nc    = 125
Nb    = 10
sigma = 1.0
label_prefix = r'$\phi=$'

WL_A_file = "../Lx11.000_kb10.0_WLMC_Ts.out"
WL_B_file = "../Lx11.436_kb10.0_WLMC_Ts.out"
WL_C_file = "../Lx13.000_kb10.0_WLMC_Ts.out"
WL_D_file = "../Lx15.000_kb10.0_WLMC_Ts.out"
Lx_A      = 11.000
Lx_B      = 11.436
Lx_C      = 13.000
Lx_D      = 15.000
phi_A     = np.round(Nc*Nb*sigma**3/Lx_A**3*np.pi/6, 3)
phi_B     = np.round(Nc*Nb*sigma**3/Lx_B**3*np.pi/6, 3)
phi_C     = np.round(Nc*Nb*sigma**3/Lx_C**3*np.pi/6, 3)
phi_D     = np.round(Nc*Nb*sigma**3/Lx_D**3*np.pi/6, 3)
kb_A      = 10.0
kb_B      = 10.0
kb_C      = 10.0
kb_D      = 10.0

T_IN_reg = []
T_IC_reg = []
T_A = peak_A = E_A = []
T_B = peak_B = E_B = []
T_C = peak_C = E_C = []
T_D = peak_D = E_D = []
Ts_data_A = np.loadtxt(WL_A_file, skiprows=1)
if len(Ts_data_A) > 0:
  T_A       = Ts_data_A[:,0]
  T_A       /= kb_A
  peak_A    = Ts_data_A[:,1]
  E_A       = Ts_data_A[:,2]
  if len(T_A) == 2:
    T_IN_reg.append(T_A[1])
    T_IC_reg.append(T_A[0])
  elif len(T_A) == 1:
    T_IN_reg.append(T_A[0])
Ts_data_B = np.loadtxt(WL_B_file, skiprows=1)
if len(Ts_data_B) > 0:
  T_B       = Ts_data_B[:,0]
  T_B       /= kb_B
  peak_B    = Ts_data_B[:,1]
  E_B       = Ts_data_B[:,2]
  if len(T_B) == 2:
    T_IN_reg.append(T_B[1])
    T_IC_reg.append(T_B[0])
  elif len(T_B) == 1:
    T_IN_reg.append(T_B[0])
Ts_data_C = np.loadtxt(WL_C_file, skiprows=1, ndmin=2)
if len(Ts_data_C) > 0:
  T_C       = Ts_data_C[:,0]
  T_C       /= kb_C
  peak_C    = Ts_data_C[:,1]
  E_C       = Ts_data_C[:,2]
  if len(T_C) == 2:
    T_IN_reg.append(T_C[1])
    T_IC_reg.append(T_C[0])
  elif len(T_C) == 1:
    T_IN_reg.append(T_C[0])
Ts_data_D = np.loadtxt(WL_D_file, skiprows=1, ndmin=2)
if len(Ts_data_D) > 0:
  T_D       = Ts_data_D[:,0]
  T_D       /= kb_D
  peak_D    = Ts_data_D[:,1]
  E_D       = Ts_data_D[:,2]
  if len(T_D) == 2:
    T_IN_reg.append(T_D[1])
    T_IC_reg.append(T_D[0])
  elif len(T_D) == 1:
    T_IN_reg.append(T_D[0])

phi_reg  = [ phi_A, phi_B, phi_C, phi_D ]
phi_IN_reg = phi_reg[:len(T_IN_reg)]
phi_IC_reg = phi_reg[:len(T_IC_reg)]

phi_min = phi_D
phi_max = 0.64 #phi_A+0.2

#slope, intercept, r_value, p_value, std_err = stats.linregress(phi_IN_reg, T_IN_reg)
#phi_IN_line = np.linspace(phi_min, phi_max, 1000)
#T_IN_line   = phi_line*slope + intercept
#
#slope, intercept, r_value, p_value, std_err = stats.linregress(phi_IC_reg, T_IC_reg)
#phi_IC_line = np.linspace(phi_min, phi_max, 1000)
#T_IC_line   = phi_line*slope + intercept
#
model_IN = np.poly1d(np.polyfit(phi_IN_reg, T_IN_reg, 3))
phi_IN_quad = np.linspace(phi_min, phi_max, 1000)
T_IN_quad = model_IN(phi_IN_quad)

model_IC = np.poly1d(np.polyfit(phi_IC_reg, T_IC_reg, 3))
phi_IC_quad = np.linspace(phi_min, phi_max, 1000)
T_IC_quad = model_IC(phi_IC_quad)

#min_T_id = np.argmin(T_quad)
#Tmin = T_quad[min_T_id]
#print(min_T_id, T_quad[np.argmin(T_quad)], phi_quad[np.argmin(T_quad)])
#T_quad[0:min_T_id] = Tmin

phi_IN_scat = phi_IN_reg
T_IN_scat   = T_IN_reg
phi_IC_scat = phi_IC_reg
T_IC_scat   = T_IC_reg

Tmin = 0.0
Tmax = 0.2
fig, ax = plt.subplots(1, figsize=(3.25,3.1))

phi_below=[]
i = 0
region_1 = np.linspace(Tmin, Tmax, 100)
for i in range(len(region_1)):
  idx = (np.abs(T_IC_quad-region_1[i])).argmin()
  phi_below.append(phi_IC_quad[idx])
ax.fill_between(region_1, phi_below, phi_max, color=['#FFC947'], alpha=0.7)

phi_below_2=[]
phi_above_2=[]
i = 0
region_2 = np.linspace(Tmin, Tmax, 100)
for i in range(len(region_2)):
  idx = (np.abs(T_IN_quad-region_2[i])).argmin()
  phi_below_2.append(phi_IN_quad[idx])
  idx = (np.abs(T_IC_quad-region_2[i])).argmin()
  phi_above_2.append(phi_IC_quad[idx])
ax.fill_between(region_2, phi_below_2, phi_above_2, color=['#185ADB'], alpha=0.5)

ax.fill_between(T_IN_quad, phi_min, phi_IN_quad, color=['#EFEFEF'], alpha=0.5)

##like S and P
#T_SandP = np.linspace(0.01,0.6,1000)
#th_s = np.arccos(0.9) #stepwise stiffness cutoff
#th_m = 2.*np.pi/3. #max theta due to hard core restrictions
#l = 1.0 #bond length
#N = 10 #chain length
#cos_theta_avg = 0.5*(np.exp(1./T_SandP)*np.sin(th_s)**2 + np.cos(th_s)**2 - np.cos(th_m)**2) / (np.exp(1./T_SandP)*(1-np.cos(th_s)) + np.cos(th_s) - np.cos(th_m)) #formula for thermal average for an isolated bond angle doi:10.1103/PhysRevE.97.042501
#lk_by_l = ( (1+cos_theta_avg)/(1-cos_theta_avg) - 2./(N-1.) * (1-cos_theta_avg**(N-1))/(1-cos_theta_avg)**2 )
#phi_SandP = 1.4/lk_by_l
#ax.plot(T_SandP, phi_SandP, color='m', ls=':', alpha=0.7, label='Shakirov and Paul')

ax.plot(T_IN_quad, phi_IN_quad, color='g', label="IN", zorder=1)
ax.plot(T_IC_quad, phi_IC_quad, color='r', label="IC", zorder=1)
#ax.plot([Tmin, model(phi_trip)], [phi_trip, phi_trip], ls='--', color='#00008b', zorder=1)
ax.scatter(T_IN_scat, phi_IN_scat, color='g', label="IN", zorder=2)
ax.scatter(T_IC_scat, phi_IC_scat, color='r', label="IC", zorder=2)
ax.set_xlabel(r"$T_{r}$", fontsize=10, labelpad=6)#, labelpad=0.3)
ax.set_ylabel(r"$\phi$", fontsize=10, labelpad=5.5)
ax.tick_params(axis='both', labelsize=8)
ax.set_xlim(Tmin, Tmax)
ax.set_ylim(phi_min, phi_max)
#ax.set_yticks([0.35, 0.4, 0.45, 0.5, 0.55])
ax.text(0.68, 0.25 , 'Melt'   , weight='bold', color='k', fontsize=12, fontname='dejavusans', transform = ax.transAxes)
ax.text(0.15, 0.80, 'Crystal', weight='bold', color='k', fontsize=12, fontname='dejavusans', transform = ax.transAxes)
ax.text(0.04, 0.35, 'Nematic', weight='bold', color='k', fontsize=12, fontname='dejavusans', transform = ax.transAxes)
plt.subplots_adjust(left=0.18, top=0.98, bottom=0.135, right=0.974)
#plt.show()
#sys.exit()
plt.savefig("fig-phase_diag.pdf")
plt.close()
