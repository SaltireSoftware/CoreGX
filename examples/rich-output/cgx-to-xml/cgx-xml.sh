#!/usr/bin/env bash
#
# Working example: CoreGX source to XML.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./cgx-xml.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Writes the generated XML to output.xml.
#

set -euo pipefail

INPUT=example.coregx
OUTPUT=output.xml

# Direct conversion: CoreGX source → XML
python3 cgx-xml.py < "$INPUT" > "$OUTPUT"

# Alternatively, generate JSON first and then extract the XML:
#
# JSON=output.json
#
# python3 cgx-json.py < "$INPUT" > "$JSON"
# python3 json-xml.py < "$JSON" > "$OUTPUT"