#!/usr/bin/env bash

#
# Working example: CoreGX source to XML.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./get-xml.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Uses Python scripts from the scripts directory.
#   - Writes the generated XML to the output directory.
#

set -euo pipefail

SCRIPTS=scripts
OUTPUT_DIR=output

export PYTHONWARNINGS="ignore::SyntaxWarning"

INPUT=example.coregx

OUTPUT="$OUTPUT_DIR/output.xml"

mkdir -p "$OUTPUT_DIR"

python3 "$SCRIPTS/cgx-xml.py" \
    < "$INPUT" \
    > "$OUTPUT"

echo "XML output:    $OUTPUT"

# Alternatively, generate JSON first and then extract the XML:
#
# JSON="$OUTPUT_DIR/output.json"
#
# python3 "$SCRIPTS/cgx-json.py" \
#     < "$INPUT" \
#     > "$JSON"
#
# python3 "$SCRIPTS/json-xml.py" \
#     < "$JSON" \
#     > "$OUTPUT"
