#!/bin/bash

rsync pkawak@ssh.fsl.byu.edu:/fslhome/pkawak/data/mcpc_data/gradual_hoyification/phantom_chains_all/harm_step_kappa_sweep/avg-* .
#:/fslhome/pkawak/data/mcpc_data/SandPlike/Lx10.00/phant_chain_TSweeps/*.avg.out \

cp ../fig-step_lp_vs_T/avg-cos_theta_backbone.out noharm_avg-cos_theta_backbone.out
cp ../fig-step_lp_vs_T/avg-lpvsT.out noharm_avg-lpvsT.out
