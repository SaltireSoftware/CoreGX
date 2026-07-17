#!/usr/bin/env python3
"""Working example: Equations JSON to critical points.

Usage:

    Linux / macOS / WSL (bash, zsh):
        python3 critical_points.py < equations.json > output.json

    Windows PowerShell:
        Get-Content .\equations.json -Raw | py -3.12 -X utf8 .\critical_points.py | Set-Content -Encoding UTF8 .\output.json

    Windows Command Prompt (cmd.exe):
        type equations.json | py -3.12 -X utf8 critical_points.py > output.json

    Windows Git Bash:
        ./critical_points.py < equations.json > output.json

Notes:
    - Reads an equations JSON document from standard input.
    - Uses the first equation's "valueTex" field.
    - Outputs the critical points and corresponding function values as JSON.
"""

import json
import sys

import sympy as sp
from sympy.parsing.latex import parse_latex

data = json.load(sys.stdin)

expr = parse_latex(data["equations"][0]["valueTex"])

symbols = list(expr.free_symbols)
if len(symbols) != 1:
    raise SystemExit("Expression must contain exactly one free symbol.")

x = symbols[0]

critical_points = sp.solve(sp.diff(expr, x), x)

result = []

for point in critical_points:
    result.append(
        {
            "point": sp.latex(point),
            "value": sp.latex(sp.simplify(expr.subs(x, point))),
        }
    )

print(json.dumps(result, indent=2))