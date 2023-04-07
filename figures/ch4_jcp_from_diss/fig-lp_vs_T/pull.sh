#!/bin/bash

rsync pkawak@ssh.fsl.byu.edu:/fslhome/pkawak/data/mcpc_data/SandPlike/Lx10.00/phant_chain_TSweeps/alt.py \
:/fslhome/pkawak/data/mcpc_data/SandPlike/Lx10.00/phant_chain_TSweeps/*.avg.out \
.

chmod u+x *.py;
