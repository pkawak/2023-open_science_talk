#!/bin/bash

rsync pkawak@ssh.fsl.byu.edu:/fslhome/pkawak/data/mcpc_data/sandbox/rep_Nikolaos_Fytas/lambda_1.12/Lx_20/MCMC/plot* plotMC.py
rsync pkawak@ssh.fsl.byu.edu:/fslhome/pkawak/data/mcpc_data/sandbox/rep_Nikolaos_Fytas/lambda_1.12/Lx_20/MCMC/summ.out mcmc_results.out
cp /home/pkawak/data/mcpc_data/sandbox/rep_Nikolaos_Fytas/lambda_1.12/Lx_20/better_wmw2/ext_canon_distro.out wlmc_results.out
