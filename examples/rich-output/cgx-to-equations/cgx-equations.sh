#!/usr/bin/env bash
#
# Working example: CoreGX source to equations JSON.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./cgx-equations.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Writes the equations JSON to output.json.
#

set -euo pipefail

INPUT=example.coregx
OUTPUT=output.json

# Direct conversion: CoreGX source → equations JSON
python3 cgx-equations.py < "$INPUT" > "$OUTPUT"

# Alternatively, generate full JSON first and then extract the equations:
#
# JSON=output-full.json
#
# python3 cgx-json.py < "$INPUT" > "$JSON"
# python3 json-equations.py < "$JSON" > "$OUTPUT"