#!/usr/bin/env python3
"""
Remove CoreGX lines that produced errors.

Usage:

    Linux / macOS / WSL:
        python3 remove-error-lines.py coregx.json < example.coregx > fixed.coregx

    Windows PowerShell:
        Get-Content .\example.coregx | py -3.12 -X utf8 .\remove-error-lines.py .\coregx.json | Set-Content -Encoding UTF8 .\fixed.coregx

Notes:
    - Reads CoreGX error JSON.
    - Finds error line numbers.
    - Removes those lines from the input CoreGX program.
    - Outputs repaired CoreGX source.
"""

import json
import sys


def main():

    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: remove-error-lines.py coregx.json"
        )

    json_file = sys.argv[1]

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = (
        data
        .get("value", {})
        .get("errors", [])
    )

    remove_lines = {
        error["line"]
        for error in errors
        if "line" in error
    }

    program = sys.stdin.read().splitlines()

    fixed = [
        line
        for index, line in enumerate(program, start=1)
        if index not in remove_lines
    ]

    print("\n".join(fixed))


if __name__ == "__main__":
    main()