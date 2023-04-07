#!/usr/bin/env python3

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=6.5in,paperheight=4.9in]{geometry}
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
\\begin{picture}(6.5,4.9)
  \\put(0.00, 2.45 ){\\includegraphics[]{subfig-speedup_nom_real.pdf}}
  \\put(3.25, 2.45 ){\\includegraphics[]{subfig-speedup_threads.pdf}}
  \\put(0.00, 0.00 ){\\includegraphics[]{subfig-speedup_ratio_nom_real.pdf}}
  \\put(3.25, 0.00 ){\\includegraphics[]{subfig-speedup_efficiency.pdf}}
  \\put(-0.03, 2.25 ){\\mylabel{(c)}}
  \\put(-0.03, 4.70 ){\\mylabel{(a)}}
  \\put(3.21, 2.25 ){\\mylabel{(d)}}
  \\put(3.21, 4.70 ){\\mylabel{(b)}}
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

