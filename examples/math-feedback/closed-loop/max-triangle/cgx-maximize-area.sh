#!/usr/bin/env bash
#
# Working example: CoreGX → critical points → value substitution → SVG.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./cgx-maximize-area.sh
#
# Notes:
#   - Installs Python dependencies from scripts/requirements.txt.
#   - Suppresses Python SyntaxWarning messages.
#   - Reads CoreGX source from example.coregx.
#   - Extracts equations (LaTeX) from the CoreGX program.
#   - Computes critical points using SymPy.
#   - Appends a `value <variable> <number>` statement to the CoreGX program.
#   - Produces a substituted CoreGX program.
#   - Generates SVG output in the outputs directory.
#

set -euo pipefail

SCRIPTS=scripts
OUTPUT_DIR=output

pip install -r "$SCRIPTS/requirements.txt"

export PYTHONWARNINGS="ignore::SyntaxWarning"

INPUT=example.coregx
EQUATIONS="$OUTPUT_DIR/equations.json"
CRITICAL="$OUTPUT_DIR/critical.json"
FIXED="$OUTPUT_DIR/fixed.coregx"
OUTPUT="$OUTPUT_DIR/output.svg"

mkdir -p "$OUTPUT_DIR"


python3 "$SCRIPTS/cgx-equations.py" \
    < "$INPUT" \
    > "$EQUATIONS"


python3 "$SCRIPTS/equations-critical_points.py" \
    < "$EQUATIONS" \
    > "$CRITICAL"


python3 "$SCRIPTS/solved-substitute.py" \
    "$INPUT" \
    "$EQUATIONS" \
    "$CRITICAL" \
    > "$FIXED"


python3 "$SCRIPTS/cgx-svg.py" \
    < "$FIXED" \
    > "$OUTPUT"


echo "Fixed CoreGX program: $FIXED"
echo "SVG output:           $OUTPUT"