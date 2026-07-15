#!/usr/bin/env python3
"""Working example: CoreGX source to SymPy to TEX.

Usage:
    COREGX_API_KEY=your-key python minimal.py < program.coregx > output.svg

    Powershell:
    Get-Content -Raw .\example.coregx | py -3.12 -X utf8 .\solve.py | Set-Content -Encoding UTF8 output.xml
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

area_tex = result["value"]["equations"][0]["valueTex"]
area = parse_latex(area_tex)

c = list(area.free_symbols)[0]

# Find critical points
derivative = sp.diff(area, c)

critical_points = sp.solve(derivative, c)

# Evaluate area at each critical point
for point in critical_points:
    area_at_point = sp.simplify(area.subs(c, point))
    program = f"""
    triangle A B C
    perpendicular AB BC
    distance A B {sp.sstr(point)}
    distance B C {sp.sstr(12-point)}
    measure area(A,B,C)
    """



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

print(result["value"]["xml"])



