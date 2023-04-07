#!/usr/bin/env python

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=9.0in,paperheight=6.5in]{geometry}
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
\\begin{picture}(9.0,6.5)
  \\put(0.075,0.00 ){\\includegraphics[]{subfig-FEL_p438_sim.pdf}}
  \\put(1.696,3.09 ){\\mylabel{(b) $\phi = 0.438$}}
  \\put(4.569,0.00 ){\\includegraphics[]{subfig-FEL_p407_sim.pdf}}
  \\put(6.162,3.09 ){\\mylabel{(d) $\phi = 0.407$}}
  \\put(5.815,3.32 ){\\includegraphics[]{subfig-FEL_p379_sim.pdf}}
  \\put(7.20,6.3 ){\\mylabel{(e) $\phi = 0.379$}}
  \\put(2.8,3.32 ){\\includegraphics[]{subfig-FEL_p428_sim.pdf}}
  \\put(4.2,6.3 ){\\mylabel{(c) $\phi = 0.428$}}
  \\put(-0.15,3.32 ){\\includegraphics[]{subfig-FEL_p471_sim.pdf}}
  \\put(1.2,6.3 ){\\mylabel{(a) $\phi = 0.471$}}
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

