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
#   - Writes the generated web app to output.html.
#

set -euo pipefail

INPUT=example.coregx
OUTPUT=output.html

# Direct conversion: CoreGX source → web app
python3 cgx-webapp.py < "$INPUT" > "$OUTPUT"

# Alternatively, generate JSON first and then extract the web app:
#
# JSON=output.json
#
# python3 cgx-json.py < "$INPUT" > "$JSON"
# python3 json-webapp.py < "$JSON" > "$OUTPUT"