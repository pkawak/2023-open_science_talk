#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Tue June 14 08:41:00 2021

@author: pierrekawak
"""

import matplotlib.pyplot as plt
import sys

fig, ax = plt.subplots(1, figsize=(0.4,0.2))
x = 0.0
y = 0.0
dx = 0.0
dy = -0.5
width = 0.6
head_length = 0.3
head_width = 1.2
ax.arrow(x, y, dx, dy, head_width=head_width, head_length=head_length, width=width, facecolor='g', edgecolor='k')
ax.set_xlim(-head_width/2, head_width/2+dx)
ax.set_ylim(dy-head_length-0.03, 0.0+0.03)
ax.axis('off')
plt.savefig("fig-down_arrow.pdf", transparent=True)

fig, ax = plt.subplots(1, figsize=(0.3,0.3))
x = 0.0
y = 0.0
dx = 0.5
dy = 0.5
width = 0.6
head_length = 0.3
head_width = 1.2
ax.arrow(x, y, dx, dy, head_width=head_width, head_length=head_length, width=width, facecolor='g', edgecolor='k')
ax.set_xlim(-0.3,1.)
ax.set_ylim(-0.3,1.)
ax.axis('off')
plt.savefig("fig-diag_up_right_arrow.pdf", transparent=True)

fig, ax = plt.subplots(1, figsize=(0.3,0.2))
x = 0.0
y = 0.0
dx = 0.5
dy = 0.0
width = 0.6
head_length = 0.3
head_width = 1.2
ax.arrow(x, y, dx, dy, head_width=head_width, head_length=head_length, width=width, facecolor='g', edgecolor='k')
ax.set_ylim(-head_width/1.8, head_width/1.8)
ax.set_xlim(0.0-0.04, dx+head_length+0.04)
ax.axis('off')
plt.savefig("fig-right_arrow.pdf", transparent=True)

cm=1/2.54
fig, ax = plt.subplots(1, figsize=(1.664*cm,2.56*cm))
x = 0.0
y = 0.0
dx = 1.0
dy = 0.0
width = 1.2
head_length = 0.2*dx
head_width = width+0.5
ax.arrow(x, y, dx, dy, head_width=head_width, head_length=head_length, width=width, length_includes_head=True, facecolor='g', edgecolor='k')
ax.text(x+0.008, y-0.19, "Canonical""\n""Analysis", color='w', fontsize=9)
ax.axis('off')
ax.set_ylim(-0.85, 0.85)
ax.set_xlim(-0.01, dx+0.01)
plt.subplots_adjust(left=0.,bottom=0, right=1, top=1)
plt.savefig("fig-right_arrow_text.pdf", transparent=True)
