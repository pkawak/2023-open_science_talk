#!/bin/bash

dirss="../p2263_bugfix_redesign_mw2/ ../p22635_bugfix_redesign_mw2/ ../p22637_bugfix_redesign_mw2/"
for i in ${dirss}
do
  cd $i;
  echo "checking $i"
  grep error exp/slurm*;
  grep error exp/*/slurm*;
  cd -;
done;
