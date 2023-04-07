#!/usr/bin/env python3

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=3.25in,paperheight=8.0in]{geometry}
\\usepackage{graphicx}
\\usepackage[dvipsnames]{xcolor}
\\usepackage{tikz}
\\newcommand{\mylabel}[1]{%
  \\begin{tikzpicture}
    \\node[rounded corners=2pt, align=center, inner sep=1.5pt]{\\large{#1}};
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
\\begin{picture}(3.25,8.0)
  \\put(0.0, 0.0 ){\\includegraphics[]{subfig-WLMC.pdf}}
  \\put(-0.03, 2.02 ){\\mylabel{(d)}}
  \\put(-0.03, 3.95 ){\\mylabel{(c)}}
  \\put(-0.03, 5.9 ){\\mylabel{(b)}}
  \\put(-0.03, 7.82 ){\\mylabel{(a)}}
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

