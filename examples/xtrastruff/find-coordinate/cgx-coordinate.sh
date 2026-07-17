#!/usr/bin/env bash

#
# Working example: CoreGX source to coordinate-substituted SVG.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./cgx_coordinate.sh
#
# Notes:
#   - Installs Python dependencies from scripts/requirements.txt.
#   - Suppresses Python SyntaxWarning messages.
#   - Uses Python scripts from the scripts directory.
#   - Reads CoreGX source from example.coregx.
#   - Extracts equations from CoreGX.
#   - Solves the symbolic expression using SymPy.
#   - Substitutes the solved value back into the CoreGX program.
#   - Generates final XML output.
#   - Writes intermediate and final outputs to the outputs directory.
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


# Extract equations from CoreGX
python3 "$SCRIPTS/cgx-equations.py" \
    < "$INPUT" \
    > "$EQUATIONS"


# Find symbolic solutions
python3 "$SCRIPTS/equations-solve.py" \
    < "$EQUATIONS" \
    > "$CRITICAL"


# Substitute solved value into the CoreGX program
COREGX_SUBSTITUTE_MODE=replace python3 "$SCRIPTS/solved-substitute.py" \
    "$INPUT" \
    "$EQUATIONS" \
    "$CRITICAL" \
    > "$FIXED"


# Render solved CoreGX program
python3 "$SCRIPTS/cgx-svg.py" \
    < "$FIXED" \
    > "$OUTPUT"


echo "Equations:             $EQUATIONS"
echo "Solved CoreGX program: $FIXED"
echo "SVG output:            $OUTPUT"