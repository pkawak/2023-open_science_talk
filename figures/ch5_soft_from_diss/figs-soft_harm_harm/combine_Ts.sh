#!/bin/bash

echo file kb Lx Tm I Em Tm2 I2 Em2 > Ts.out

# get Ts.out files
Ts_files=$(ls *WLMC_Ts.out)

for file_ in ${Ts_files[@]}; do
  kb=$(echo $file_ | cut -d'_' -f2 | cut -d'b' -f2)
  Lx=$(echo $file_ | cut -d'_' -f1 | cut -d'x' -f2)
  line1=$(tail -n1 $file_ | head -n1)
  if [[ "$line1" == "Ts, Peak Strengths and Energies: " ]]; then
    line1="0 0 0"
  fi
  line2=$(tail -n2 $file_ | head -n1)
  if [ "$line2" = "Ts, Peak Strengths and Energies: " ]; then
    line2="0 0 0"
  fi
  echo $file_ $kb $Lx $line1 $line2  >> Ts.out
done
