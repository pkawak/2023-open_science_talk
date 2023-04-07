#!/bin/bash

cd /home/pkawak/data/mcpc_data/2000x100x0.85/diff_Ts/
cat 0.5/canon_distro.out 1.0/canon_distro.out 1.5/canon_distro.out 2.0/canon_distro.out 2.5/canon_distro.out 3.0/canon_distro.out 3.5/canon_distro.out 4.0/canon_distro.out 4.5/canon_distro.out 5.0/canon_distro.out 5.5/canon_distro.out 6.0/canon_distro.out 6.5/canon_distro.out 7.0/canon_distro.out 7.5/canon_distro.out > combo_canon_distro.out
cd -
cp /home/pkawak/data/mcpc_data/2000x100x0.85/diff_Ts/combo_canon_distro.out wlmc_results.out
