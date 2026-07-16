#!/usr/bin/env bash
#
# Working example: CoreGX source to symbolic limit.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./cgx-limit.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Writes the computed limit as TeX to output.tex.
#

set -euo pipefail

INPUT=example.coregx
EQUATIONS=equations.json
OUTPUT=output.tex

python3 cgx-equations.py < "$INPUT" > "$EQUATIONS"
python3 equations-limit.py < "$EQUATIONS" > "$OUTPUT"