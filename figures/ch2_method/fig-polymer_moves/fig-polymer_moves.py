#!/usr/bin/env python3

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=7.0in,paperheight=4.305in]{geometry}
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
\\begin{picture}(7.0,4.305)
  \\put(0.000, 1.110){\\mylabel{c)}}
  \\put(0.000, 2.580){\\mylabel{b)}}
  \\put(0.000, 4.090){\\mylabel{a)}}
  \\put(3.330, 4.080){\\mylabel{d)}}
  \\put(0.010, 0.020){\\frame{\\includegraphics[scale=1.035]{reptation_move.pdf}}}
  \\put(0.010, 1.505){\\frame{\\includegraphics[scale=1.035]{end_rotation_move.pdf}}}
  \\put(0.010, 2.990){\\frame{\\includegraphics[scale=1.035]{crank_shaft_move.pdf}}}
  \\put(3.311, 0.010){\\frame{\\includegraphics[scale=0.994]{config_bias_move.pdf}}}
\\end{picture}
\\end{document}
"""
)
f1.close();

subprocess.run(['pdflatex', basename+'.tex'])
subprocess.run(['rm', basename+'.tex', basename+'.aux', basename+'.log'])
