#!/usr/bin/env python3

import os
import sys
import numpy as np
import json
import matplotlib.pyplot as plt

def get_immediate_subdirs(a_dir):
    return [ name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name)) ]

Nc = []
MCPerSecA = []
Type = []
dirs = get_immediate_subdirs(os.getcwd())
for direc in dirs:
  os.chdir(direc)
  dirs2 = get_immediate_subdirs(os.getcwd())
  for dir2 in dirs2:
    os.chdir(dir2)
    dirs3 = get_immediate_subdirs(os.getcwd())
    for dir3 in dirs3:       
#      print(direc+"/"+dir2+"/"+dir3)
      os.chdir(dir3)
      with open("result.out", "r+") as f:
        MCPerSec = float(f.readlines()[1].split(' ')[1])
      Type.append(direc)
      MCPerSecA.append(MCPerSec)
      Nc.append(dir2)
      os.chdir("../")
    os.chdir("../")
  os.chdir("../")

#print(Nc)
#print(MCPerSecA)
#print(Type)
Nc_par = [nc for nc, type in zip(Nc, Type) if type == 'par']
MCPerSecA_par = [nc for nc, type in zip(MCPerSecA, Type) if type == 'par']
Nc_ser = [nc for nc, type in zip(Nc, Type) if type == 'ser']
MCPerSecA_ser = [nc for nc, type in zip(MCPerSecA, Type) if type == 'ser']

import pandas as pd
df_par = pd.DataFrame(list(zip(Nc_par, MCPerSecA_par)), columns = ['Nc', 'spd'])
df_ser = pd.DataFrame(list(zip(Nc_ser, MCPerSecA_ser)), columns = ['Nc', 'spd'])
df_par['Nc'] = df_par['Nc'].astype('int')
df_ser['Nc'] = df_ser['Nc'].astype('int')
df_par.sort_values('Nc')
df_ser.sort_values('Nc')
df_par = df_par.groupby('Nc').mean()
df_ser = df_ser.groupby('Nc').mean()
pd.set_option("display.precision", 8)
df_par = df_par.reset_index()
df_ser = df_ser.reset_index()
df = df_par
df['spd'] = df_ser['spd']/df_par['spd']
#print(df_par)
#print(df_ser)
#print(df)

fig, ax = plt.subplots()
ax.plot(df['Nc']*100, df['spd'])
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_yticks([10, 100])
ax.get_xaxis().get_major_formatter().labelOnlyBase = False
ax.set_xlabel('Number')
ax.set_ylabel('Speedup')
plt.show()
