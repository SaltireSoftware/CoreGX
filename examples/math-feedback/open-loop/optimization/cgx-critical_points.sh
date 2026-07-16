#!/usr/bin/env bash
#
# Working example: CoreGX source to critical points.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./equations-critical_points.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Extracts equations using CoreGX.
#   - Finds critical points using SymPy.
#   - Writes results to output.json.
#

set -euo pipefail

INPUT=example.coregx
EQUATIONS=equations.json
OUTPUT=output.json

python3 cgx-equations.py < "$INPUT" > "$EQUATIONS"
python3 equations-critical_points.py < "$EQUATIONS" > "$OUTPUT"