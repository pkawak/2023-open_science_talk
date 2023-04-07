#!/bin/bash

dirss="../p290729_bugfix_mw2/ ../p290729_bugfix_2_mw2/ ../p290729_bugfix_3_mw2/"
for i in ${dirss}
do
  cd $i;
  echo "checking $i"
  grep error exp/slurm*;
  grep error exp/*/slurm*;
  cd -;
done;
