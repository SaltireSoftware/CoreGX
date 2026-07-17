#!/usr/bin/env python3
"""Example: Read JSON from stdin and output SVG.

Usage:
    Linux / macOS / WSL (bash, zsh):
        python3 json-svg.py < input.json > output.svg

    Windows PowerShell:
        Get-Content .\input.json -Raw | python .\json-svg.py | Out-File .\output.svg -Encoding utf8

    Windows Command Prompt (cmd.exe):
        type input.json | python json-svg.py > output.svg

Notes:
    - The script reads JSON from standard input.
    - It prints the SVG found at result["value"]["svg"].
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
    svg = data["value"]["svg"]
except KeyError:
    raise SystemExit("Input JSON does not contain value.svg")

print(svg)
