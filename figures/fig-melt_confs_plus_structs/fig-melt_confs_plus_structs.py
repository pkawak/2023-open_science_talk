#!/usr/bin/env python

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=5.96in,paperheight=3.3676in]{geometry}
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
    \\node[fill={rgb:red,1;green,0;blue,0}, rounded corners=2pt, align=center, inner sep=1.5pt]{{\\textcolor{white}{\\LARGE{#1}}}};
  \\end{tikzpicture}%
  }
\\newcommand{\mynematiclabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill={rgb:red,0;green,100;blue,0}, rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{white}{\\LARGE{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\mycrystlabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill={rgb:red,0;green,0;blue,1}, rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{white}{\\LARGE{#1}}};
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
\\begin{picture}(5.96,3.2)
  \\put(0.30, 2.40 ){\\mymeltlabel{Melt $(\phi=0.471,T_{r}=2.0)$}}
  \\put(0.00, 0.10 ){\\includegraphics[trim={90 240 90 240}, clip, scale=0.29]{../configs_lowT/melt.png}}
  \\put(0.40, 0.38 ){\\yourxlabel{x}}
  \\put(0.13, 0.30 ){\\yourylabel{y}}
  \\put(0.35, 0.10 ){\\yourzlabel{z}}
  \\put(0.20, 0.15 ){\\includegraphics[trim={36 34 172 176}, clip]{../configs_lowT/axes.pdf}}
  \\put(3.34, 0.00){\\includegraphics[]{structs/subfig-melt.x.y1.z1.3D.dat.pdf}}
  \\put(4.66, 0.65 ){\\includegraphics[]{structs/subfig-melt.x1.y.z1.3D.dat.pdf}}
  \\put(3.34, 1.4 ){\\includegraphics[]{structs/subfig-melt.x1.y1.z.3D.dat.pdf}}
  \\put(4.86, 2.1 ){\\includegraphics[]{subfig-WLMC_P2_comp.pdf}}
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

