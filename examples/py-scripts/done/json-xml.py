#!/usr/bin/env python3
"""Example: Read JSON from stdin and output XML.

Usage:
    Linux / macOS / WSL (bash, zsh):
        python3 json-xml.py < input.json > output.xml

    Windows PowerShell:
        Get-Content .\input.json -Raw | python .\json-xml.py | Out-File .\output.xml -Encoding utf8

    Windows Command Prompt (cmd.exe):
        type input.json | python json-xml.py > output.xml

Notes:
    - The script reads JSON from standard input.
    - It prints the SVG found at result["value"]["xml"].
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
    xml = data["value"]["xml"]
except KeyError:
    raise SystemExit("Input JSON does not contain value.xml")

print(xml)
