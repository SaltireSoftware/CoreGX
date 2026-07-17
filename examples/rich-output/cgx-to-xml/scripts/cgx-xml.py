#!/usr/bin/env python3
"""Example: CoreGX source to XML.

Usage:
    Linux / macOS / WSL (bash, zsh):
        COREGX_API_KEY=your-key python3 cgx-xml.py < program.coregx > output.xml

    Windows PowerShell:
        $env:COREGX_API_KEY="your-key"
        Get-Content .\program.coregx -Raw | python .\cgx-xml.py | Out-File .\output.xml -Encoding utf8

    Windows Command Prompt (cmd.exe):
        set COREGX_API_KEY=your-key
        type program.coregx | python cgx-xml.py > output.xml

    Windows Git Bash:
        export COREGX_API_KEY=your-key
        ./cgx-xml.py < program.coregx > output.xml

Notes:
    - The script reads CoreGX source from standard input.
    - The generated XML is written to standard output.
    - Set COREGX_API_KEY in your environment before running.
"""

import json
import os
import sys
import urllib.request

program = sys.stdin.read()

request = urllib.request.Request(
    "https://api.coregx.dev/dev/api/run-coregx",
    method="POST",
    headers={"Content-Type": "application/json", "User-Agent": "some-other-user-agent"},
    data=json.dumps(
        {
            "apikey": os.environ["COREGX_API_KEY"],
            "program": program,
            "xml": True,
        }
    ).encode(),
)

with urllib.request.urlopen(request) as response:
    result = json.load(response)

if not result["ok"]:
    raise SystemExit(f"CoreGX error: {result['error']}")

print(result["value"]["xml"])