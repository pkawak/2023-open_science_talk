#!/usr/bin/env python

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=3.25in,paperheight=3.1in]{geometry}
\\usepackage{graphicx}
\\usepackage[dvipsnames]{xcolor}
\\usepackage{tikz}
\\newcommand{\mylabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill=MidnightBlue, text=white, rounded corners=2pt, align=center, inner sep=1.5pt]{\\small{#1}};
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
\\begin{picture}(3.25,3.1)
  \\put(0.0, 0.0 ){\\includegraphics[]{subfig-phase_diag.pdf}}
  \\put(0.45, 0.3 ){\\includegraphics[scale=0.18]{configs/nem.png}}
  \\put(0.76, 1.7 ){\\includegraphics[scale=0.18]{configs/cryst.png}}
  \\put(1.88, 0.7 ){\\includegraphics[scale=0.18]{configs/melt.png}}
%  \\put(0.01, 1.45 ){\\mylabel{(a)}}
%  \\put(1.67, 0.0 ){\\includegraphics[]{subfig-Q6_melting_10.25.pdf}}
%  \\put(1.61, 1.45 ){\\mylabel{(b)}}
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

