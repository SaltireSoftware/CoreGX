#!/usr/bin/env python3
"""Example: Read JSON from stdin and output equations.

Usage:
    Linux / macOS / WSL (bash, zsh):
        python3 json-equations.py < input.json > output.json

    Windows PowerShell:
        Get-Content .\input.json -Raw | python .\json-equations.py | Out-File .\output.json -Encoding utf8

    Windows Command Prompt (cmd.exe):
        type input.json | python json-equations.py > output.json

Notes:
    - The script reads JSON from standard input.
    - It prints the JSON found at result["value"]["equations"].
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
    raise SystemExit("Input JSON does not contain value.equations")

print(equations)
