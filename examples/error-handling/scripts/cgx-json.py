#!/usr/bin/env python3
#!/usr/bin/env python3
"""Example: CoreGX source to JSON.

Usage:

    Linux / macOS / WSL (bash, zsh):
        COREGX_API_KEY=your-key python3 cgx-json.py < program.coregx > output.json

    Windows PowerShell:
        $env:COREGX_API_KEY="your-key"
        Get-Content .\program.coregx -Raw | python .\cgx-json.py | Out-File .\output.json -Encoding utf8

    Windows Command Prompt (cmd.exe):
        set COREGX_API_KEY=your-key
        type program.coregx | python cgx-json.py > output.json

    Windows Git Bash:
        export COREGX_API_KEY=your-key
        ./cgx-json.py < program.coregx > output.json

Notes:
    - The script reads CoreGX source from standard input.
    - The generated JSON is written to standard output.
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
            "program": program,
            "all": True,
        }
    ).encode(),
)

with urllib.request.urlopen(request) as response:
    result = json.load(response)

if not result["ok"]:
    raise SystemExit(f"CoreGX error: {result['error']}")

print(json.dumps(result, indent=2))
