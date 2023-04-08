
proc remove_long_bonds { max_length } {
#this function removes bonds that span the box (periodic boundary conditions cause these bonds)
  set numframes [molinfo top get numframes]
  puts "this many frames $numframes"
  for { set frame_i 0 } { $frame_i < $numframes } { incr frame_i } {
    animate goto $frame_i
    for { set i 0 } { $i < [ molinfo top get numatoms ] } { incr i } {
      set bead [ atomselect top "index $i" ]
      set bonds [ lindex [$bead getbonds] 0 ]
      if { [ llength bonds ] > 0 } {
        set bonds_new {}
        set xyz [ lindex [$bead get {x y z}] 0 ]
        foreach j $bonds {
          set bead_to [ atomselect top "index $j" ]
          set xyz_to [ lindex [$bead_to get {x y z}] 0 ]
          if { [ vecdist $xyz $xyz_to ] < $max_length } {
            lappend bonds_new $j
          }
        }
        $bead setbonds [ list $bonds_new ]
      }
    }
  }
}

proc make_rotation_animated_gif {save_name} {
#makes an animated gif that's rotated around the y axis by 20 degrees every frame
  set frame 0
  for {set i 0} {$i < 360} {incr i 20} {
    set filename snap.[format "%04d" $frame].rgb
    render snapshot $filename
    incr frame
    rotate y by 20
  }
  exec convert -delay 100 -loop 4 snap.*.rgb $save_name.cpk.gif
  file delete {*}[glob -nocomplain snap.*.rgb]
  #rm snap.*.rgb
}

proc auto_add_bonds { num Nc Nb Lx } {
  mol top $num
  #add bonds to 0, 1; 1, 2; 2, 3; etc.
  for {set nc 0} {$nc < $Nc} {incr nc} {
    for {set i 0} {$i < $Nb-1} {incr i} {
      set nb [expr $nc*$Nb+$i];
      set nbp1 [expr 1+$nb];
      topo addbond $nb $nbp1;
    }
  }
  #remove bonds that wrap around the box
  set Lby2 [expr $Lx/2.]
  remove_long_bonds $Lby2
}

#read params.json file to get box dims
package require json
set fp [open "params.json" r]
set param_json [read $fp]
close $fp
unset fp
set param_dict [::json::json2dict $param_json]
set Lx [dict get $param_dict Lx]
set Nc [dict get $param_dict Nc]
set Nb [dict get $param_dict Nb]
unset param_dict
unset param_json

color Display Background white
color Display BackgroundTop white
color Display BackgroundBot white

pbc box -off
mol delete all

proc vizualize_all { type zeroth offx offy offz Nc Nb Lx } {
  mol new melt.xyz autobonds 0 type xyz
  mol modstyle top top $type
  mol modcolor top top "ColorID" 255

  mol new nematic.xyz autobonds 0 type xyz
  mol modstyle top top $type
  mol modcolor top top "ColorID" 27
  
  mol new cryst.xyz autobonds 0 type xyz
  mol modstyle top top $type
  
  set oneth [expr $zeroth+1]
  set twoth [expr $zeroth+2]
#  mol fix $oneth
#  mol fix $twoth
#  translate by -1.600000 0.000000 0.000000
#  mol fix $zeroth
#  mol free $twoth
#  translate by 1.600000 0.000000 0.000000
#  
#  mol free $zeroth
#  mol free $oneth
#  translate by $offx $offy $offz
#
#  mol fix $zeroth
#  mol fix $oneth
#  mol fix $twoth

  auto_add_bonds $zeroth $Nc $Nb $Lx
  auto_add_bonds $oneth $Nc $Nb $Lx
  auto_add_bonds $twoth $Nc $Nb $Lx
}

# points
set last 0

vizualize_all "CPK 0.6" $last 0 1.5 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "CPK 0.6" $last 0 1.5 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "CPK 0.6" $last 0 1.5 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "Lines 10" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "Lines 10" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "Lines 10" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "Bonds 0.3 12" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "Bonds 0.3 12" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "Bonds 0.3 12" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
#vizualize_all "DynamicBonds 1.1 0.3 12" $last 0 0 0 $Nc $Nb $Lx
#set last [expr $last+3]
vizualize_all "Points 2" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "Points 2" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "Points 2" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "Licorice 0.4 12 12" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "Licorice 0.4 12 12" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "Licorice 0.4 12 12" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
#vizualize_all "Polyhedra 1.300000" $last 0 0 0 $Nc $Nb $Lx
#set last [expr $last+3]
vizualize_all "Dotted 1 18" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "Dotted 1 18" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
vizualize_all "Dotted 1 18" $last 0 0 0 $Nc $Nb $Lx
set last [expr $last+3]
#vizualize_all "Solvent 0.000000 13.000000 1.000000" $last 0 0 0 $Nc $Nb $Lx
#set last [expr $last+3]
#vizualize_all "LatticeCubes 0.100000" $last 0 0 0 $Nc $Nb $Lx
#set last [expr $last+3]

set howmanytrios [expr $last/3]
mol fix all

set xsep 1.6
for {set molid 0} {$molid < $howmanytrios} {incr molid} { mol free [expr $molid*3] }
translate by -$xsep 0 0
for {set molid 0} {$molid < $howmanytrios} {incr molid} { mol fix [expr $molid*3] }

for {set molid 0} {$molid < $howmanytrios} {incr molid} { mol free [expr $molid*3+2] }
translate by $xsep 0 0
for {set molid 0} {$molid < $howmanytrios} {incr molid} { mol fix [expr $molid*3+2] }

proc move_three { zeroth offx offy offz } {
  set oneth [expr $zeroth+1]
  set twoth [expr $zeroth+2]
  mol free $zeroth
  mol free $oneth
  mol free $twoth
  translate by $offx $offy $offz
  mol fix $zeroth
  mol fix $oneth
  mol fix $twoth
}

set ysep 1.7
for {set molid 0} {$molid < $howmanytrios} {incr molid} { move_three [expr $molid*3] 0 [expr $ysep-$molid*$ysep] 0 }

set rotate 1

#mol fix all
#mol free 3
#mol free 3
#mol free 3
#rotate y by -90
#mol free all
#mol fix all
#mol free [expr 6+9*$molid]
#mol free [expr 6+9*$molid]
#mol free [expr 6+9*$molid]
#rotate x by 90
#rotate z by 90
#mol fix all
set howmanynines [expr $last/9]
for {set molid 0} {$molid < $howmanynines} {incr molid} {
  mol fix all
  mol free [expr 3+9*$molid]
  mol free [expr 4+9*$molid]
  mol free [expr 5+9*$molid]
  rotate y by -90
  mol free all
  mol fix all
  mol free [expr 6+9*$molid]
  mol free [expr 7+9*$molid]
  mol free [expr 8+9*$molid]
  rotate x by 90
  rotate z by 90
  mol fix all
}

mol fix all
rotate x by 180
mol free all

draw color red
draw text {0 5 8} "zax Dotted 1 18" size 10
draw text {11.2 5 8} "xax Dotted 1 18" size 10
draw text {22.4 5 8} "yax Dotted 1 18" size 10
draw text {33.6 5 8} "zax Licorice 0.4 12 12" size 10
draw text {44.8 5 8} "xax Licorice 0.4 12 12" size 10
draw text {56 5 8} "yax Licorice 0.4 12 12" size 10
draw text {67.2 5 8} "zax Points 2" size 10
draw text {78.4 5 8} "xax Points 2" size 10
draw text {89.6 5 8} "yax Points 2" size 10
draw text {100.8 5 8} "zax Bonds 0.3 12" size 10
draw text {112.0 5 8} "xax Bonds 0.3 12" size 10
draw text {123.2 5 8} "yax Bonds 0.3 12" size 10
draw text {134.4 5 8} "zax Lines 10" size 10
draw text {145.6 5 8} "xax Lines 10" size 10
draw text {156.8 5 8} "yax Lines 10" size 10
draw text {168.0 5 8} "zax CPK 0.6" size 10
draw text {179.2 5 8} "xax CPK 0.6" size 10
draw text {190.4 5 8} "yax CPK 0.6" size 10


unset Nc
unset Nb

#axes Location off
#rotate y by 70
#rotate z by 30
#rotate x by 20

#set periodic box size (-all applies to all frames)
for {set molid 0} {$molid < $last} {incr molid} {
  mol top $molid
  set Lx_a "$Lx $Lx $Lx"
  pbc set "$Lx_a" -all
  pbc box -center origin
}
#make_rotation_animated_gif $file_name
#
#render Tachyon tmp.dat "/home/pkawak/VMD_TESTS/vmd-1.9.4a43/lib/tachyon/tachyon_LINUXAMD64" -format BMP -o "$file_name.bmp"
#render POV3 test.pov povray +W1000 +H1000 -I%s -O"wtv.tga" +X +A +FT +UA
#quit
