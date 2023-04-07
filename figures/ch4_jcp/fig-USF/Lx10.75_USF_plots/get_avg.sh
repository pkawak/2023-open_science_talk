#!/bin/bash

dirss="../p2263_bugfix_redesign_mw2/ ../p22635_bugfix_redesign_mw2/" # ../p22637_bugfix_redesign_mw2/"
dirssp=""
dirsspp=""
for i in ${dirss}
do
  cd $i;
  ~/git/opwl/tools/WL/PMF_anal/collect_all.sh;
  echo $(../../mule_impl.py; ../subfig-path*.py; ../subfig-2d*.py;) > /dev/null &
  dirssp+="${i}/lng_2d.out "
  dirsspp+="${i}/subfig-path*.pdf "
  cd -;
done;
../../accum_lngs_avg.py $dirssp
../../mule_impl.py ;
../subfig-pathway_*.py ;
../subfig-2d_barrier_*.py ;

pdfjam ${dirsspp} subfig-path*pdf --nup 3x1 --frame 'true' --landscape --outfile avg.pdf; 
evince avg.pdf
