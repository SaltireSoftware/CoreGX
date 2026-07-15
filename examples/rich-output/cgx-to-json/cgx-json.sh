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
#   - Writes the generated JSON to output.json.

set -euo pipefail

INPUT=example.coregx
OUTPUT=output.json

python3 cgx-json.py < "$INPUT" > "$OUTPUT"