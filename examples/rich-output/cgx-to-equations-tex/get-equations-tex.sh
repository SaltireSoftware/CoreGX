#!/usr/bin/env bash

#
# Working example: CoreGX source to TeX.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       export COREGX_API_KEY=your-key
#       ./get-equations-tex.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Uses Python scripts from the scripts directory.
#   - Writes the generated TeX to the output directory.
#

set -euo pipefail

SCRIPTS=scripts
OUTPUT_DIR=output

export PYTHONWARNINGS="ignore::SyntaxWarning"

INPUT=example.coregx

OUTPUT="$OUTPUT_DIR/output.tex"

mkdir -p "$OUTPUT_DIR"

python3 "$SCRIPTS/cgx-tex.py" \
    < "$INPUT" \
    > "$OUTPUT"

echo "TeX output:    $OUTPUT"
