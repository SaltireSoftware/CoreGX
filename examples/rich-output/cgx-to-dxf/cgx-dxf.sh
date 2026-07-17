#!/usr/bin/env bash

#
# Working example: CoreGX source to DXF.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./cgx-dxf.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Uses Python scripts from the scripts directory.
#   - Writes the generated DXF to the output directory.
#

set -euo pipefail

SCRIPTS=scripts
OUTPUT_DIR=output

export PYTHONWARNINGS="ignore::SyntaxWarning"

INPUT=example.coregx

OUTPUT="$OUTPUT_DIR/output.dxf"

mkdir -p "$OUTPUT_DIR"

python3 "$SCRIPTS/cgx-dxf.py" \
    < "$INPUT" \
    > "$OUTPUT"

echo "DXF output:    $OUTPUT"

# Alternatively, generate JSON first and then extract the dxf:
#
# JSON="$OUTPUT_DIR/output.json"
#
# python3 "$SCRIPTS/cgx-json.py" \
#     < "$INPUT" \
#     > "$JSON"
#
# python3 "$SCRIPTS/json-dxf.py" \
#     < "$JSON" \
#     > "$OUTPUT"