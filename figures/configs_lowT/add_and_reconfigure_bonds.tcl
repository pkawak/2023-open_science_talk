
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

pbc box -off

mol delete all
set file_name $argv 
mol new $file_name autobonds 0 type xyz
mol modstyle top top CPK 0.3

#read params.json file to get box dims
package require json
set fp [open "params.json" r]
set param_json [read $fp]
close $fp
unset $fp
set param_dict [::json::json2dict $param_json]
set Lx [dict get $param_dict Lx]
set Nc [dict get $param_dict Nc]
set Nb [dict get $param_dict Nb]
unset $param_dict
unset $param_json

#set c_id 0
#for {set nc 0} {$nc < $Nc} {incr nc} {
#  for {set i 0} {$i < $Nb} {incr i} {
#    puts "color: $c_id"
#    set nb [expr $nc*$Nb+$i];
#    mol modcolor top $nb "ColorID" $c_id
#    incr c_id
#  }
#}

mol modcolor top 0 "ColorID" 255
color Display Background white
color Display BackgroundTop white
color Display BackgroundBot white
axes Location off
rotate y by 70
#rotate z by 30
#rotate x by 20

#add bonds to 0, 1; 1, 2; 2, 3; etc.
for {set nc 0} {$nc < $Nc} {incr nc} {
  for {set i 0} {$i < $Nb-1} {incr i} {
    set nb [expr $nc*$Nb+$i];
    set nbp1 [expr 1+$nb];
    topo addbond $nb $nbp1;
  }
}

#shows you colors and their ids
#set i 0
#foreach color [colorinfo colors] {
#  puts "$i $color"
#  incr i
#}
unset $Nc
unset $Nb
    
#remove bonds that wrap around the box
set Lby2 [expr $Lx/2.]
remove_long_bonds $Lby2

#set periodic box size (-all applies to all frames)
#set Lx_a "$Lx $Lx $Lx"
#pbc set "$Lx_a" -all
#pbc box -center origin
 
#make_rotation_animated_gif $file_name
#
#render Tachyon tmp.dat "/home/pkawak/VMD_TESTS/vmd-1.9.4a43/lib/tachyon/tachyon_LINUXAMD64" -format BMP -o "$file_name.bmp"
#render POV3 test.pov povray +W1000 +H1000 -I%s -O"$file_name.tga" +X +A +FT +UA
#quit
