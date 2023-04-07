#!/usr/bin/env python3

import os
import numpy as np
import json

def get_immediate_subdirs(a_dir):
    return [ name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name)) ]

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

lnf_str = ""
dirs = get_immediate_subdirs(os.getcwd())
for direc in dirs:
  os.chdir(direc)
  dirs2 = get_immediate_subdirs(os.getcwd())
  for dir2 in dirs2:
    os.chdir(dir2)
    dirs3 = get_immediate_subdirs(os.getcwd())
    for dir3 in dirs3:       
      #print(direc + " " + dir2 + " " + dir3)
      os.chdir(dir3)
      rangel = dir2.split("_")[1]
      rangeh = dir2.split("_")[2]
      lnf_str += rangel + " " + rangeh + " "
      for i in range(14):
        file_name = "lng" + str(i) + ".out"
        if os.path.exists(file_name):
          f = open(file_name)
          lines = f.readlines()
          f.close()
          lnf = lines[0].split()[28][:-1]
          try:
            float(lnf)
          except ValueError:
            lnf = lines[0].split()[25][:-1]
          lnf = str(int(round(np.log2(1/float(lnf)))))
          lnf_str += " " + lnf
      file_name = "lng.out"
      if os.path.exists(file_name):
        f = open(file_name)
        lines = f.readlines()
        f.close()
        lnf = lines[0].split()[28][:-1]
        try:
          float(lnf)
        except ValueError:
          lnf = lines[0].split()[25][:-1]
        lnf = str(int(round(np.log2(1/float(lnf)))))
        lnf_str += " " + lnf
        time = lines[0].split()[-2]
        lnf_str += " " + time
      lnf_str += "\n"
      os.chdir("../")
    os.chdir("../")
  os.chdir("../")

lnf_list = lnf_str.split("\n")
lnf_list_sorted = sorted(lnf_list)
lnf_str_sorted = "\n".join(lnf_list_sorted)
f = open("lng_summary.out","w")
f.write(lnf_str_sorted)
f.close()
