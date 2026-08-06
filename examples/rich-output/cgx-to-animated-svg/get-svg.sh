#!/usr/bin/env bash

#
# Working example: CoreGX source to SVG.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./get-svg.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Writes the generated SVG to the outputs directory.
#   - Uses Python scripts from the scripts directory.
#

set -euo pipefail

SCRIPTS=scripts
OUTPUT_DIR=output

export PYTHONWARNINGS="ignore::SyntaxWarning"

INPUT=example.coregx

OUTPUT="$OUTPUT_DIR/output.svg"

mkdir -p "$OUTPUT_DIR"

python3 "$SCRIPTS/cgx-svg.py" \
    < "$INPUT" \
    > "$OUTPUT"

echo "SVG output:    $OUTPUT"

# Alternatively, generate JSON first and then extract the SVG:
#
# JSON="$OUTPUT_DIR/output.json"
#
# python3 "$SCRIPTS/cgx-json.py" \
#     < "$INPUT" \
#     > "$JSON"
#
# python3 "$SCRIPTS/json-svg.py" \
#     < "$JSON" \
#     > "$OUTPUT"
