#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 18:48:14 2020

@author: pierrekawak
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('tkagg')

initT = 140

time = []#np.linspace(0, total_time, total_time+1)
curr_time = 0
T = []#np.zeros(len(time))
for i in range(50):
  time.append(curr_time)
  T.append(initT)
  curr_time += 1

def addPoints(deltatime_max, inity, finaly,
              initx, finalx, time, T):
    deltay = finaly-inity
    for time_i in range(initx, finalx):
        time.append(time_i)
        T.append(-deltay*np.exp(-5.0/deltatime_max*(time_i-initx))+finaly)

delta_time = 400
deltatime_max = 200
finalT = 93
addPoints(deltatime_max, initT, finalT, curr_time, curr_time+delta_time, time, T)
curr_time += delta_time

time_black = time[:]
time_ph = time[:]
T1 = T[:]
T1_final = 132
T2 = T[:]
T2_final = 129
T3 = T[:]
T3_final = 126
T4 = T[:]
T4_final = 123

delta_time_melting = 300
delta_time_recryst = 400

deltatime_max = 30
delta_time = delta_time_melting
initT = 93
finalT = T1_final
addPoints(deltatime_max, initT, finalT, curr_time, curr_time+delta_time,
          time, T1)
curr_time += delta_time

deltatime_max = 300
delta_time = delta_time_recryst
initT = T1_final
finalT = 93
addPoints(deltatime_max, initT, finalT, curr_time, curr_time+delta_time,
          time, T1)
curr_time += delta_time

deltatime_max = 30
delta_time = delta_time_melting
initT = 93
finalT = T2_final
addPoints(deltatime_max, initT, finalT, curr_time, curr_time+delta_time,
          time_ph, T2)

deltatime_max = 300
delta_time = delta_time_recryst
initT = T2_final
finalT = 93
addPoints(deltatime_max, initT, finalT, curr_time, curr_time+delta_time,
          time_ph, T2)

deltatime_max = 30
delta_time = delta_time_melting
initT = 93
finalT = T3_final
addPoints(deltatime_max, initT, finalT, curr_time, curr_time+delta_time,
          time_ph, T3)

deltatime_max = 300
delta_time = delta_time_recryst
initT = T3_final
finalT = 93
addPoints(deltatime_max, initT, finalT, curr_time, curr_time+delta_time,
          time_ph, T3)

deltatime_max = 30
delta_time = delta_time_melting
initT = 93
finalT = T4_final
addPoints(deltatime_max, initT, finalT, curr_time, curr_time+delta_time,
          time_ph, T4)

deltatime_max = 300
delta_time = delta_time_recryst
initT = T4_final
finalT = 93
addPoints(deltatime_max, initT, finalT, curr_time, curr_time+delta_time,
          time_ph, T4)

time_black2 = []
T_2 = []
delta_time = 200
initT = 93
finalT = 93
addPoints(deltatime_max, initT, finalT, curr_time, curr_time+delta_time,
          time_black2, T_2)

pt_in     = 1/72
figsize_x = 159*0.95
figsize_y = 243*0.5
fontsize  = 9
fig = plt.figure(figsize=(figsize_x*pt_in, figsize_y*pt_in))
ax = fig.add_subplot(111)

ax.plot([0, 1150], [110, 110], c='r', ls='--')
plt.text(1050, 113, r"$T_{m}$", c='r', fontsize=fontsize)
ax.plot([0, 1150], [93 , 93 ], c='c', ls='--')
plt.text(1050, 96 , r"$T_{c}$", c='c', fontsize=fontsize)

ax.plot(time       , T1 , c='k')
ax.plot(time_black , T  , c='k')
ax.plot(time_black2, T_2, c='k')

#plt.text(140, 105, "Complete"        , fontsize=fontsize)
#plt.text(140, 101, "Crystall-"       , fontsize=fontsize)
#plt.text(170, 97 , "ization"         , fontsize=fontsize)
plt.text(520, 134, r"$T_{\mathrm{Anneal}}$", fontsize=fontsize)
#plt.text(460, 128, r"> $T_{m}$"       , fontsize=fontsize)
#plt.text(840, 105, "Recrysta-", fontsize=fontsize)
#plt.text(890, 97, r"at $T_c$"       , fontsize=fontsize)
#plt.text(-90, 92, r"$T_c$"          , fontsize=fontsize)

ax.set_xlim(0, 1150)
ax.set_ylim(85, 143)

ax.set_xticks([])
ax.set_yticks([])

ax.set_xlabel('time'       , fontsize=fontsize, labelpad=-1)
ax.set_ylabel('Temperature', fontsize=fontsize, labelpad=1)

plt.subplots_adjust(left=0.087, right=0.995, bottom=0.08, top=0.995)

fig.savefig('fig-cryst_cycle.pdf')
