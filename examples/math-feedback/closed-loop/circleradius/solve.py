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
import re

import sympy as sp
from sympy.parsing.latex import parse_latex

program = sys.stdin.read()

request = urllib.request.Request(
    "https://api.coregx.dev/dev/api/run-coregx",
    method="POST",
    headers={
        "Content-Type": "application/json",
        "User-Agent": "example",
    },
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

area = parse_latex(result["value"]["equations"][0]["valueTex"])

r = next(iter(area.free_symbols))

best = sp.solve(
    area - 81*sp.pi,
    r
)[0]

program = re.sub(r"\br\b", sp.sstr(best), program)

request = urllib.request.Request(
    "https://api.coregx.dev/dev/api/run-coregx",
    method="POST",
    headers={
        "Content-Type": "application/json",
        "User-Agent": "example",
    },
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

print(result["value"]["app"])



