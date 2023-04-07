pbc box -off
mol delete all

mol modcolor top 0 "ColorID" 255
color Display Background white
color Display BackgroundTop white
color Display BackgroundBot white
color Axes Labels white
#axes Location off
rotate y by 70
#rotate z by 30
#rotate x by 20

render POV3 test.pov povray +W1000 +H1000 -I%s -O"axes.tga" +X +A +FT +UA
quit
