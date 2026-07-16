#!/usr/bin/env bash
#
# Working example: CoreGX source to optimized SVG.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./critical_pipeline.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Extracts equations.
#   - Finds critical points using SymPy.
#   - Substitutes the optimal value back into the CoreGX program.
#   - Generates final SVG output.

set -euo pipefail

INPUT=example.coregx
EQUATIONS=equations.json
CRITICAL=critical.json
FIXED=fixed.coregx
OUTPUT=output.svg

# Extract equations from CoreGX
python3 cgx-equations.py < "$INPUT" > "$EQUATIONS"

# Find critical points and evaluate them
python3 equations-solve.py < "$EQUATIONS" > "$CRITICAL"

# Substitute the optimal value into the CoreGX program
COREGX_SUBSTITUTE_MODE=value python3 solved-substitute.py "$INPUT" "$EQUATIONS" "$CRITICAL" > "$FIXED"

# Render the solved CoreGX program
python3 cgx-svg.py < "$FIXED" > "$OUTPUT"

echo "Solved CoreGX program: $FIXED"
echo "SVG output:            $OUTPUT"