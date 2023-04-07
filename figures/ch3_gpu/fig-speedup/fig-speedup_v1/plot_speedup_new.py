#!/usr/bin/env python3

import sys

Nb = 100
rho = 0.15
sigma = 1
rc = 2.5

in_file = "sp_metrics.out"

import pandas as pd
pd.set_option("display.precision", 16)

df = pd.read_csv(in_file, sep=" ")

# average out reps
df = df.groupby( ['mode', 'Nc'] ).mean().reset_index()
df['acc'] = df['numb_succ']/df['numb_try']
df['time_per_succ'] = df['time_per_step']*df['numb_try']/df['numb_succ']
df['Lx'] = (df['Nc']*Nb/rho) ** (1/3)
df['ncell'] = (df['Lx']/rc).astype('int')
for i in range(len(df['ncell'])):
  while (df['ncell'].iloc[i]/2 % 2) == 1:
    df['ncell'].iloc[i] -= 1
df['rcell'] = df['Lx']/df['ncell']
df['proc'] = (df['ncell']/2) ** 3

# split into parallel and serial
df_par = df.loc[df['mode'] == "par"]
df_ser = df.loc[df['mode'] == "ser"]

# use this to simplify plotting interesting stuff
toPlot = [['time_per_step', 'numb_try', 'acc'], ['auto_time_sec', 'Emean', 'conv_crit']]
x = 'Nc'
scale  = [['log', 'linear', 'linear'], ['linear', 'linear', 'linear']]
import matplotlib.pyplot as plt
fig, axes = plt.subplots(nrows=3,ncols=2,figsize=(12,12), constrained_layout=True)
for j in [0,1]:
  for i,ax in enumerate(axes[:,j]):
    ax.scatter(df_par['Nc'], df_par[toPlot[j][i]],label="par")
    ax.scatter(df_ser['Nc'], df_ser[toPlot[j][i]],label="ser")
    ax.set_xlabel(r'$N_{c}$ $(N/100)$')
    ax.set_ylabel(toPlot[j][i])
    ax.set_yscale(scale[j][i])
    ax.legend(loc='best')
fig.savefig('fig-sp_metrics.png')
plt.close()

# calculate speedup measures
import numpy as np
Nc = df_ser['Nc'].to_numpy()
sp_nom  = df_ser['time_per_step'].to_numpy()/df_par['time_per_step'].to_numpy()
sp_succ = df_ser['time_per_succ'].to_numpy()/df_par['time_per_succ'].to_numpy()
sp_auto = df_ser['auto_time_sec'].to_numpy()/df_par['auto_time_sec'].to_numpy()

fig, ax = plt.subplots(figsize=(2.95,2.95), constrained_layout=True)
ax.scatter(Nc, sp_nom, label='nominal')
ax.scatter(Nc, sp_succ, label='success')
ax.scatter(Nc, sp_auto, label='real')
ax.set_yscale('log')
ax.set_xscale('log')
#ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.set_xlabel(r'$N_{c}$ $(N/100)$')
ax.set_ylabel(r'$S_{p}$')
ax.legend(loc='best')
#plt.show()
fig.savefig('fig-sp_nom_real.png')
fig.savefig('fig-sp_nom_real.pdf')
plt.close()

fig, ax = plt.subplots(figsize=(2.95,2.95), constrained_layout=True)
ax.scatter(Nc, sp_auto/sp_nom)
ax.set_xscale('log')
ax.set_xlabel(r'$N_{c}$ $(N/100)$')
ax.set_ylabel(r'$S_{p}^{\mathrm{auto}}/S_{p}^{\mathrm{nom}}$')
fig.savefig('fig-ratio_nom_real.png')
fig.savefig('fig-ratio_nom_real.pdf')
plt.close()

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(5.9,2.95), constrained_layout=True)
axes[0].scatter(Nc, df_par['proc'])
axes[0].set_xlabel(r'$N_{c}$ $(N/100)$')
axes[0].set_ylabel(r'proc (number of threads)')
axes[1].scatter(df_par['proc'], sp_nom, label='nominal')
axes[1].scatter(df_par['proc'], sp_succ, label='success')
axes[1].scatter(df_par['proc'], sp_auto, label='real')
#axes[1].text(1792, (axes[1].get_ylim()[0]+axes[1].get_ylim()[1])/2*0.05, r"$proc_{\mathrm{Pascal}}=1792$")
#axes[1].autoscale(enable=False, axis='y')
axes[1].vlines(1792, axes[1].get_ylim()[0], axes[1].get_ylim()[1], ls='dashed', label=r"$proc^{\mathrm{Pa}}=1792$")
axes[1].set_yscale('log')
axes[1].set_xscale('log')
axes[1].set_xlabel(r'proc (number of threads)')
axes[1].set_ylabel(r'$S_{p}$')
axes[1].legend(loc='best')
#plt.show()
fig.savefig('fig-speedup_threads_combo.png')
fig.savefig('fig-speedup_threads_combo.pdf')
plt.close()

fig, axes = plt.subplots(figsize=(2.95,2.95), constrained_layout=True)
axes.scatter(Nc, df_par['proc'])
axes.set_xlabel(r'$N_{c}$ $(N/100)$')
axes.set_ylabel(r'proc (number of threads)')
fig.savefig('fig-thread_NC.png')
fig.savefig('fig-thread_NC.pdf')
plt.close()

fig, axes = plt.subplots(figsize=(2.95,2.95), constrained_layout=True)
axes.scatter(df_par['proc'], sp_nom, label='nominal')
axes.scatter(df_par['proc'], sp_succ, label='success')
axes.scatter(df_par['proc'], sp_auto, label='real')
#axes.vlines(1792, axes.get_ylim()[0], axes.get_ylim()[1], ls='dashed', label=r"$proc^{\mathrm{Pa}}=1792$")
axes.set_yscale('log')
axes.set_xscale('log')
axes.set_xlabel(r'proc (number of threads)')
axes.set_ylabel(r'$S_{p}$')
axes.legend(loc='best')
#plt.show()
fig.savefig('fig-speedup_threads.png')
fig.savefig('fig-speedup_threads.pdf')
plt.close()


fig, ax = plt.subplots(figsize=(2.95,2.95), constrained_layout=True)
ax.scatter(df_par['proc'], sp_nom/df_par['proc'], label='nominal')
ax.scatter(df_par['proc'], sp_succ/df_par['proc'], label='success')
ax.scatter(df_par['proc'], sp_auto/df_par['proc'], label='real')
#ax.set_yscale('log')
ax.set_xscale('log')
#ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.set_xlabel(r'$N_{c}$ $(N/100)$')
ax.set_ylabel(r'$E_{p}=S_{p}/p$')
ax.legend(loc='best')
#plt.show()
fig.savefig('fig-efficiency_threads.png')
fig.savefig('fig-efficiency_threads.pdf')
plt.close()

#I still need tmp-fig-mem_time.png
# tmp-fig-pascal_comp.png  tmp-fig-serial_fract.png    tmp-fig-sp_nom_real.png
