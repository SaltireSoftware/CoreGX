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

area_tex = result["value"]["tex"][0]["valueTex"]
area = parse_latex(area_tex)

print("Area:")
print(area)

c = list(area.free_symbols)[0]

# Find critical points
derivative = sp.diff(area, c)

print("Derivative:")
print(derivative)

critical_points = sp.solve(derivative, c)

print("Critical points:")
print(critical_points)

# Evaluate area at each critical point
for point in critical_points:
    area_at_point = sp.simplify(area.subs(c, point))

print(f"\nAt c = {point}, Area = {area_at_point}")



