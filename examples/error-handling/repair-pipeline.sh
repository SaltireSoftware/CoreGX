#!/usr/bin/env bash
#
# Working example: CoreGX overconstraint repair pipeline.
#
# Usage:
#
#   Linux / macOS / WSL / Git Bash:
#       ./repair_pipeline.sh
#
# Notes:
#   - Reads CoreGX source from example.coregx.
#   - Runs CoreGX and captures JSON output.
#   - Finds overconstraint error line numbers.
#   - Removes the offending CoreGX lines.
#   - Generates SVG from the repaired CoreGX program.
#

set -euo pipefail

INPUT=example.coregx
ERROR_JSON=coregx.json
FIXED=fixed.coregx
OUTPUT=output.svg


python3 cgx-json.py \
    < "$INPUT" \
    > "$ERROR_JSON"


python3 error-remover.py \
    "$ERROR_JSON" \
    < "$INPUT" \
    > "$FIXED"


python3 cgx-svg.py \
    < "$FIXED" \
    > "$OUTPUT"


echo "Repaired CoreGX: $FIXED"
echo "SVG output:      $OUTPUT"