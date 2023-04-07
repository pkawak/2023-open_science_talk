#!/usr/bin/env python3

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=6.8in,paperheight=7.8in]{geometry}
\\usepackage{graphicx}
\\usepackage[dvipsnames]{xcolor}
\\usepackage{tikz}
\\newcommand{\mylabel}[1]{%
  \\begin{tikzpicture}
    \\node[rounded corners=2pt, align=center, inner sep=1.5pt]{\\large{#1}};
  \\end{tikzpicture}%
  }
\\newcommand{\myrotlabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill={rgb:red,255;green,98;blue,17}, rotate=90, rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{white}{\\large{#1}}};
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

%Font
\\usepackage{DejaVuSans}
\\renewcommand*\\familydefault{\sfdefault}
\\usepackage[T1]{fontenc}
 
%Document
\\begin{document}
\\setlength{\\unitlength}{1.0in}
\\centering
\\begin{picture}(6.7,7.7)
  \\put(0.25, 6.0 ){\\includegraphics[]{subfig-kb_0.1-Lx_11.000.pdf}}
  \\put(0.25, 4.5 ){\\includegraphics[]{subfig-kb_1.0-Lx_11.000.pdf}}
  \\put(0.25, 3.0 ){\\includegraphics[]{subfig-kb_10.-Lx_11.000.pdf}}
  \\put(1.875, 6.0 ){\\includegraphics[]{subfig-kb_0.1-Lx_11.436.pdf}}
  \\put(1.875, 4.5 ){\\includegraphics[]{subfig-kb_1.0-Lx_11.436.pdf}}
  \\put(1.875, 3.0 ){\\includegraphics[]{subfig-kb_10.-Lx_11.436.pdf}}
  \\put(3.5, 6.0 ){\\includegraphics[]{subfig-kb_0.1-Lx_13.000.pdf}}
  \\put(3.5, 4.5 ){\\includegraphics[]{subfig-kb_1.0-Lx_13.000.pdf}}
  \\put(3.5, 3.0 ){\\includegraphics[]{subfig-kb_10.-Lx_13.000.pdf}}
  \\put(5.125, 6.0 ){\\includegraphics[]{subfig-kb_0.1-Lx_15.000.pdf}}
  \\put(5.125, 4.5 ){\\includegraphics[]{subfig-kb_1.0-Lx_15.000.pdf}}
  \\put(5.125, 3.0 ){\\includegraphics[]{subfig-kb_10.-Lx_15.000.pdf}}
  \\put(-0.03, 3.50 ){\\myrotlabel{$k_{b}=10$}}
  \\put(-0.03, 5.00 ){\\myrotlabel{$k_{b}=1$}}
  \\put(-0.03, 6.5 ){\\myrotlabel{$k_{b}=0.1$}}
  \\put(0.90, 7.5 ){\\mycrystlabel{$\phi=0.492$}}
  \\put(2.60, 7.5 ){\\mycrystlabel{$\phi=0.438$}}
  \\put(4.20, 7.5 ){\\mycrystlabel{$\phi=0.298$}}
  \\put(5.80, 7.5 ){\\mycrystlabel{$\phi=0.194$}}
  \\put(0.25, 1.5 ){\\includegraphics[]{subfig-Lx_11.000.pdf}}
  \\put(1.875, 1.5 ){\\includegraphics[]{subfig-Lx_11.436.pdf}}
  \\put(3.5, 1.5 ){\\includegraphics[]{subfig-Lx_13.000.pdf}}
  \\put(5.125, 1.5 ){\\includegraphics[]{subfig-Lx_15.000.pdf}}
  \\put(0.25, 0.0 ){\\includegraphics[]{subfig-kb_0.1.pdf}}
  \\put(1.875, 0.0 ){\\includegraphics[]{subfig-kb_1.0.pdf}}
  \\put(3.5, 0.0 ){\\includegraphics[]{subfig-kb_10..pdf}}
  \\put(1.250, 0.5 ){\\mynematiclabel{$k_{b}=0.1$}}
  \\put(2.875, 0.5 ){\\mynematiclabel{$k_{b}=1$}}
  \\put(4.500, 0.5 ){\\mynematiclabel{$k_{b}=10$}}
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

