#!/usr/bin/env python

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=6.5in,paperheight=5.4in]{geometry}
\\usepackage{graphicx}
\\usepackage[dvipsnames]{xcolor}
\\usepackage{tikz}
\\newcommand{\mylabel}[1]{%
  \\begin{tikzpicture}
    \\node[text=black, inner sep=1.5pt]{\\large{#1}};
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
\\begin{picture}(6.5,5.4)
  \\put(0.075,0.00 ){\\includegraphics[]{subfig-FEL_p438.pdf}}
  \\put(1.225,2.57 ){\\mylabel{(b) $\phi = 0.438$}}
  \\put(3.3,0.00 ){\\includegraphics[]{subfig-FEL_p407.pdf}}
  \\put(4.45,2.57 ){\\mylabel{(d) $\phi = 0.407$}}
  \\put(4.22,2.82 ){\\includegraphics[]{subfig-FEL_p379.pdf}}
  \\put(4.95,5.22 ){\\mylabel{(e) $\phi = 0.379$}}
  \\put(2.1,2.82 ){\\includegraphics[]{subfig-FEL_p428.pdf}}
  \\put(2.85,5.22 ){\\mylabel{(c) $\phi = 0.428$}}
  \\put(0.00,2.82 ){\\includegraphics[]{subfig-FEL_p471.pdf}}
  \\put(0.75,5.22 ){\\mylabel{(a) $\phi = 0.471$}}
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

