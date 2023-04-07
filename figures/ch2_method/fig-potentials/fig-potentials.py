#!/usr/bin/env python3

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=6.8in,paperheight=6.0in]{geometry}
\\usepackage{graphicx}
\\usepackage[dvipsnames]{xcolor}
\\usepackage{tikz}
\\newcommand{\mylabel}[1]{%
  \\begin{tikzpicture}
    \\node[text=black, inner sep=1.5pt]{\\large{#1}};
  \\end{tikzpicture}%
  }

\\newcommand{\mytransbox}[1]{%
  \\begin{tikzpicture}
    \\node[fill={rgb:red,1;green,1;blue,1},opacity=0.7]{\\large{#1}};
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
\\begin{picture}(6.8,6.0)
  \\put(0.010, 3.010){\\frame{\\includegraphics[scale=3.725]{fig-pairs/fig-pair_CG.pdf}}}
  \\put(3.000, 3.000){\\includegraphics[]{fig-pairs/fig-pairs.pdf}}
  \\put(0.000, 0.000){\\includegraphics[]{fig-bonds/fig-bonds.pdf}}
  \\put(3.400, 0.000){\\includegraphics[]{fig-angles/fig-angles.pdf}}
  \\put(0.000, 5.757){\\mytransbox{a)}}
  \\put(2.980, 5.757){\\mytransbox{b)}}
  \\put(0.000, 2.760){\\mytransbox{c)}}
  \\put(3.225, 2.760){\\mytransbox{d)}}
\\end{picture}
\\end{document}
"""
)
f1.close();

subprocess.run(['pdflatex', basename+'.tex'])
subprocess.run(['rm', basename+'.tex', basename+'.aux', basename+'.log'])
