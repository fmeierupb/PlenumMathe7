# Blatt Zweisatz und Dreisatz. Maße, Linien und Pfeile wie im Zweisatz-Blatt (aus dessen PDF ausgelesen):
# Tabelle 2 x 22 mm, Kopf und Zeilen 13 mm, Linien 1,1 pt, Zeilentrennung 0,7 pt, Kopf grau E6E6E6.
# Rechenpfeil: Bogen ab 1,5 mm neben der Tabelle, 90° bis 270°, x-Radius 5,5 mm, Spitze Stealth 2,6 x 2,4 mm gebogen.
# Feld für das Rechenzeichen 10 x 8 mm, Ecken 1,2 mm, grau C8C8C8, 7,6 mm neben der Tabelle.
import sys

HH, RH, CW = 13, 13, 22          # mm
LAB_B, TAB_A, TAB_B = 94.1, 24.25, 118.35   # x von b), Tabelle a), Tabelle b) ab Textrand

def ztab(x0, heads, rows, arrows):
    """rows: [(links, rechts)], arrows: [(von, nach, seite, text oder None)]"""
    n = len(rows); W = 2 * CW; B = -HH - n * RH
    s = [rf"\fill[kopf] ({x0},0) rectangle ({x0+W},{-HH});",
         rf"\draw ({x0},0) rectangle ({x0+W},{B});",
         rf"\draw ({x0+CW},0) -- ({x0+CW},{B});",
         rf"\draw ({x0},{-HH}) -- ({x0+W},{-HH});"]
    for i in range(1, n):
        s.append(rf"\draw[line width=0.7pt] ({x0},{-HH-i*RH}) -- ({x0+W},{-HH-i*RH});")
    if heads:
        for j, t in enumerate(heads):
            s.append(rf"\node[text width={CW-2}mm,align=center,font=\bfseries\klein] at ({x0+(j+.5)*CW},{-HH/2}) {{{t}}};")
    for i, (l, r) in enumerate(rows):
        y = -HH - (i + .5) * RH
        if l: s.append(rf"\node at ({x0+CW/2},{y}) {{{l}}};")
        if r: s.append(rf"\node at ({x0+1.5*CW},{y}) {{{r}}};")
    c = lambda i: -HH - (i + .5) * RH
    for a, b, side, lab in arrows:
        # wie im Zweisatz-Blatt: Start 0,5 mm über der Zeilenmitte, Ende 0,5 mm darunter.
        # Bei zwei Bögen hintereinander bleibt an der mittleren Zeile 2 mm Luft.
        ya = c(a) + (0.5 if a == 0 else -1.0)
        yb = c(b) - (0.5 if b == len(rows) - 1 else -1.0)
        yr = (ya - yb) / 2; ym = (ya + yb) / 2
        if side < 0:
            s.append(rf"\draw[-{{Stealth[length=2.6mm,width=2.4mm,bend]}}] ({x0-1.5},{ya:.2f}) arc[start angle=90,end angle=270,x radius=5.5,y radius={yr:.2f}];")
        else:
            s.append(rf"\draw[-{{Stealth[length=2.6mm,width=2.4mm,bend]}}] ({x0+W+1.5},{ya:.2f}) arc[start angle=90,end angle=-90,x radius=5.5,y radius={yr:.2f}];")
        if lab:
            anc = "east" if side < 0 else "west"
            xx = x0 - 7.5 if side < 0 else x0 + W + 7.5
            s.append(rf"\node[anchor={anc}] at ({xx},{ym:.2f}) {{{lab}}};")
        else:
            xa = x0 - 17.6 if side < 0 else x0 + W + 7.6
            s.append(rf"\fill[feld,rounded corners=1.2mm] ({xa},{ym-4:.2f}) rectangle ({xa+10},{ym+4:.2f});")
    return s, -B

def paar(a, b, labels=True):
    sa, h = ztab(TAB_A, *a); sb, _ = ztab(TAB_B, *b)
    s = [r"\noindent\begin{tikzpicture}[line width=1.1pt,draw=ink,x=1mm,y=1mm]",
         rf"\useasboundingbox (0,0) rectangle ({184.6},{-h});"]
    if labels:
        s += [r"\node[anchor=north west,inner sep=0,font=\bfseries] at (0,-4.4) {a)};",
              rf"\node[anchor=north west,inner sep=0,font=\bfseries] at ({LAB_B},-4.4) {{b)}};"]
    s += sa + sb + [r"\end{tikzpicture}\par"]
    return "\n".join(s)

def zuo(t1="", t2=""):
    return "\n".join([r"\noindent\begin{tikzpicture}[x=1mm,y=1mm,baseline=0pt]",
        r"\useasboundingbox (0,-1.5) rectangle (184.6,4);",
        r"\node[anchor=base west,inner sep=0] at (0,0) {Zuordnung:};",
        r"\draw[line width=0.8pt,draw=ink] (27.7,-0.9) -- (97.7,-0.9);",
        r"\draw[line width=0.8pt,draw=ink] (114.6,-0.9) -- (184.6,-0.9);",
        rf"\node[anchor=base,inner sep=0,font=\fontsize{{14}}{{17}}\selectfont] at (62.7,0) {{{t1}}};",
        rf"\node[anchor=base,inner sep=0,font=\fontsize{{14}}{{17}}\selectfont] at (149.6,0) {{{t2}}};",
        r"\node[anchor=base west,inner sep=0] at (103.1,0) {\fontsize{17.2}{17}\selectfont$\rightarrow$};",
        r"\end{tikzpicture}\par"])

def ab(a, b):
    return (r"\noindent\begin{minipage}[t]{89mm}\textbf{a)} " + a + r"\end{minipage}\hfill"
            r"\begin{minipage}[t]{90.5mm}\textbf{b)} " + b + r"\end{minipage}\par")

PRE = r"""% !TeX program = xelatex
\documentclass{article}
\usepackage[a4paper,top=11mm,bottom=10mm,left=12.7mm,right=12.7mm]{geometry}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,bending,shapes.geometric}
\usepackage{ragged2e}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\hyphenpenalty=10000
\exhyphenpenalty=10000
\emergencystretch=3em
\setmainfont{SourceSans3}[Path=fonts/, Extension=.otf, UprightFont=*-Regular, BoldFont=*-Bold]
\renewcommand\normalsize{\fontsize{13}{19}\selectfont}
\newcommand\klein{\fontsize{11}{14}\selectfont}
\definecolor{ink}{HTML}{1F1D1A}
\definecolor{kopf}{HTML}{E6E6E6}
\definecolor{feld}{HTML}{C8C8C8}
\definecolor{gitter}{HTML}{B4B4B4}
\newcommand\titel[1]{{\bfseries\fontsize{28}{30}\selectfont #1\par}\vspace{2.5mm}\hrule height 1.2pt\vspace{4mm}}
\newcommand\aufgabe[2]{\par\noindent\begin{tikzpicture}[baseline=(n.base)]
  \node[circle,fill=ink,text=white,minimum size=7mm,inner sep=0,font=\bfseries\fontsize{12}{12}\selectfont] (n) {#1};
  \end{tikzpicture}\hspace{2.5mm}\textbf{#2}\par\vspace{2.5mm}}
\newcommand\stern{\tikz[baseline=-0.6ex]{\node[circle,fill=ink,inner sep=0pt,minimum size=7mm]{};\node[star,star points=5,star point ratio=2.3,fill=white,inner sep=0pt,minimum size=4.4mm]{};}}
\newcommand\linie[1]{\tikz[baseline=0pt]\draw[line width=0.8pt,draw=ink] (0,-0.9mm) -- (#1,-0.9mm);}
\AtBeginDocument{\normalsize\RaggedRight\color{ink}}
\begin{document}
"""

A2 = [(0, 1, -1, None), (0, 1, 1, None)]
A3 = [(0, 1, -1, None), (1, 2, -1, None), (0, 1, 1, None), (1, 2, 1, None)]
G = r"\vspace{5mm}"
b = [r"\titel{Zweisatz und Dreisatz}"]

b.append(r"\aufgabe{1}{Ergänze beide Rechenpfeile und den fehlenden Wert.}")
b.append(r"Im Schreibwarenladen kosten 4 Ordner 6~€. Tom kauft 8 Ordner, Lea 2 Ordner.\par\vspace{4mm}")
b.append(zuo("Anzahl der Ordner", "Preis in €") + r"\vspace{3mm}")
H = (r"Anzahl der Ordner", r"Preis in €")
b.append(paar((H, [("4", "6"), ("8", "")], A2), (H, [("4", "6"), ("2", "")], A2)))
b.append(G)

b.append(r"\aufgabe{2}{Schreibe die Zuordnung auf. Rechne zuerst auf 1, dann zum gesuchten Wert.}")
b.append(ab(r"Im Schreibwarenladen kosten 8 Hefte 20~€.\\Wie viel kosten 3 Hefte?", r"Im Supermarkt kosten 6 Hefte 13,20~€.\\Wie viel kosten 14 Hefte?") + r"\vspace{4mm}")
b.append(zuo() + r"\vspace{3mm}")
H = (r"Anzahl der Hefte", r"Preis in €")
b.append(paar((H, [("8", "20"), ("1", ""), ("3", "")], A3), (H, [("6", "13,20"), ("1", ""), ("14", "")], A3)))
b.append(G)

b.append(r"\aufgabe{3}{Schreibe die Zuordnung auf. Trage die 1 selbst ein und rechne.}")
b.append(ab(r"Ein Auto fährt mit 6 Litern Benzin 84~km.\\Wie weit kommt es mit 4 Litern?", r"Ein Roller fährt mit 3 Litern Benzin 105~km.\\Wie weit kommt er mit 8 Litern?") + r"\vspace{4mm}")
b.append(zuo() + r"\vspace{3mm}")
H = (r"Benzin in Liter", r"Strecke in km")
b.append(paar((H, [("6", "84"), ("", ""), ("4", "")], A3), (H, [("3", "105"), ("", ""), ("8", "")], A3)))

b.append(r"\newpage")
b.append(r"\aufgabe{4}{Schreibe die Zuordnung auf. Beschrifte die Tabelle, trage die Werte ein und rechne.}")
b.append(r"Auf dem Wochenmarkt kaufen Frau Kaya und Herr Becker ein.\par\vspace{2mm}")
b.append(ab(r"3~kg Äpfel kosten 7,50~€.\\Wie viel kosten 5~kg Äpfel?", r"6 Gläser Honig kosten 27~€.\\Wie viel kosten 4 Gläser Honig?") + r"\vspace{4mm}")
b.append(zuo() + r"\vspace{3mm}")
E3 = [("", ""), ("", ""), ("", "")]
b.append(paar((None, E3, A3), (None, E3, A3), labels=False))
b.append(r"\vspace{5mm}")
b.append(r"\noindent\begin{minipage}[t]{89mm}Antwort: \linie{68mm}\\[6mm]\linie{87mm}\end{minipage}\hfill\begin{minipage}[t]{90.5mm}Antwort: \linie{69.5mm}\\[6mm]\linie{89mm}\end{minipage}\par" + G)

b.append(r"\aufgabe{5}{Arbeite \underline{im Heft}: Zuordnung, Tabelle, Rechnung und Antwortsatz.}")
b.append(r"""\begin{tabular}{@{}l@{\hspace{2mm}}p{176mm}@{}}
\textbf{a)} & Ein Drucker druckt in 4 Minuten 96 Seiten. Wie viele Seiten druckt er in 15 Minuten?\\
\textbf{b)} & 7 Eintrittskarten für den Zoo kosten 59,50~€. Wie viel kosten 3 Karten?\\
\textbf{c)} & Für 4 Portionen Pfannkuchen braucht man 300~g Mehl. Wie viel Mehl brauchen 10 Portionen?
\end{tabular}\par""" + G)

b.append(r"\par\noindent\stern\hspace{2.5mm}\textbf{Für Schnelle: Arbeite \underline{im Heft}.}\par\vspace{2.5mm}")
b.append(r"""\begin{tabular}{@{}l@{\hspace{2mm}}p{176mm}@{}}
\textbf{a)} & 12 Flaschen Wasser kosten 5,40~€. Was kosten 7 Flaschen?\\
\textbf{b)} & 6 Kugeln Eis kosten 9~€. Wie viele Kugeln bekommst du für 12~€?\\
\textbf{c)} & Lina soll den Preis für 4 Müsliriegel berechnen. 6 Müsliriegel kosten 18~€. Sie rechnet: \mbox{„18~€ : 6 = 3~€.} \mbox{Dann 3~€ + 4 = 7~€.“} Was hat Lina falsch gemacht? Rechne richtig.\\
\textbf{d)} & Eine Taxifahrt kostet 4~€ Grundgebühr und 2~€ pro Kilometer. Für 5~km zahlt man 14~€. Ben rechnet mit dem Dreisatz den Preis für 10~km aus und erhält 28~€. Stimmt das? Begründe.\\
\textbf{e)} & Denke dir selbst eine Dreisatz-Aufgabe aus. Tausche sie mit deinem Nachbarn. Löst eure Aufgaben gegenseitig.
\end{tabular}\par\vspace{5mm}""")
GR = sys.argv[1] if len(sys.argv) > 1 else "40"
b.append(rf"""\noindent\begin{{tikzpicture}}[x=1mm,y=1mm]
\draw[gitter,line width=0.4pt,step=5] (0,0) grid (180,-{GR});
\draw[gitter,line width=0.4pt] (0,0) rectangle (180,-{GR});
\end{{tikzpicture}}""")

open('ab-dreisatz.tex', 'w').write(PRE + "\n".join(b) + "\n\\end{document}\n")
