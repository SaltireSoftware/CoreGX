#!/usr/bin/env bash

#
# Working example: CoreGX source to equations JSON.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./get-equations.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Uses Python scripts from the scripts directory.
#   - Writes the equations JSON to the output directory.
#

set -euo pipefail

SCRIPTS=scripts
OUTPUT_DIR=output

export PYTHONWARNINGS="ignore::SyntaxWarning"

INPUT=example.coregx

OUTPUT="$OUTPUT_DIR/output.json"

mkdir -p "$OUTPUT_DIR"

python3 "$SCRIPTS/cgx-equations.py" \
    < "$INPUT" \
    > "$OUTPUT"

echo "Equations:     $OUTPUT"

# Alternatively, generate full JSON first and then extract the equations:
#
# JSON="$OUTPUT_DIR/output-full.json"
#
# python3 "$SCRIPTS/cgx-json.py" \
#     < "$INPUT" \
#     > "$JSON"
#
# python3 "$SCRIPTS/json-equations.py" \
#     < "$JSON" \
#     > "$OUTPUT"
