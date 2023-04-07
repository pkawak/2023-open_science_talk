#!/bin/bash

sed -i 's/Lx": 10.5/Lx": 10.0/g' params.json
for i in melt.xyz cryst.xyz; do
  vmd -e add_and_reconfigure_bonds.tcl -args $i;
done

sed -i 's/Lx": 10.0/Lx": 10.5/g' params.json
for i in nematic.xyz; do
  vmd -e add_and_reconfigure_bonds.tcl -args $i;
done

for j in *.tga; do
  jj=$(echo $j | cut -d'.' -f1)
  convert -density 300 $j ${jj}.pdf;
done;

vmd -e save_axis.tcl
convert -density 300 axes.tga axes.pdf
