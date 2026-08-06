#!/usr/bin/env python3
r"""Working example: Equations JSON to a symbolic limit.

Usage:

    Linux / macOS / WSL (bash, zsh):
        python3 limit.py < equations.json > output.tex

    Windows PowerShell:
        Get-Content .\equations.json -Raw | py -3.12 -X utf8 .\limit.py | Set-Content -Encoding UTF8 .\output.tex

    Windows Command Prompt (cmd.exe):
        type equations.json | py -3.12 -X utf8 limit.py > output.tex

    Windows Git Bash:
        ./limit.py < equations.json > output.tex

Notes:
    - Reads an equations JSON document from standard input.
    - Uses the first equation's "valueTex" field.
    - Computes the limit of (f(x)-1)/x² as x→0.
    - Outputs the answer as a sentence in TeX format.
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

limit_expression = (expr - 1) / x**2
value = sp.limit(limit_expression, x, 0)

print(
    rf"\text{{The limit as }} {sp.latex(x)} \to 0 "
    rf"\text{{ of }} {sp.latex(limit_expression)} "
    rf"\text{{ is }} {sp.latex(value)}\text{{.}}"
)
