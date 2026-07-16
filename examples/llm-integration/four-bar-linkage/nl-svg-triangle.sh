#!/usr/bin/env bash

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

OUTPUT=output.svg
PROGRAM=program.coregx

if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "  ./nl-svg-fourbar.sh \"description\""
    echo "  ./nl-svg-fourbar.sh description.txt"
    exit 1
fi

if [ -f "$1" ]; then
    python3 nl-xgc-fourbar.py --file "$1" > "$PROGRAM"
else
    python3 nl-xgc-fourbar.py "$*" > "$PROGRAM"
fi

python3 nl-xgc-fourbar < "$PROGRAM" > "$OUTPUT"
