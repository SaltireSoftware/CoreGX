#!/usr/bin/env bash
#
# Working example: CoreGX source to solved TeX.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./solve_substitute.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Extracts equations.
#   - Solves the symbolic equation.
#   - Substitutes the solution back into the expression.
#   - Writes final TeX output.


set -euo pipefail

INPUT=example.coregx
EQUATIONS=equations.json
SOLUTIONS=solutions.json
OUTPUT=output.tex

python3 cgx-equations.py < "$INPUT" > "$EQUATIONS"
python3 equations-solve.py < "$EQUATIONS" > "$SOLUTIONS"
python3 solved-substitute.py "$EQUATIONS" "$SOLUTIONS" > "$OUTPUT"