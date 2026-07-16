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
#   - Installs Python dependencies from scripts/requirements.txt.
#   - Suppresses Python SyntaxWarning messages.
#   - Uses Python scripts from the scripts directory.
#   - Writes intermediate equations and final TeX output to the outputs directory.
#

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


python3 "$SCRIPTS/equations-limit.py" \
    < "$EQUATIONS" \
    > "$OUTPUT"


echo "Equations:     $EQUATIONS"
echo "Limit output:  $OUTPUT"