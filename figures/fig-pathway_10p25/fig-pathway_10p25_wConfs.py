#!/usr/bin/env python3

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=3.75in,paperheight=2.92in]{geometry}
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
\\begin{picture}(3.75,2.92)
  \\put(0.00, 0.00){\\includegraphics[]{subfig-pathway_10p25_mark.pdf}}
  \\put(0.65, 0.80){\\includegraphics[scale=1.85]{melt_chains.pdf}}
%  \\put(0.40, 0.95){\\includegraphics[]{trans_chains.pdf}}
  \\put(1.67, 2.30){\\includegraphics[scale=1.85]{crystal_chains.pdf}}
%  \\put(2.00, 0.75){\\includegraphics[scale=1.75]{subfig-cooperativity_arrow.pdf}}
\\end{picture}
\\end{document}
"""
)
f1.close();

subprocess.run(['pdflatex', basename+'.tex'])
subprocess.run(['rm', basename+'.tex', basename+'.aux', basename+'.log'])
