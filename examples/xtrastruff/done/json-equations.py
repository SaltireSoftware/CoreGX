#!/usr/bin/env python3
"""Example: Read JSON from stdin and output equations in JSON format.

Usage:
    Linux / macOS / WSL (bash, zsh):
        python3 json-equations.py < input.json > output.svg

    Windows PowerShell:
        Get-Content .\input.json -Raw | python .\json-equations.py | Out-File .\output.svg -Encoding utf8

    Windows Command Prompt (cmd.exe):
        type input.json | python json-equations.py > output.svg

Notes:
    - The script reads JSON from standard input.
    - It prints the equations found at result["value"]["equations"].
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
    equations = data["value"]["equations"]
except KeyError:
    raise SystemExit("Input JSON does not contain value.svg")

print(json.dumps(equations, indent=2))
