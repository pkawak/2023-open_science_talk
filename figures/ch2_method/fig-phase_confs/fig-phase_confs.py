#!/usr/bin/env python3

import os
import subprocess

basename = os.path.splitext(__file__)[0]

f1 = open(basename+'.tex', 'w')
f1.writelines("""\
\\documentclass[10pt]{article}

%Preamble
\\usepackage[margin=0in,paperwidth=6.5in,paperheight=5.41in]{geometry}
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
\\begin{picture}(6.5,5.41)
  \\put(4.34, 3.440 ){\\includegraphics[trim={144 220 150 214}, clip, scale=0.22]{configs_lowT/cryst-vdw-x.png}}
  \\put(2.17, 3.440 ){\\includegraphics[trim={150 220 150 220}, clip, scale=0.22]{configs_lowT/nematic-vdw-x.png}}
  \\put(0.00, 3.440 ){\\includegraphics[trim={150 220 145 220}, clip, scale=0.22]{configs_lowT/melt-vdw-x.png}}
  \\put(4.34, 1.720 ){\\includegraphics[trim={155 235 160 223}, clip, scale=0.22]{configs_lowT/cryst-licorice-x.png}}
  \\put(2.17, 1.720 ){\\includegraphics[trim={160 230 160 232}, clip, scale=0.22]{configs_lowT/nematic-licorice-x.png}}
  \\put(0.00, 1.720 ){\\includegraphics[trim={160 230 156 230}, clip, scale=0.22]{configs_lowT/melt-licorice-x.png}}
  \\put(4.34, 0.000 ){\\includegraphics[trim={160 235 156 220}, clip, scale=0.22]{configs_lowT/cryst-licorice-z.png}}
  \\put(2.17, 0.000 ){\\includegraphics[trim={156 230 165 230}, clip, scale=0.22]{configs_lowT/nematic-licorice-z.png}}
  \\put(0.00, 0.000 ){\\includegraphics[trim={160 230 156 230}, clip, scale=0.22]{configs_lowT/melt-licorice-z.png}}
  \\put(0.7, 5.2 ){\\mymeltlabel{(a) Melt}}
  \\put(0.1, 4.88 ){\\mymeltlabel{i}}
  \\put(0.1, 3.14 ){\\mymeltlabel{ii}}
  \\put(0.1, 1.4 ){\\mymeltlabel{iii}}
  \\put(2.8, 5.2 ){\\mynematiclabel{(b) Nematic}}
  \\put(2.3, 4.88 ){\\mynematiclabel{i}}
  \\put(2.3, 3.14 ){\\mynematiclabel{ii}}
  \\put(2.3, 1.4 ){\\mynematiclabel{iii}}
  \\put(5.0, 5.2 ){\\mycrystlabel{(c) Crystal}}
  \\put(4.55, 4.88 ){\\mycrystlabel{i}}
  \\put(4.55, 3.14 ){\\mycrystlabel{ii}}
  \\put(4.55, 1.4 ){\\mycrystlabel{iii}}
\\end{picture}
\\end{document}
"""
)
f1.close();

subprocess.run(['pdflatex', basename+'.tex'])
subprocess.run(['rm', basename+'.tex', basename+'.aux', basename+'.log'])
