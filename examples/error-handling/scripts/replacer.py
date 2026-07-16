#!/usr/bin/env python3
"""Working example: CoreGX IR variable replacer.

Usage:

    Linux / macOS / WSL:
        python3 replacer.py repair.json < example.coregx > fixed.coregx

    Windows PowerShell:
        Get-Content .\example.coregx | py -3.12 -X utf8 .\replacer.py .\repair.json | Set-Content -Encoding UTF8 .\fixed.coregx

Notes:
    - Reads CoreGX source from stdin.
    - Reads solved variables from JSON.
    - Replaces variables throughout the IR.
    - Outputs repaired CoreGX source.
"""

import json
import sys
import re


def replace_variables(program, replacements):

    for variable, value in replacements.items():

        program = re.sub(
            rf"\b{variable}\b",
            str(value),
            program
        )

    return program


def main():

    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: replacer.py repair.json"
        )

    repair_file = sys.argv[1]

    with open(repair_file) as f:
        data = json.load(f)


    replacements = data["replacements"]

    program = sys.stdin.read()


    fixed = replace_variables(
        program,
        replacements
    )


    print(fixed)


if __name__ == "__main__":
    main()