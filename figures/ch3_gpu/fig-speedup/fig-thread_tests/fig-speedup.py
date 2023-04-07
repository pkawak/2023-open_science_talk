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

ylim1 = 1
ylim2 = 70

cmap = plt.get_cmap("tab10")
test = 0
fig, ax = plt.subplots(figsize=(6,5), constrained_layout=test)
#ax.scatter(Nc, df_par['proc']/32, color=cmap(0), s=100, label=r'$S_{p}^{\mathrm{try}}$')
#ax.scatter(Nc, df_par['proc']/32, color=cmap(2), s=100, label=r'$S_{p}^{\mathrm{success}}$')
#ax.scatter(Nc, df_par['proc']/32, color=cmap(3), s=100, label=r'$S_{p}^{\mathrm{auto}}$')
ax.scatter(Nc, sp_nom , color=cmap(0), s=100, label=r'$S_{p}^{\mathrm{try}}$')
ax.scatter(Nc, sp_succ, color=cmap(2), s=100, label=r'$S_{p}^{\mathrm{success}}$')
ax.scatter(Nc, sp_auto, color=cmap(3), s=100, label=r'$S_{p}^{\mathrm{auto}}$')
print(Nc)
print(df_par['proc']/32)

def returnbandgDim(proc):
  bdim=6
  while proc%bdim != 0:
    bdim -= 2
  gdim = proc/bdim
  return bdim, gdim

bdim = np.zeros(len(Nc))
gdim = np.zeros(len(Nc))
for i in range(len(df_par['proc'])):
  bdim[i], gdim[i] = returnbandgDim(df_par['proc'].iat[i])
print(bdim)
print(gdim)
print(gdim/32)

ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlabel(r'$N_{c}$', fontsize=fontsize)
ax.set_ylabel(r'$S_{p}$', fontsize=fontsize)#, labelpad=-5)
ax.legend(loc='upper left', fontsize=fontsize, ncol=2, columnspacing=1.0)
#ax.set_yticks([1,10])
#ax.set_ylim([ylim1, ylim2])
#Nclim1 = 80
#Nclim2 = 12000
#ax.set_xlim(80, 12000)
ax.tick_params(axis='both', labelsize=fontsize, pad=0)
if test == 0:
  plt.subplots_adjust(left=0.099, bottom=0.085, right=0.999, top=0.987)
fig.savefig('fig-speedup.pdf')
plt.close()
