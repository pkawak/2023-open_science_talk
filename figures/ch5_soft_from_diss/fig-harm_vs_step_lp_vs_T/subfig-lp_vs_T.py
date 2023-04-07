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

l  = 1.0 #bond length
N  = 10 #chain length
Nc = 125

step_lp_file_name       = "step_avg-lpvsT.out"
step_costheta_file_name = "step_avg-cos_theta_backbone.out"
step_Em_file_name       = "step_avg-EvsT.out"
harm_lp_file_name       = "harm_avg-lpvsT.out"
harm_costheta_file_name = "harm_avg-cos_theta_backbone.out"
harm_Em_file_name       = "harm_avg-EvsT.out"
filter_by = { "kb": 1.0 , "costheta_s": 0.9 }

# get lp data
step_lp_df               = pd.read_csv(step_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
step_lp_df['costheta_s'] = np.round(np.cos(step_lp_df['theta_s']),3)
step_lp_df               = step_lp_df.loc[(step_lp_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]
harm_lp_df               = pd.read_csv(harm_lp_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
harm_lp_df['costheta_s'] = 0.9
harm_lp_df               = harm_lp_df.loc[(harm_lp_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

# get cos_theta data
step_costheta_df               = pd.read_csv(step_costheta_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
step_costheta_df['costheta_s'] = np.round(np.cos(step_costheta_df['theta_s']),3)
step_costheta_df               = step_costheta_df.loc[(step_costheta_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]
harm_costheta_df               = pd.read_csv(harm_costheta_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
harm_costheta_df['costheta_s'] = 0.9
harm_costheta_df               = harm_costheta_df.loc[(harm_costheta_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

# get E data
step_Em_df               = pd.read_csv(step_Em_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
step_Em_df['costheta_s'] = np.round(np.cos(step_Em_df['theta_s']),3)
step_Em_df               = step_Em_df.loc[(step_Em_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]
harm_Em_df               = pd.read_csv(harm_Em_file_name, index_col=False, delimiter=" ", keep_default_na=False, na_values=['_'])
harm_Em_df['costheta_s'] = 0.9
harm_Em_df               = harm_Em_df.loc[(harm_Em_df[list(filter_by)] == pd.Series(filter_by)).all(axis=1)]

# filter out stuff with T > 1
step_lp_df       = step_lp_df.loc[step_lp_df['T'] < 1.01]
step_costheta_df = step_costheta_df.loc[step_costheta_df['T'] < 1.01]
step_Em_df       = step_Em_df.loc[step_Em_df['T'] < 1.01]
harm_lp_df       = harm_lp_df.loc[harm_lp_df['T'] < 1.01]
harm_costheta_df = harm_costheta_df.loc[harm_costheta_df['T'] < 1.01]
harm_Em_df       = harm_Em_df.loc[harm_Em_df['T'] < 1.01]

step_Em_df['Em'] = step_Em_df['Em']/Nc/(N-2)
step_Em_df['Em'] = step_Em_df['Em']+1
harm_Em_df['Em'] = harm_Em_df['Em']/Nc/(N-2)
step_Em_df['Em_se'] = step_Em_df['Em_se']/Nc/(N-2)
harm_Em_df['Em_se'] = harm_Em_df['Em_se']/Nc/(N-2)

figsize   = (2.5,1.8*3)
fontsize  = 10
labelsize = 8
fig, ax = plt.subplots(3, figsize=figsize, sharex=True, constrained_layout=True)

ax[0].set_ylabel(r"$\langle \cos\theta \rangle \left( s=0 \right)$", fontsize=fontsize, labelpad=7)
ax[0].errorbar(step_costheta_df["Tr"], step_costheta_df["costheta"], yerr=step_costheta_df["costheta_se"], fmt='.', color='m', label='stepwise')
ax[0].errorbar(harm_costheta_df["Tr"], harm_costheta_df["costheta"], yerr=harm_costheta_df["costheta_se"], fmt='.', color='b', label='harmonic')
ax[0].hlines(0.9, 0, 1, ls='--', color='k', label=r'$\cos\theta_{s}$')
ax[0].legend(loc='lower left', fontsize=labelsize, frameon=False, handlelength=1.8, handletextpad=0.3)
ax[0].set_yticks([0.0,0.2,0.4,0.6,0.8,1.0])
ax[0].tick_params(axis='both', labelsize=labelsize)
from matplotlib.ticker import ScalarFormatter, NullFormatter
ax[0].yaxis.set_major_formatter(ScalarFormatter())
ax[0].yaxis.set_minor_formatter(NullFormatter())

ax[1].set_ylabel(r"$\langle U \rangle / k_{b} N_{\mathrm{bonds}}$", fontsize=fontsize, labelpad=7)
ax[1].tick_params(axis='both', labelsize=labelsize)
ax[1].errorbar(step_Em_df["Tr"], step_Em_df["Em"], yerr=step_Em_df["Em_se"], fmt='.', color='m', label=r"$\langle U^{\mathrm{step}} \rangle / k_{b} N_{\mathrm{bonds}} + 1$")
ax[1].errorbar(harm_Em_df["Tr"], harm_Em_df["Em"], yerr=harm_Em_df["Em_se"], fmt='.', color='b', label=r"$\langle U^{\mathrm{harm}} \rangle / k_{b} N_{\mathrm{bonds}}$")
#ax[1].errorbar(step_Em_df["Tr"], np.exp(-step_Em_df["Em"]/step_Em_df["Tr"]), yerr=np.exp(-step_Em_df["Em_se"]/step_Em_df["Tr"]), fmt='.', color='m', label=r"$\langle U^{\mathrm{step}} \rangle / k_{b} N_{\mathrm{bonds}} + 1$")
#ax[1].errorbar(harm_Em_df["Tr"], np.exp(-harm_Em_df["Em"]/harm_Em_df["Tr"]), yerr=np.exp(-harm_Em_df["Em_se"]/harm_Em_df["Tr"]), fmt='.', color='b', label=r"$\langle U^{\mathrm{harm}} \rangle / k_{b} N_{\mathrm{bonds}}$")
ax[1].legend(loc='lower right', fontsize=labelsize, frameon=True, handlelength=1, handletextpad=0.1)
#ax[1].set_yscale('log')
#ax[0].set_xscale('log')
#ax[0].set_yticks([1,100])

ax[2].set_xlabel(r"$T_{r}$", fontsize=fontsize, labelpad=6)
ax[2].set_ylabel(r"$l_{p}/\sigma$", fontsize=fontsize, labelpad=2)
ax[2].tick_params(axis='both', labelsize=labelsize)
ax[2].errorbar(step_lp_df["Tr"], step_lp_df["lp"], yerr=step_lp_df["lp_se"], fmt='.', color='m')
ax[2].errorbar(harm_lp_df["Tr"], harm_lp_df["lp"], yerr=harm_lp_df["lp_se"], fmt='.', color='b')
ax[2].set_yscale('log')
#ax[1].set_yscale('log')
#ax[1].set_xscale('log')
#ax[1].set_yticks([0.3,1.0])
#ax[1].xaxis.set_major_formatter(ScalarFormatter())

T = np.linspace(0.01,1.0,10000)
th_m = math.pi#2.*np.pi/3. #max theta due to hard core restrictions

# theoretical lp
th_s = np.arccos(0.9) #stepwise stiffness cutoff
cosT = 0.5*(np.exp(1./T)*np.sin(th_s)**2 + np.cos(th_s)**2 - np.cos(th_m)**2) / (np.exp(1./T)*(1-np.cos(th_s)) + np.cos(th_s) - np.cos(th_m)) #formula for thermal average for an isolated bond angle doi:10.1103/PhysRevE.97.042501
lp = 0.5 * l * ( (1+cosT)/(1-cosT) )
ax[0].plot(T, cosT, color='m')#, label="Theory")
#ax[1].plot(T, U, color='m')
ax[2].plot(T, lp, color='m')#, label=r"$\frac{1}{2}\frac{1+\cos\theta}{1-\cos\theta}$")

Emin   = -Nc*(N-2)
Nangles = Nc*(N-2)
Erange = np.linspace(Emin, 0, -Emin+1, dtype=int)
Erangeplus = Erange-Emin
Erange = Erangeplus
#print(Erangeplus)

import gmpy2
from gmpy2 import mpfr

def Z_count(Ti):
  Zi = mpfr(0)
  for Ej in Erange:
    Zi += gmpy2.exp(-Ej/Ti)
  return(Zi)

def Combs(n,r):
  return(gmpy2.fac(n)/gmpy2.fac(n-r)/gmpy2.fac(r))

def Perms(n,r):
  return(gmpy2.fac(n)/gmpy2.fac(n-r))

def cosE(Ei):
  return(0.5*(np.cos(th_s)+1+Ei/Nangles*(np.cos(th_m)-1-2*np.cos(th_s))))

def cosT_count(Ti):
  cosi = mpfr(0)
  Zi = mpfr(0)
  for Ej in Erange:
#    print(Ej, Combs(Nangles, int(Ej)))
    Zj = gmpy2.exp(-Ej/Ti)*Combs(Nangles, int(Ej))
    cosj = cosE(Ej)
    cosi += mpfr(cosj * Zj)
    Zi += Zj
   # print(Ej, Zj, Ei, Zi)
   # sys.exit()
 # print(Zi)
  cosi = cosi/Zi
#  print("Ti:", Ti, "cosi", cosi, "Zi:", Zi)
  return(cosi)

def E_count(Ti):
  Ei = mpfr(0)
  Zi = mpfr(0)
  for Ej in Erange:
#    print(Ej, Combs(Nangles, int(Ej)))
    Zj = gmpy2.exp(-Ej/Ti)*Combs(Nangles, int(Ej))
    Ei += mpfr(Ej * Zj)
    Zi += Zj
   # print(Ej, Zj, Ei, Zi)
   # sys.exit()
 # print(Zi)
  Ei /= Zi
#  print("Ti:", Ti, "Ei", Ei, "Zi:", Zi)
  return(Ei)

#print(Combs(5,0))
#print(Combs(5,1))
#print(Combs(5,2))
#print(Combs(5,3))
#print(Combs(5,4))
#print(Combs(5,5))
#print(10000000000  , E_count(10000000000)+Emin)
#print(1/10000000000, E_count(1/10000000000)+Emin)
#print(10000000000  , cosT_count(10000000000))
#print(1/10000000000, cosT_count(1/10000000000))

#T_count = np.linspace(0.01,1.0,100)
#cosT_count = np.array( [ cosT_count(ti) for ti in T_count ] )
#E_count = np.array( [ E_count(ti) for ti in T_count ] )
#E_count = E_count/Nc/(N-2)
#E_count = E+1
#ax[0].plot(T_count, cosT_count, color='g', ls='-.')
#ax[1].plot(T_count, E_count, color='g', ls='-.')

# theoretical lp
#cosT = - T + ( - np.exp(1/T) + np.cos(th_m) * np.exp(-1/T * np.cos(th_m)) ) / ( np.exp(1/T) - np.exp(-1/T * np.cos(th_m)) )
cosT = ( np.cos(th_m) * np.exp(np.cos(th_m)/T) - np.exp(1/T) ) / ( np.exp(np.cos(th_m)/T) - np.exp(1/T) ) - T
#print(np.cos(th_m))
#print(cosT)
lp = 0.5 * l * ( (1+cosT)/(1-cosT) )
U = 1-cosT
ax[0].plot(T, cosT, color='b')#, label="Theory")
ax[1].plot(T, U, color='b')
ax[2].plot(T, lp, color='b')#, label=r"$\frac{1}{2}\frac{1+\cos\theta}{1-\cos\theta}$")


plt.savefig("subfig-lp_vs_T.pdf")
plt.close()
#if big:
#  plt.subplots_adjust(left=0.147, top=0.995, bottom=0.156, right=0.998)
#else:
#  plt.subplots_adjust(left=0.21, top=0.99, bottom=0.23, right=0.985)
