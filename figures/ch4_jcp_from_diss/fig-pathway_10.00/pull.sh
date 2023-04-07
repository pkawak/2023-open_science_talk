#!/bin/bash

rsync pkawak@ssh.fsl.byu.edu:/fslhome/pkawak/data/opwl_data/sand_box/parallel_try/P2_SandP_like/after2d/Lx10.00/p373627_avg_mw2/*pathway* \
:/fslhome/pkawak/data/opwl_data/sand_box/parallel_try/P2_SandP_like/after2d/Lx10.00/p373627_avg_mw2/*barrier* \
:/fslhome/pkawak/data/opwl_data/sand_box/parallel_try/P2_SandP_like/after2d/Lx10.00/p373627_avg_mw2/params.json \
:/fslhome/pkawak/data/opwl_data/sand_box/parallel_try/P2_SandP_like/after2d/Lx10.00/p373627_avg_mw2/lng_2d.out \
:/fslhome/pkawak/data/opwl_data/sand_box/parallel_try/P2_SandP_like/after2d/Lx10.00/p373627_avg_mw2/MFEP_1d.out \
:/fslhome/pkawak/data/opwl_data/sand_box/parallel_try/P2_SandP_like/after2d/Lx10.00/p373627_avg_mw2/2d_plot_params.json \
:/fslhome/pkawak/data/opwl_data/sand_box/parallel_try/P2_SandP_like/after2d/Lx10.00/*barrier* \
:/fslhome/pkawak/data/opwl_data/sand_box/parallel_try/P2_SandP_like/after2d/Lx10.00/*pathway* \
.

chmod u+x *.py;
