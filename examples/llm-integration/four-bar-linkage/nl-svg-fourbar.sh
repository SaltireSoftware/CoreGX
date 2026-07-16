#!/usr/bin/env bash

#
# Input:
#   ./nl-svg-fourbar.sh \
#     "Give me a crank-rocker four-bar linkage with crank AB length 1, \
#      rocker DC length 3, base AD length 3.5, connector BC length 3.7. \
#      Show the coupler curve of a point 3.2 to the right of A and \
#      1.2 below BC."
#
# or
#
#   ./nl-svg-fourbar.sh description.txt
#
# Notes:
#   - Installs Python dependencies from scripts/requirements.txt.
#   - Suppresses Python SyntaxWarning messages.
#   - Uses Python scripts from the scripts directory.
#   - Writes generated CoreGX programs and SVG output to the outputs directory.
#

set -euo pipefail

SCRIPTS=scripts
OUTPUT_DIR=outputs

pip install -r "$SCRIPTS/requirements.txt"

export PYTHONWARNINGS="ignore::SyntaxWarning"

PROGRAM="$OUTPUT_DIR/program.coregx"
OUTPUT="$OUTPUT_DIR/output.svg"


if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "  ./nl-svg-fourbar.sh \"description\""
    echo "  ./nl-svg-fourbar.sh description.txt"
    exit 1
fi


mkdir -p "$OUTPUT_DIR"


if [ -f "$1" ]; then
    python3 "$SCRIPTS/nl-cgx-fourbar.py" --file "$1" > "$PROGRAM"
else
    python3 "$SCRIPTS/nl-cgx-fourbar.py" "$*" > "$PROGRAM"
fi


python3 "$SCRIPTS/cgx-svg.py" \
    < "$PROGRAM" \
    > "$OUTPUT"


echo "CoreGX program: $PROGRAM"
echo "SVG output:     $OUTPUT"