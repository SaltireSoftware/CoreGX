#!/usr/bin/env python3
"""Example: CoreGX source to equations JSON.

Usage:

    Linux / macOS / WSL (bash, zsh):
        COREGX_API_KEY=your-key python3 cgx-equations.py < program.coregx > output.json

    Windows PowerShell:
        $env:COREGX_API_KEY="your-key"
        Get-Content .\program.coregx -Raw | py -3.12 -X utf8 .\cgx-equations.py | Set-Content -Encoding UTF8 .\output.tex

    Windows Command Prompt (cmd.exe):
        set COREGX_API_KEY=your-key
        type program.coregx | py -3.12 -X utf8 cgx-equations.py > output.json

    Windows Git Bash:
        export COREGX_API_KEY=your-key
        ./cgx-equations.py < program.coregx > output.json

Notes:
    - The script reads CoreGX source from standard input.
    - The generated JSON equations output is written to standard output.
    - Set COREGX_API_KEY in your environment before running.
"""

import json
import os
import sys
import urllib.request
from sympy.parsing.latex import parse_latex
import sympy as sp

program = sys.stdin.read()

request = urllib.request.Request(
    "https://api.coregx.dev/run-coregx",
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

print(json.dumps(result["value"]["equations"], indent=2))