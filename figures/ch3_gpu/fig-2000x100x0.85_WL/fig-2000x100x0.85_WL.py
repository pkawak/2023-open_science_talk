#!/usr/bin/env python3

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=5.0in,paperheight=5.5in]{geometry}
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
\\begin{picture}(5.0,5.5)
%  \\put(0.1, 0.00 ){\\includegraphics[]{subfig-Cv_vs_T.pdf}}
%  \\put(0.1, 2.75 ){\\includegraphics[]{subfig-r2g_vs_T.pdf}}
%  \\put(0.1, 5.50 ){\\includegraphics[]{subfig-U_vs_T.pdf}}
  \\put(0.0, 0.0 ){\\includegraphics[]{subfig-2000x100x0.85_WL.pdf}}
  \\put(-0.03, 2.65 ){\\mylabel{(b)}}
  \\put(-0.03, 5.3 ){\\mylabel{(a)}}
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

