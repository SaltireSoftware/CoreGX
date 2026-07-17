"""Example: CoreGX source to SVG.

Usage:
    Linux / macOS / WSL (bash, zsh):
        COREGX_API_KEY=your-key python3 cgx-svg.py < program.coregx > output.svg

    Windows PowerShell:
        $env:COREGX_API_KEY="your-key"
        Get-Content .\program.coregx -Raw | python .\cgx-svg.py | Out-File .\output.svg -Encoding utf8

    Windows Command Prompt (cmd.exe):
        set COREGX_API_KEY=your-key
        type program.coregx | python cgx-svg.py > output.svg

    Windows Git Bash:
        export COREGX_API_KEY=your-key
        ./cgx-svg.py < program.coregx > output.svg

Notes:
    - The script reads CoreGX source from standard input.
    - The generated SVG is written to standard output.
    - Set COREGX_API_KEY in your environment before running.
"""

import json
import os
import sys
import urllib.request

program = sys.stdin.read()

request = urllib.request.Request(
    "https://api.coregx.dev/run-coregx",
    method="POST",
    headers={"Content-Type": "application/json", "User-Agent": "some-other-user-agent"},
    data=json.dumps(
        {
            "apikey": os.environ["COREGX_API_KEY"],
            "seed": 5,
            "program": program,
            "svg": True,
        }
    ).encode(),
)

with urllib.request.urlopen(request) as response:
    result = json.load(response)

if not result["ok"]:
    raise SystemExit(f"CoreGX error: {result['error']}")

print(result["value"]["svg"])
