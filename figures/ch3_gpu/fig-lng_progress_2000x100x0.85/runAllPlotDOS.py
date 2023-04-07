#!/usr/bin/env python3

import os 

for i in range(14):
  file_name = "lng" + str(i) + ".out"
  os.system("./plotDOS_var.py " + file_name)
os.system("./plotDOS_var.py lng.out")
