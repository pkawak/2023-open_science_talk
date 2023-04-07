#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

Nb       = 100
rho      = 0.15
sigma    = 1
rc       = 2.5
fontsize = 12
in_file  = "sp_metrics.out"

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

# calculate speedup measures
Nc = df_ser['Nc'].to_numpy()
sp_nom  = df_ser['time_per_step'].to_numpy()/df_par['time_per_step'].to_numpy()
sp_succ = df_ser['time_per_succ'].to_numpy()/df_par['time_per_succ'].to_numpy()
sp_auto = df_ser['auto_time_sec'].to_numpy()/df_par['auto_time_sec'].to_numpy()

def returnThreads(Nc):
  return int( ( 100/2.5**3/0.15*Nc )**(1/3) )**3/8

def returnNc(threads):
  return 2.5**3 * 8 * threads * 0.15/100

ylim1 = 0
ylim2 = 1

cmap = plt.get_cmap("tab10")
test = 0
fig, ax = plt.subplots(figsize=(6,5), constrained_layout=test)
ax.scatter(Nc, sp_succ/sp_nom, color=cmap(2), s=100, label=r"$S_{p}^{\mathrm{success}}$")
ax.scatter(Nc, sp_auto/sp_nom, color=cmap(3), s=100, label=r"$S_{p}^{\mathrm{auto}}$")
ax.set_xscale('log')
ax.set_xlabel(r'$N_{c}$', fontsize=fontsize)
ax.set_ylabel(r'$S_{p}/S_{p}^{\mathrm{try}}$', fontsize=fontsize)
ax.set_yticks([0.0,0.2,0.4,0.6,0.8,1.0])
ax.legend(loc='best', fontsize=fontsize)
ax.set_ylim([ylim1, ylim2])
Nclim1 = 80
Nclim2 = 12000
ax.set_xlim(80, 12000)
ax.tick_params(axis='both', labelsize=fontsize, pad=0)

if test == 0:
  plt.subplots_adjust(left=0.102, bottom=0.085, right=0.999, top=0.987)
fig.savefig('fig-speedup.pdf')
plt.close()
