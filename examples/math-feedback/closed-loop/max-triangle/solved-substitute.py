#!/usr/bin/env python3
"""
solved-substitute.py

Append a CoreGX `value <variable> <value>` statement to a program.

Accepts either:
    - critical point JSON (with "point" and "value")
    - solved JSON (with "solutions")

If the JSON does not contain a variable name,
the variable name is inferred from equations.json.

Usage:
    python3 solved-substitute.py program.coregx equations.json critical.json > fixed.coregx
"""

import json
import sys
import re


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def infer_variable_from_equations(eq_json):
    if "variable" in eq_json:
        return eq_json["variable"]
    if "variables" in eq_json and eq_json["variables"]:
        return eq_json["variables"][0]
    return "t"


def normalize_json(data, variable_hint):
    # Case 1: critical.json with "point" and "value"
    if isinstance(data, list) and "point" in data[0]:
        return {
            "variable": variable_hint,
            "value": str(data[0]["point"])   # use point, ignore value
        }

    # Case 2: solutions.json
    if isinstance(data, dict) and "solutions" in data:
        return {
            "variable": data["variable"],
            "value": str(data["solutions"][0])
        }

    raise ValueError("Unknown JSON format.")


def append_value(program_text, variable, value):
    pattern = rf"value\s+{variable}\s+.+"
    replacement = f"value {variable} {value}"

    if re.search(pattern, program_text):
        return re.sub(pattern, replacement, program_text)

    return program_text.rstrip() + f"\n{replacement}\n"


def main():
    if len(sys.argv) != 4:
        raise SystemExit(
            "Usage: python3 solved-substitute.py program.coregx equations.json critical.json"
        )

    coregx_path = sys.argv[1]
    equations_path = sys.argv[2]
    json_path = sys.argv[3]

    program = load_text(coregx_path)
    equations = load_json(equations_path)
    data = load_json(json_path)

    variable_hint = infer_variable_from_equations(equations)
    normalized = normalize_json(data, variable_hint)

    variable = normalized["variable"]
    value = normalized["value"]

    substituted = append_value(program, variable, value)

    print(substituted)


if __name__ == "__main__":
    main()
