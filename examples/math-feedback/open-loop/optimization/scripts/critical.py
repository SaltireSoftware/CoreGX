#!/usr/bin/env python3
r"""Working example: Equations JSON to critical points.

Usage:

    Linux / macOS / WSL (bash, zsh):
        python3 critical.py < equations.json > output.tex

    Windows PowerShell:
        Get-Content .\equations.json -Raw | py -3.12 -X utf8 .\critical.py | Set-Content -Encoding UTF8 .\output.tex

    Windows Command Prompt (cmd.exe):
        type equations.json | py -3.12 -X utf8 critical.py > output.tex

    Windows Git Bash:
        ./critical.py < equations.json > output.tex

Notes:
    - Reads an equations JSON document from standard input.
    - Uses the first equation's "valueTex" field.
    - Outputs the critical points and corresponding function values as a sentence in TeX format.
"""

import json
import sys

import sympy as sp
from sympy.parsing.latex import parse_latex

data = json.load(sys.stdin)

expr = parse_latex(data[0]["valueTex"])

symbols = list(expr.free_symbols)
if len(symbols) != 1:
    raise SystemExit("Expression must contain exactly one free symbol.")

x = symbols[0]

critical_points = sp.solve(sp.diff(expr, x), x)

if not critical_points:
    print(r"\text{The expression has no critical points.}")
elif len(critical_points) == 1:
    point = critical_points[0]
    value = sp.simplify(expr.subs(x, point))
    print(
        rf"\text{{The critical point is }} {sp.latex(x)} = {sp.latex(point)}"
        rf"\text{{, where the function value is }} {sp.latex(value)}\text{{.}}"
    )
else:
    answers = []
    separator = r"; \quad "
    for point in critical_points:
        value = sp.simplify(expr.subs(x, point))
        answers.append(
            rf"{sp.latex(x)} = {sp.latex(point)}"
            rf"\text{{, where the function value is }} {sp.latex(value)}"
        )

    print(
        rf"\text{{The critical points are }} {separator.join(answers)}\text{{.}}"
    )
