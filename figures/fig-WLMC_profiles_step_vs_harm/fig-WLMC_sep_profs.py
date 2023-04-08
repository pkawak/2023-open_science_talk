#!/usr/bin/env python3

import os
import subprocess

basename = os.path.splitext(__file__)[0]

for i in [1, 2, 3, 4]:
  f1 = open(basename+'_'+str(i)+'.tex', 'w')
  f1.writelines("""\
  \\documentclass[10pt]{article}
  
  %Preamble
  \\usepackage[margin=0in,paperwidth=5.5in,paperheight=2.92in]{geometry}
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
  \\begin{picture}(5.5,2.92)
    \\put(0.00, 0.00){\\includegraphics[]{sub""" + basename.split('/')[1] + """_"""+str(i)+""".pdf}}
  """
  )

  if i > 1:
    f1.writelines("""\
      \\put(1.30, 2.65){\\includegraphics[scale=0.704]{melt_chains.pdf}}
      \\put(1.42, 2.56){$\\Downarrow$}
      \\put(1.33, 2.3){\\includegraphics[scale=0.792]{crystal_chains.pdf}}
    """
    )

  if i > 3:
    f1.writelines("""\
      \\put(3.70, 1.70){\\includegraphics[scale=0.704]{melt_chains.pdf}}
      \\put(3.82, 1.61){$\\Downarrow$}
      \\put(3.73, 1.34){\\includegraphics[scale=0.55]{trans_chains.pdf}}
      \\put(3.82, 1.30){$\\Downarrow$}
      \\put(3.73, 1.05){\\includegraphics[scale=0.792]{crystal_chains.pdf}}
    """
    )

  f1.writelines("""\
  \\end{picture}
  \\end{document}
  """
  )
  f1.close();
  
  subprocess.run(['pdflatex', basename+'_'+str(i)+'.tex'])
  subprocess.run(['rm', basename+'_'+str(i)+'.tex', basename+'_'+str(i)+'.aux', basename+'_'+str(i)+'.log'])
