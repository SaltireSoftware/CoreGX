#!/usr/bin/env python3
"""Working example: CoreGX source to SymPy to TEX.

Usage:
    COREGX_API_KEY=your-key python minimal.py < program.coregx > output.svg

    Powershell:
    Get-Content .\example.coregx | python .\solve.py | Set-Content output.tex
"""

import json
import os
import sys
import urllib.request
from sympy.parsing.latex import parse_latex
import sympy as sp

program = sys.stdin.read()

request = urllib.request.Request(
    "https://api.coregx.dev/dev/api/run-coregx",
    method="POST",
    headers={"Content-Type": "application/json", "User-Agent": "some-other-user-agent"},
    data=json.dumps(
        {
            "apikey": os.environ["COREGX_API_KEY"],
            "program": program,
            "all": True,
        }
    ).encode(),
)

with urllib.request.urlopen(request) as response:
    result = json.load(response)

if not result["ok"]:
    raise SystemExit(f"CoreGX error: {result['error']}")

tex = result["value"]["code"][0]["tex"]

print("LaTeX:", tex)

# Convert LaTeX -> SymPy expression
expr = parse_latex(tex)

print("SymPy expression:")
print(expr)

# Simplify
simplified = sp.simplify(expr)

print("Simplified:")
print(simplified)

# Solve if you have an equation
c = sp.symbols("c")
solution = sp.solve(expr, c)

print("Solutions:")
print(solution)
