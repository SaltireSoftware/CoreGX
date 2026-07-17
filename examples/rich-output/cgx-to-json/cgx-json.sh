#!/usr/bin/env bash

#
# Working example: CoreGX source to JSON.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./cgx-json.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Uses Python scripts from the scripts directory.
#   - Writes the generated JSON to the output directory.
#

set -euo pipefail

SCRIPTS=scripts
OUTPUT_DIR=output

export PYTHONWARNINGS="ignore::SyntaxWarning"

INPUT=example.coregx

OUTPUT="$OUTPUT_DIR/output.json"

mkdir -p "$OUTPUT_DIR"

python3 "$SCRIPTS/cgx-json.py" \
    < "$INPUT" \
    > "$OUTPUT"

echo "JSON output:   $OUTPUT"