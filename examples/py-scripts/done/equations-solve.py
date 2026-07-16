#!/usr/bin/env python3
"""Working example: Equations JSON to symbolic solutions.

Usage:

    Linux / macOS / WSL (bash, zsh):
        python3 solve.py < equations.json > output.json

    Windows PowerShell:
        Get-Content .\equations.json -Raw | py -3.12 -X utf8 .\solve.py | Set-Content -Encoding UTF8 .\output.json

    Windows Command Prompt (cmd.exe):
        type equations.json | py -3.12 -X utf8 solve.py > output.json

    Windows Git Bash:
        ./solve.py < equations.json > output.json

Notes:
    - Reads an equations JSON document from standard input.
    - Uses the first equation's "valueTex" field.
    - Solves the equation expression = 0.
    - Outputs the symbolic solutions as JSON.
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

solutions = sp.solve(expr, x)

print(
    json.dumps(
        {
            "variable": str(x),
            "solutions": [sp.latex(s) for s in solutions],
        },
        indent=2,
    )
)