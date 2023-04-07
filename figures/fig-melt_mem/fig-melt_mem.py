#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 18:48:14 2020

@author: pierrekawak
"""
import numpy as np
import matplotlib.pyplot as plt

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
T1_final = 125
T2 = T[:]
T2_final = 122
T3 = T[:]
T3_final = 119
T4 = T[:]
T4_final = 117

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

fig = plt.figure(figsize=(3.7,3))
ax = fig.add_subplot(111)
plt.xlabel('time'       , fontsize=12, labelpad=4)
plt.ylabel('Temperature', fontsize=12, labelpad=7)
plt.xticks([])

plt.subplots_adjust(left=0.17, right=0.99, bottom=0.07, top=0.99)

plt.plot(time, T1, c='r')
plt.plot(time, T2, c='y')
plt.plot(time, T3, c='g')
plt.plot(time, T4, c='b')

plt.plot(time_black, T, c='k')
plt.plot(time_black2, T_2, c='k')
plt.text(140, 105, "Complete"        , fontsize=12)
plt.text(140, 101, "Crystall-"       , fontsize=12)
plt.text(170, 97 , "ization"         , fontsize=12)
plt.text(460, 132, "Annealing"       , fontsize=12)
plt.text(460, 128, r"at $T_m$"       , fontsize=12)
plt.text(840, 105, "Recrysta-", fontsize=12)
plt.text(860, 101, "llization", fontsize=12)
plt.text(890, 97, r"at $T_c$"       , fontsize=12)
plt.text(-240, 92, r"$T_c=$"          , fontsize=12)

plt.xlim(0, 1150)
ax.set_yticks([93, 100, 110, 120, 130, 140])
#melt_img = mpimg.imread("colored_melt_mem.png")
#imagebox = OffsetImage(melt_img, zoom=0.15)
#ab = AnnotationBbox(imagebox, (1200, 140))
#ax.add_artist(ab)
#plt.grid()
#plt.draw()
##plt.plot(time, deltaT*np.exp(-time))
#plt.show()
fig.savefig('fig-melt_mem.pdf')
#fig.savefig('fig-melt_mem.png', dpi=1200)
