#!/usr/bin/env python3

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=5.0in,paperheight=1.650in]{geometry}
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
    \\node[fill={rgb:red,1;green,1;blue,1},opacity=0.8]{\\large{#1}};
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
\\begin{picture}(5.0,1.650)
  \\put(-0.02, 1.49){\\mylabel{a}}
  \\put(1.950, 1.49){\\mylabel{b}}
  \\put(3.500, 1.49){\\mylabel{c}}
  \\put(0.000, 0.00){\\includegraphics[scale=4]{melt_chains.pdf}}
  \\put(2.000, 0.00){\\includegraphics[scale=3]{trans_chains.pdf}}
  \\put(3.550, 0.00){\\includegraphics[scale=4]{crystal_chains.pdf}}
\\end{picture}
\\end{document}
"""
)
f1.close();

subprocess.run(['pdflatex', basename+'.tex'])
subprocess.run(['rm', basename+'.tex', basename+'.aux', basename+'.log'])
