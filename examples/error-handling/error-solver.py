#!/usr/bin/env python3
"""Working example: CoreGX overconstraint equation solver.

Usage:

    Linux / macOS / WSL:
        python3 error-solver.py < coregx.json > repair.json

    Windows PowerShell:
        Get-Content .\coregx.json -Raw | py -3.12 -X utf8 .\error-solver.py | Set-Content -Encoding UTF8 .\repair.json

Notes:
    - Reads CoreGX JSON from stdin.
    - Extracts overconstraint equations.
    - Solves them using SymPy.
    - Outputs variable replacements.
"""

import json
import sys
import re

import sympy as sp


def normalize(expr):
    return expr.replace("^", "**")


def variables(expr):

    names = re.findall(
        r"[a-zA-Z]+",
        expr
    )

    return sorted(
        set(names) - {"sqrt"}
    )


def solve_equation(equation):

    lhs, rhs = equation.split("=")

    names = variables(equation)

    if len(names) != 1:
        raise RuntimeError(
            "Expected one variable"
        )

    symbol = sp.symbols(names[0])

    lhs = sp.sympify(
        normalize(lhs)
    )

    rhs = sp.sympify(
        normalize(rhs)
    )

    solutions = sp.solve(
        sp.Eq(lhs, rhs),
        symbol
    )

    if not solutions:
        raise RuntimeError(
            "No solution"
        )

    return {
        str(symbol): solutions[0]
    }


def main():

    data = json.load(sys.stdin)

    errors = (
        data
        .get("value", {})
        .get("errors", [])
    )

    replacements = {}

    for error in errors:

        if error["type"] != "overconstraint_error":
            continue

        replacements.update(
            solve_equation(
                error["equation"]
            )
        )

    print(
        json.dumps(
            {
                "replacements": {
                    k: str(v)
                    for k, v in replacements.items()
                }
            },
            indent=2
        )
    )


if __name__ == "__main__":
    main()