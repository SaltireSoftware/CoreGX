#!/usr/bin/env bash
#
# Working example: CoreGX source to simplified TeX.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./cgx-simplify.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Extracts equations from CoreGX.
#   - Simplifies the expression using SymPy.
#   - Writes the result as TeX to output.tex.
#

set -euo pipefail

INPUT=example.coregx
EQUATIONS=equations.json
OUTPUT=output.tex

python3 cgx-equations.py < "$INPUT" > "$EQUATIONS"
python3 equations-simplify.py < "$EQUATIONS" > "$OUTPUT"