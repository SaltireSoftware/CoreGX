#!/usr/bin/env python3
"""Example: Read JSON from stdin and output DXF.

Usage:
    Linux / macOS / WSL (bash, zsh):
        python3 json-dxf.py < input.json > output.dxf

    Windows PowerShell:
        Get-Content .\input.json -Raw | python .\json-dxf.py | Out-File .\output.dxf -Encoding utf8

    Windows Command Prompt (cmd.exe):
        type input.json | python json-dxf.py > output.dxf

Notes:
    - The script reads JSON from standard input.
    - It prints the DXF found at result["value"]["dxf"].
"""

import json
import sys

raw = sys.stdin.read()

# Parse JSON
try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    raise SystemExit(f"Invalid JSON input: {e}")

try:
    dxf = data["value"]["dxf"]
except KeyError:
    raise SystemExit("Input JSON does not contain value.dxf")

print(dxf)
