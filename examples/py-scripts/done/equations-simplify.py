#!/usr/bin/env python3
"""Working example: Equations JSON to simplified expression.

Usage:

    Linux / macOS / WSL (bash, zsh):
        python3 simplify.py < equations.json > output.tex

    Windows PowerShell:
        Get-Content .\equations.json -Raw | py -3.12 -X utf8 .\simplify.py | Set-Content -Encoding UTF8 .\output.tex

    Windows Command Prompt (cmd.exe):
        type equations.json | py -3.12 -X utf8 simplify.py > output.tex

    Windows Git Bash:
        ./simplify.py < equations.json > output.tex

Notes:
    - Reads an equations JSON document from standard input.
    - Uses the first equation's "valueTex" field.
    - Outputs the simplified expression as TeX.
"""

import json
import sys

import sympy as sp
from sympy.parsing.latex import parse_latex

data = json.load(sys.stdin)

expr = parse_latex(data["equations"][0]["valueTex"])

print(sp.latex(sp.simplify(expr)))