#!/usr/bin/env python3

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=6.5in,paperheight=4.1in]{geometry}
\\usepackage{graphicx}
\\usepackage[dvipsnames]{xcolor}
\\usepackage{tikz}
\\newcommand{\mylabel}[1]{%
  \\begin{tikzpicture}
    \\node[rounded corners=2pt, align=center, inner sep=1.5pt]{\\large{#1}};
  \\end{tikzpicture}%
  }
\\newcommand{\mymeltlabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill={rgb:red,151;green,32;blue,53}, rounded corners=2pt, align=center, inner sep=1.5pt]{{\\textcolor{white}{\\large{#1}}}};
  \\end{tikzpicture}%
  }
\\newcommand{\mynematiclabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill={rgb:red,255;green,98;blue,17}, rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{white}{\\large{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\mycrystlabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill={rgb:red,159;green,174;blue,105}, rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{white}{\\large{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\myxlabel}[1]{%
  \\begin{tikzpicture}
    \\node[rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{red}{\\normalsize{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\myylabel}[1]{%
  \\begin{tikzpicture}
    \\node[rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{green}{\\normalsize{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\myzlabel}[1]{%
  \\begin{tikzpicture}
    \\node[rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{blue}{\\normalsize{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\yourxlabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill=white, rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{red}{\\normalsize{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\yourylabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill=white, rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{green}{\\normalsize{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\yourzlabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill=white, rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{blue}{\\normalsize{#1}}};
  \\end{tikzpicture}%
  }

%Font
\\usepackage{DejaVuSans}
\\renewcommand*\\familydefault{\sfdefault}
\\usepackage[T1]{fontenc}
 
%Document
\\begin{document}
\\setlength{\\unitlength}{1.0in}
\\centering
\\begin{picture}(6.5,4.1)
  \\put(4.42, 2.5 ){\\includegraphics[trim={490 1220 440 1000}, clip, scale=0.038]{configs_lowT/cryst.png}}
  \\put(4.82, 2.7  ){\\yourxlabel{x}}
  \\put(4.57, 2.6  ){\\yourylabel{y}}
  \\put(4.77, 2.45  ){\\yourzlabel{z}}
  \\put(4.62, 2.5) {\\includegraphics[trim={700 700 3550 3667}, clip, scale=0.038]{configs_lowT/axes.png}}
  \\put(2.25, 2.5 ){\\includegraphics[trim={490 1220 490 1230}, clip, scale=0.038]{configs_lowT/nematic.png}}
  \\put(2.65, 2.7  ){\\yourxlabel{x}}
  \\put(2.40, 2.6  ){\\yourylabel{y}}
  \\put(2.60, 2.45  ){\\yourzlabel{z}}
  \\put(2.45, 2.5) {\\includegraphics[trim={700 700 3550 3667}, clip, scale=0.038]{configs_lowT/axes.png}}
  \\put(0.07, 2.5 ){\\includegraphics[trim={490 1220 490 1230}, clip, scale=0.038]{configs_lowT/melt.png}}
  \\put(0.40, 2.7  ){\\yourxlabel{x}}
  \\put(0.15, 2.6  ){\\yourylabel{y}}
  \\put(0.35, 2.45  ){\\yourzlabel{z}}
  \\put(0.2, 2.5  ){\\includegraphics[trim={700 700 3550 3667}, clip, scale=0.038]{configs_lowT/axes.png}}
  \\put(4.85, 0.00 ){\\includegraphics[]{structs/subfig-cryst.x.y1.z1.3D.dat.pdf}}
  \\put(5.35, 1.25 ){\\includegraphics[]{structs/subfig-cryst.x1.y.z1.3D.dat.pdf}}
  \\put(4.3, 1.25 ){\\includegraphics[]{structs/subfig-cryst.x1.y1.z.3D.dat.pdf}}
  \\put(2.675, 0.00 ){\\includegraphics[]{structs/subfig-nematic.x.y1.z1.3D.dat.pdf}}
  \\put(3.2, 1.25 ){\\includegraphics[]{structs/subfig-nematic.x1.y.z1.3D.dat.pdf}}
  \\put(2.15, 1.25 ){\\includegraphics[]{structs/subfig-nematic.x1.y1.z.3D.dat.pdf}}
  \\put(0.525, 0.00 ){\\includegraphics[]{structs/subfig-melt.x.y1.z1.3D.dat.pdf}}
  \\put(1.05, 1.25 ){\\includegraphics[]{structs/subfig-melt.x1.y.z1.3D.dat.pdf}}
  \\put(0.0, 1.25 ){\\includegraphics[]{structs/subfig-melt.x1.y1.z.3D.dat.pdf}}
  \\put(0.7, 3.9 ){\\mymeltlabel{(a) Melt}}
  \\put(0.3, 3.6 ){\\mymeltlabel{i}}
  \\put(0.15, 2.2 ){\\mymeltlabel{ii}}
  \\put(1.2, 2.2 ){\\mymeltlabel{iii}}
  \\put(0.675, 0.95 ){\\mymeltlabel{iv}}
  \\put(2.8, 3.9 ){\\mynematiclabel{(b) Nematic}}
  \\put(2.4, 3.6 ){\\mynematiclabel{i}}
  \\put(2.3, 2.2 ){\\mynematiclabel{ii}}
  \\put(3.35, 2.2 ){\\mynematiclabel{iii}}
  \\put(2.825, 0.95 ){\\mynematiclabel{iv}}
  \\put(5.0, 3.9 ){\\mycrystlabel{(c) Crystal}}
  \\put(4.6, 3.6 ){\\mycrystlabel{i}}
  \\put(4.45, 2.2 ){\\mycrystlabel{ii}}
  \\put(5.5, 2.2 ){\\mycrystlabel{iii}}
  \\put(5.0, 0.95 ){\\mycrystlabel{iv}}
\\end{picture}
\\end{document}
"""
)
f1.close();

#    \\put(0.05, 4.72){(a)}
#    \\put(0.05, 2.27){(b)}

subprocess.run(['pdflatex', basename+'.tex'])
subprocess.run(['rm', basename+'.tex', basename+'.aux', basename+'.log'])

#pdflatex $name.tex
#rm $name.tex $name.aux $name.log
#

