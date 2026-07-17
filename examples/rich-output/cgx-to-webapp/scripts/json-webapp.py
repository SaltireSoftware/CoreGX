#!/usr/bin/env python3
"""Example: Read JSON from stdin and output HTML web app.

Usage:
    Linux / macOS / WSL (bash, zsh):
        python3 json-webapp.py < input.json > output.html

    Windows PowerShell:
        Get-Content .\input.json -Raw | python .\json-webapp.py | Out-File .\output.html -Encoding utf8

    Windows Command Prompt (cmd.exe):
        type input.json | python json-webapp.py > output.html

Notes:
    - The script reads JSON from standard input.
    - It prints the HTML found at result["value"]["app"].
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
    app = data["value"]["app"]
except KeyError:
    raise SystemExit("Input JSON does not contain value.app")

print(app)
