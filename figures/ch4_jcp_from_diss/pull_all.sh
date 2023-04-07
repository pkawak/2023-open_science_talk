#!/bin/bash

#for dir in fig-pathway_1*/
for dir in fig-FELs_all/ fig-pathway_1*/ fig-heights_vs_phi/ fig-FELs_all_sim/
do
  cd $dir
#  pwd
  chmod u+x pull.sh
  ./pull.sh
  for subfig in subfig*.py; 
  do
    chmod u+x $subfig
    ./$subfig
  done
  for fig in fig*.py; 
  do
    chmod u+x $fig
    ./$fig
  done
  cp fig*.pdf ../../manuscript/;
  cd ../;
done
