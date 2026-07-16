#!/usr/bin/env python3
"""
Equations JSON to symbolic solutions.

Uses:
    valueTex = symbolic expression
    valueRealAsTex = target value

Solves:

    expression = valueRealAsTex

Usage:

    python3 equations-solve.py < equations.json > solutions.json


Optional target override:

    python3 equations-solve.py 100 < equations.json > solutions.json
"""

import json
import sys

import sympy as sp
from sympy.parsing.latex import parse_latex


data = json.load(sys.stdin)

if not data:
    raise SystemExit("No equations found.")


equation_data = data[0]


expr = parse_latex(
    equation_data["valueTex"]
)


symbols = list(expr.free_symbols)

if len(symbols) != 1:
    raise SystemExit(
        f"Expression must contain exactly one free symbol. Found: {symbols}"
    )


variable = symbols[0]


# Optional command-line target
if len(sys.argv) > 1:
    target = parse_latex(sys.argv[1])

# Otherwise use CoreGX evaluated value
else:
    target = sp.Float(
        equation_data["valueRealAsTex"]
    )


equation = sp.Eq(
    expr,
    target
)


solutions = sp.solve(
    equation,
    variable
)


real_solutions = []

for solution in solutions:
    solution = sp.simplify(solution)

    if solution.has(sp.I):
        continue

    real_solutions.append(solution)


print(
    json.dumps(
        {
            "expression": sp.latex(expr),
            "target": sp.latex(target),
            "equation": sp.latex(equation),
            "variable": str(variable),
            "solutions": [
                sp.latex(s)
                for s in real_solutions
            ],
        },
        indent=2,
    )
)