#!/usr/bin/env bash
#
# Working example: CoreGX → critical points → value substitution → SVG.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./critical_pipeline.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Extracts equations (LaTeX) from the CoreGX program.
#   - Computes critical points using SymPy.
#   - Appends a `value <variable> <number>` statement to the CoreGX program.
#   - Produces a substituted CoreGX program.
#   - Generates SVG output.
#

set -euo pipefail

INPUT=example.coregx
EQUATIONS=equations.json
CRITICAL=critical.json
FIXED=fixed.coregx
OUTPUT=output.svg

# 1. Extract equations from CoreGX
python3 cgx-equations.py < "$INPUT" > "$EQUATIONS"

# 2. Compute critical points
python3 equations-critical_points.py < "$EQUATIONS" > "$CRITICAL"

# 3. Append the critical point as a CoreGX value statement
python3 solved-substitute.py "$INPUT" "$EQUATIONS" "$CRITICAL" > "$FIXED"

# 4. Generate SVG from the substituted CoreGX program
python3 cgx-svg.py < "$FIXED" > "$OUTPUT"

echo "Fixed CoreGX program: $FIXED"
echo "SVG output:           $OUTPUT"
