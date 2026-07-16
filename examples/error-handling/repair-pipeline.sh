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
#   - Solves overconstraint equations using SymPy.
#   - Replaces solved variables in the original IR.
#   - Generates SVG from the repaired CoreGX program.
#

set -euo pipefail

INPUT=example.coregx
ERROR_JSON=coregx.json
REPAIR_JSON=repair.json
FIXED=fixed.coregx
OUTPUT=output.svg


python3 cgx-json.py \
    < "$INPUT" \
    > "$ERROR_JSON"


python3 error-solver.py \
    < "$ERROR_JSON" \
    > "$REPAIR_JSON"


python3 replacer.py \
    "$REPAIR_JSON" \
    < "$INPUT" \
    > "$FIXED"


python3 cgx-svg.py \
    < "$FIXED" \
    > "$OUTPUT"

echo "Repaired CoreGX: $FIXED"
echo "SVG output:      $OUTPUT"
