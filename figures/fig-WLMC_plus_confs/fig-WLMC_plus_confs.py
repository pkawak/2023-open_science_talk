#!/usr/bin/env python

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=5.3in,paperheight=2.85in]{geometry}
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
\\begin{picture}(5.3,2.85)
  \\put(0.0, 0.0) {\\includegraphics[]{subfig-WLMC_10.25_10.75.pdf}}
  \\put(3.7, 2.70 ){\\includegraphics[]{subfig-melt_color.pdf}}
  \\put(3.8, 1.95 ){\\includegraphics[trim={90 240 90 240}, clip, scale=0.117]{../configs_lowT/melt.png}}
  \\put(3.7, 1.75 ){\\includegraphics[]{subfig-nema_color.pdf}}
  \\put(3.8, 1.00 ){\\includegraphics[trim={90 240 90 240}, clip, scale=0.117]{../configs_lowT/nematic.png}}
  \\put(3.7, 0.80 ){\\includegraphics[]{subfig-crys_color.pdf}}
  \\put(3.8, 0.05 ){\\includegraphics[trim={90 240 90 240}, clip, scale=0.117]{../configs_lowT/cryst.png}}
%  \\put(0.7, 3.9 ){\\mymeltlabel{(a) Melt}}
%  \\put(2.8, 3.9 ){\\mynematiclabel{(b) Nematic}}
%  \\put(5.0, 3.9 ){\\mycrystlabel{(c) Crystal}}
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

