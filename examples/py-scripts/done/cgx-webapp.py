#!/usr/bin/env python3
#!/usr/bin/env python3
"""Working example: CoreGX source to web aop.

Usage:

    Linux / macOS / WSL (bash, zsh):
        COREGX_API_KEY=your-key python3 cgx-webapp.py < program.coregx > output.html

    Windows PowerShell:
        $env:COREGX_API_KEY="your-key"
        Get-Content .\program.coregx -Raw | py -3.12 -X utf8 .\cgx-webapp.py | Set-Content -Encoding UTF8 .\output.html

    Windows Command Prompt (cmd.exe):
        set COREGX_API_KEY=your-key
        type program.coregx | py -3.12 -X utf8 cgx-webapp.py > output.html

    Windows Git Bash:
        export COREGX_API_KEY=your-key
        ./cgx-webapp.py < program.coregx > output.html

Notes:
    - The script reads CoreGX source code from standard input.
    - The generated app is written to standard output.
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
