#!/usr/bin/env python3
"""Working example: Equations JSON to symbolic solutions.

Usage:

    Linux / macOS / WSL / Git Bash:
        python3 equations-solve.py < equations.json > solutions.json

    Windows PowerShell:
        Get-Content .\equations.json -Raw | py -3.12 -X utf8 .\equations-solve.py | Set-Content -Encoding UTF8 .\solutions.json

    Windows Command Prompt:
        type equations.json | py -3.12 -X utf8 equations-solve.py > solutions.json

Notes:
    - Reads an equations JSON document from standard input.
    - Uses the first equation's "valueTex" field.
    - Solves the expression equal to zero.
    - Outputs symbolic solutions as JSON.
"""

import json
import sys

import sympy as sp
from sympy.parsing.latex import parse_latex


data = json.load(sys.stdin)

expr = parse_latex(data[0]["valueTex"])

symbols = list(expr.free_symbols)

if len(symbols) != 1:
    raise SystemExit(
        "Expression must contain exactly one free symbol."
    )

variable = symbols[0]

solutions = sp.solve(expr, variable)

print(
    json.dumps(
        {
            "expression": sp.latex(expr),
            "variable": str(variable),
            "solutions": [
                sp.latex(solution)
                for solution in solutions
            ],
        },
        indent=2,
    )
)