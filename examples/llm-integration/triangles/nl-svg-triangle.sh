#!/usr/bin/env bash

# Input:
#   ./nl-svg-triangle.sh "draw a 3,4,5 triangle"
#
# or
#
#   ./nl-svg-triangle.sh description.txt

OUTPUT=output.svg
PROGRAM=program.coregx

if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "  ./nl-svg-triangle.sh \"description\""
    echo "  ./nl-svg-triangle.sh description.txt"
    exit 1
fi

if [ -f "$1" ]; then
    python3 nl-cgx-triangle.py --file "$1" > "$PROGRAM"
else
    python3 nl-cgx-triangle.py "$*" > "$PROGRAM"
fi

python3 nl-cgx-triangle < "$PROGRAM" > "$OUTPUT"
