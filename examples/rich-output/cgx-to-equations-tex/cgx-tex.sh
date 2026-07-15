#!/usr/bin/env bash
#
# Working example: CoreGX source to TeX.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./cgx-tex.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Writes the generated TeX to output.tex.
#

set -euo pipefail

INPUT=example.coregx
OUTPUT=output.tex

python3 cgx-tex.py < "$INPUT" > "$OUTPUT"