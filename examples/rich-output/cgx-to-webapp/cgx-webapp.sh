#!/usr/bin/env bash

#
# Working example: CoreGX source to web app.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./cgx-webapp.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Uses Python scripts from the scripts directory.
#   - Writes the generated web app to the output directory.
#

set -euo pipefail

SCRIPTS=scripts
OUTPUT_DIR=output

export PYTHONWARNINGS="ignore::SyntaxWarning"

INPUT=example.coregx

OUTPUT="$OUTPUT_DIR/output.html"

mkdir -p "$OUTPUT_DIR"

python3 "$SCRIPTS/cgx-webapp.py" \
    < "$INPUT" \
    > "$OUTPUT"

echo "Web app:       $OUTPUT"

# Alternatively, generate JSON first and then extract the web app:
#
# JSON="$OUTPUT_DIR/output.json"
#
# python3 "$SCRIPTS/cgx-json.py" \
#     < "$INPUT" \
#     > "$JSON"
#
# python3 "$SCRIPTS/json-webapp.py" \
#     < "$JSON" \
#     > "$OUTPUT"