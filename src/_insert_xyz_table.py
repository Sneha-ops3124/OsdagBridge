from pathlib import Path
import shutil

p = Path("osdagbridge/core/reports/chap4.py")
s = p.read_text(encoding="utf-8")

old = '""" + support_body + r"""\n\\end{longtable}\n\n\\vspace{1em}\n\\begin{longtable}{|L{7cm}|p{8.5cm}|}'

new = r'''""" + support_body + r"""
\end{longtable}

\vspace{1em}
\begin{longtable}{|>{\centering\arraybackslash}p{3.0cm}|>{\centering\arraybackslash}p{2.5cm}|>{\centering\arraybackslash}p{2.5cm}|>{\centering\arraybackslash}p{2.5cm}|>{\centering\arraybackslash}p{2.5cm}|}
\caption{\textbf{Global XYZ Reactions at Supports}}\\
\hline
\textbf{Load Case} & \textbf{Support} & \textbf{Rx (kN)} & \textbf{Ry (kN)} & \textbf{Rz (kN)} \\[6pt]
\hline
\endfirsthead
\hline
\textbf{Load Case} & \textbf{Support} & \textbf{Rx (kN)} & \textbf{Ry (kN)} & \textbf{Rz (kN)} \\[6pt]
\hline
\endhead
""" + horizontal_body + r"""
\end{longtable}

\vspace{1em}
\begin{longtable}{|L{7cm}|p{8.5cm}|}'''

if s.count(old) != 1:
    print("INSERT POINT CHECK FAILED; no change")
else:
    shutil.copy2(p, str(p) + ".before_xyz_table")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")
    print("XYZ table inserted; backup created")