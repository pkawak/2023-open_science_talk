#!/usr/bin/env python3

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=7.000in,paperheight=3.850in]{geometry}
\\usepackage{graphicx}
\\usepackage[dvipsnames]{xcolor}
\\usepackage{tikz}
\\newcommand{\mylabel}[1]{%
  \\begin{tikzpicture}
    \\node[rounded corners=2pt, align=center, inner sep=1.5pt]{\\large{#1}};
  \\end{tikzpicture}%
  }
\\newcommand{\mymeltlabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill={rgb:red,151;green,32;blue,53}, rounded corners=2pt, align=center, inner sep=1.5pt]{{\\textcolor{white}{\\large{#1}}}};
  \\end{tikzpicture}%
  }
\\newcommand{\mynematiclabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill={rgb:red,255;green,98;blue,17}, rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{white}{\\large{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\mycrystlabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill={rgb:red,159;green,174;blue,105}, rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{white}{\\large{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\myxlabel}[1]{%
  \\begin{tikzpicture}
    \\node[rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{red}{\\normalsize{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\myylabel}[1]{%
  \\begin{tikzpicture}
    \\node[rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{green}{\\normalsize{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\myzlabel}[1]{%
  \\begin{tikzpicture}
    \\node[rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{blue}{\\normalsize{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\yourxlabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill=white, rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{red}{\\normalsize{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\yourylabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill=white, rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{green}{\\normalsize{#1}}};
  \\end{tikzpicture}%
  }
\\newcommand{\yourzlabel}[1]{%
  \\begin{tikzpicture}
    \\node[fill=white, rounded corners=2pt, align=center, inner sep=1.5pt]{\\textcolor{blue}{\\normalsize{#1}}};
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
\\begin{picture}(7.000,3.850)
  \\put(0.000, 2.600){\\includegraphics[]{subfig-AA_PE.pdf}}
  \\put(2.320, 2.600){\\includegraphics[]{subfig-UA_PE.pdf}}
  \\put(4.767, 2.600){\\includegraphics[]{subfig-CG_PE.pdf}}
  \\put(-0.1, -0.07){\\includegraphics[scale=1.1]{subfig-long_CG_PE.pdf}}
  \\put(2.730, 0.000){\\includegraphics[]{fig-bonded_CG.pdf}}
  \\put(4.228, 0.000){\\includegraphics[]{fig-nonbonded_CG.pdf}}
  \\put(0.000, 3.650 ){\\mylabel{a)}}
  \\put(2.100, 3.650 ){\\mylabel{b)}}
  \\put(4.580, 3.650 ){\\mylabel{c)}}
  \\put(0.000, 2.450 ){\\mylabel{d)}}
  \\put(2.670, 2.450 ){\\mylabel{e)}}
  \\put(4.380, 2.450 ){\\mylabel{f)}}
\\end{picture}
\\end{document}
"""
)
f1.close();

subprocess.run(['pdflatex', basename+'.tex'])
subprocess.run(['rm', basename+'.tex', basename+'.aux', basename+'.log'])
