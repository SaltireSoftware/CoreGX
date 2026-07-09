#!/usr/bin/env python3
"""Working example: CoreGX source to SymPy to TEX.

Usage:
    COREGX_API_KEY=your-key python minimal.py < program.coregx > output.svg

    Powershell:
    Get-Content -Raw .\example.coregx | py -3.12 -X utf8 .\solve.py | Set-Content -Encoding UTF8 output.json
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

measurement_tex = result["value"]["tex"][0]["valueTex"]

measurement = parse_latex(measurement_tex)

print("Measurement:")
print(measurement)

c = sp.symbols("c")
given_answer = c + 2

equation = sp.Eq(measurement, given_answer)

solution = sp.solve(equation, c)

# Keep positive solutions
positive_solution = [
    s for s in solution
    if s.is_real and s.evalf() > 0
]

if positive_solution:
    c_value = positive_solution[0]

    final_measurement = measurement.subs(c, c_value)

    print("c value:")
    print(c_value)

    print("Final measurement:")
    print(final_measurement)
else:
    print("No positive solution found")
