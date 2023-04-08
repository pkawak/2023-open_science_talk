#!/bin/bash


sed -i 's/Lx": 10.5/Lx": 10.0/g' params.json
for i in melt cryst; do
  vmd -e add_and_reconfigure_bonds_2.tcl -args $i.xyz "VDW 0.35" x ; mv tmp.tga $i-vdw-x.tga
  vmd -e add_and_reconfigure_bonds_2.tcl -args $i.xyz "Licorice 0.4 12 12" x ; mv tmp.tga $i-licorice-x.tga
  vmd -e add_and_reconfigure_bonds_2.tcl -args $i.xyz "Licorice 0.4 12 12" z ; mv tmp.tga $i-licorice-z.tga
done

sed -i 's/Lx": 10.0/Lx": 10.5/g' params.json
for i in nematic; do
  vmd -e add_and_reconfigure_bonds_2.tcl -args $i.xyz "VDW 0.35" x ; mv tmp.tga $i-vdw-x.tga
  vmd -e add_and_reconfigure_bonds_2.tcl -args $i.xyz "Licorice 0.4 12 12" x ; mv tmp.tga $i-licorice-x.tga
  vmd -e add_and_reconfigure_bonds_2.tcl -args $i.xyz "Licorice 0.4 12 12" z ; mv tmp.tga $i-licorice-z.tga
done

vmd -e save_axis.tcl
for j in *.tga; do
  jj=$(echo $j | cut -d'.' -f1)
  convert $j ${jj}.png;
done;
rm *.tga
rm test.pov

