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
#   - Optionally installs Python dependencies from scripts/requirements.txt.
#   - Suppresses Python SyntaxWarning messages.
#   - Uses Python scripts from the scripts directory.
#   - Reads CoreGX source from example.coregx.
#   - Extracts equations using CoreGX.
#   - Finds critical points using SymPy.
#   - Writes intermediate and final outputs to the outputs directory.
#

set -euo pipefail

SCRIPTS=scripts
OUTPUT_DIR=output

# pip install -r "$SCRIPTS/requirements.txt"

export PYTHONWARNINGS="ignore::SyntaxWarning"

INPUT=example.coregx

EQUATIONS="$OUTPUT_DIR/equations.json"
OUTPUT="$OUTPUT_DIR/output.json"


mkdir -p "$OUTPUT_DIR"


python3 "$SCRIPTS/cgx-equations.py" \
    < "$INPUT" \
    > "$EQUATIONS"


python3 "$SCRIPTS/equations-critical_points.py" \
    < "$EQUATIONS" \
    > "$OUTPUT"


echo "Equations:          $EQUATIONS"
echo "Critical points:    $OUTPUT"