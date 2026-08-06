#!/usr/bin/env python3
"""
substitute.py

Substitute a solved variable into a CoreGX program.

Modes:
    replace (default):
        Replaces every standalone occurrence of the variable.

    value:
        Appends a CoreGX `value <variable> <value>` statement.

Usage:
    python3 substitute.py program.coregx equations.json critical.json > fixed.coregx

Optional:
    COREGX_SUBSTITUTE_MODE=value
"""

import json
import sys
import re
import os

from sympy.parsing.latex import parse_latex


# Default behavior
MODE = os.environ.get("COREGX_SUBSTITUTE_MODE", "replace")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def infer_variable_from_equations(eq_json):
    if isinstance(eq_json, dict):
        if "variable" in eq_json:
            return eq_json["variable"]

        if "variables" in eq_json and eq_json["variables"]:
            return eq_json["variables"][0]

    if isinstance(eq_json, list) and eq_json:
        value_tex = eq_json[0].get("valueTex")

        if value_tex:
            expr = parse_latex(value_tex)
            symbols = list(expr.free_symbols)

            if len(symbols) == 1:
                return str(symbols[0])

    raise ValueError("Could not infer variable from equations.")


def normalize_json(data, variable_hint):
    # critical.json
    if isinstance(data, list) and data and "point" in data[0]:
        return {
            "variable": variable_hint,
            "value": str(data[0]["point"])
        }

    # solutions.json
    if isinstance(data, dict) and "solutions" in data:
        return {
            "variable": data.get("variable", variable_hint),
            "value": str(data["solutions"][0])
        }

    raise ValueError("Unknown JSON format.")


def replace_variable(program_text, variable, value):
    """
    Replace standalone variable references only.

    Prevents replacing variables inside words:
        x -> 6
        box stays box
    """

    pattern = rf"\b{re.escape(variable)}\b"

    return re.sub(pattern, value, program_text)


def append_value(program_text, variable, value):
    pattern = rf"value\s+{re.escape(variable)}\s+.+"
    replacement = f"value {variable} {value}"

    if re.search(pattern, program_text):
        return re.sub(pattern, replacement, program_text)

    return program_text.rstrip() + f"\n{replacement}\n"


def main():
    if len(sys.argv) != 4:
        raise SystemExit(
            "Usage: python3 substitute.py program.coregx equations.json critical.json"
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

    if MODE == "value":
        result = append_value(program, variable, value)
    elif MODE == "replace":
        result = replace_variable(program, variable, value)
    else:
        raise ValueError(
            f"Unknown COREGX_SUBSTITUTE_MODE={MODE}. Use 'replace' or 'value'."
        )

    print(result)


if __name__ == "__main__":
    main()
