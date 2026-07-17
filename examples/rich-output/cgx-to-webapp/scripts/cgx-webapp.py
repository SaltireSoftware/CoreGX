#!/usr/bin/env python3
"""Example: CoreGX source to HTML web app.

Usage:
    Linux / macOS / WSL (bash, zsh):
        python3 cgx-webapp.py < program.coregx > output.html

    Windows PowerShell:
        Get-Content .\program.coregx -Raw | python .\cgx-webapp.py | Out-File .\output.html -Encoding utf8

    Windows Command Prompt (cmd.exe):
        type program.coregx | python cgx-webapp.py > output.html

Notes:
    - The script reads CoreGX source from standard input.
    - The generated HTML web app output is written to standard output.
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

print((result["value"]["app"]))
