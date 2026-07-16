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
#   - Installs Python dependencies from scripts/requirements.txt.
#   - Uses Python scripts from the scripts directory.
#   - Reads CoreGX source from example.coregx.
#   - Extracts equations from CoreGX.
#   - Simplifies the expression using SymPy.
#   - Writes intermediate and final outputs to the outputs directory.

set -euo pipefail

SCRIPTS=scripts
OUTPUT_DIR=outputs

pip install -r "$SCRIPTS/requirements.txt"

export PYTHONWARNINGS="ignore::SyntaxWarning"

INPUT=example.coregx

EQUATIONS="$OUTPUT_DIR/equations.json"
OUTPUT="$OUTPUT_DIR/output.tex"


mkdir -p "$OUTPUT_DIR"


python3 "$SCRIPTS/cgx-equations.py" \
    < "$INPUT" \
    > "$EQUATIONS"


python3 "$SCRIPTS/equations-simplify.py" \
    < "$EQUATIONS" \
    > "$OUTPUT"


echo "Equations:          $EQUATIONS"
echo "Simplified TeX:     $OUTPUT"