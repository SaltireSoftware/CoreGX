#!/usr/bin/env bash
#
# Working example: CoreGX source to SVG.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./cgx-svg.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Writes the generated SVG to output.svg.
#

set -euo pipefail

INPUT=example.coregx
OUTPUT=output.svg

# Direct conversion: CoreGX source → SVG
python3 cgx-svg.py < "$INPUT" > "$OUTPUT"

# Alternatively, generate JSON first and then extract the SVG:
#
# JSON=output.json
#
# python3 cgx-json.py < "$INPUT" > "$JSON"
# python3 json-svg.py < "$JSON" > "$OUTPUT"