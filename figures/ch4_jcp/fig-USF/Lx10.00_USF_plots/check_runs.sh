#!/bin/bash

dirss="../p373627_bugfix_mw2/ ../p373627_bugfix_2_mw2/ ../p373627_bugfix_3_mw2/"
for i in ${dirss}
do
  cd $i;
  echo "checking $i"
  grep error exp/slurm*;
  grep error exp/*/slurm*;
  cd -;
done;
