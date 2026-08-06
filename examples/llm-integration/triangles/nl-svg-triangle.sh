#!/usr/bin/env bash

#
# Input:
#   ./nl-svg-triangle.sh "draw a 3,4,5 triangle"
#
# or
#
#   ./nl-svg-triangle.sh description.txt
#
# Notes:
#   - Optionally Installs Python dependencies from requirements.txt.
#   - Suppresses Python SyntaxWarning messages.
#   - Uses Python scripts from the scripts directory.
#   - Writes generated CoreGX programs and SVG output to the outputs directory.
#

set -euo pipefail

# pip install -r scripts/requirements.txt

export PYTHONWARNINGS="ignore::SyntaxWarning"

SCRIPTS=scripts
OUTPUT_DIR=output
SYSTEM_PROMPT="$SCRIPTS/system-prompt.txt"

PROGRAM="$OUTPUT_DIR/program.coregx"
OUTPUT="$OUTPUT_DIR/output.svg"


if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "  ./nl-svg-triangle.sh \"description\""
    echo "  ./nl-svg-triangle.sh description.txt"
    exit 1
fi


mkdir -p "$OUTPUT_DIR"


if [ -f "$1" ]; then
    python3 "$SCRIPTS/nl-cgx.py" --system-prompt "$SYSTEM_PROMPT" --file "$1" > "$PROGRAM"
else
    python3 "$SCRIPTS/nl-cgx.py" --system-prompt "$SYSTEM_PROMPT" "$*" > "$PROGRAM"
fi


python3 "$SCRIPTS/cgx-svg.py" \
    < "$PROGRAM" \
    > "$OUTPUT"


echo "CoreGX program: $PROGRAM"
echo "SVG output:     $OUTPUT"
