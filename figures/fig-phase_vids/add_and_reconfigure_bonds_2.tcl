
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

pbc box -off
mol delete all

set ii 0
foreach i $argv {
  puts $ii
  if { $ii == 0 } {
    set file_name $i
  } else {
    if { $ii == 1 } {
      set type $i
    } else {
      set orient $i
    }
  }
  set ii [expr $ii+1]
}

mol new $file_name autobonds 0 type xyz
mol modstyle top top $type
if { $file_name == "melt.xyz" } {
  mol modcolor top top "ColorID" 255
}
if { $file_name == "nematic.xyz" } {
  mol modcolor top top "ColorID" 27
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
axes Location off

auto_add_bonds 0 $Nc $Nb $Lx

# z axis is default orientation
# for x axis:
if { $orient == "x" } {
  rotate y by -90
}
# for y axis
if { $orient == "y" } {
  rotate x by 90
  rotate z by 90
}

unset Nc
unset Nb

##set periodic box size (-all applies to all frames)
#set Lx_a "$Lx $Lx $Lx"
#pbc set "$Lx_a" -all
#pbc box -center origin

#render Tachyon tmp.dat "/home/pkawak/data/VMD_TESTS/vmd-1.9.4a43/lib/tachyon/tachyon_LINUXAMD64" tmp.dat -format BMP -o "tmp.bmp"
render POV3 test.pov povray +W1000 +H1000 -I%s -O"tmp.tga" +X +A +FT +UA
quit
