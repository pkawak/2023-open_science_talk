#!/usr/bin/env python3

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=2.78in,paperheight=2.222in]{geometry}
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
\\begin{picture}(2.78,2.222)
  \\put(0.00, 0.00){\\includegraphics[]{subfig-pathway_soft_cryst_small.pdf}}
  \\put(0.60, 1.20){\\includegraphics[scale=1.35]{trans_chains.pdf}}
%  \\put(0.30, 0.723){\\includegraphics[]{melt_chains.pdf}}
  \\put(1.60, 1.50){\\includegraphics[scale=1.8]{crystal_chains.pdf}}
%  \\put(2.00, 0.75){\\includegraphics[scale=1.75]{subfig-cooperativity_arrow.pdf}}
\\end{picture}
\\end{document}
"""
)
f1.close();

subprocess.run(['pdflatex', basename+'.tex'])
subprocess.run(['rm', basename+'.tex', basename+'.aux', basename+'.log'])
