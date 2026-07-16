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
#   - Python scripts are stored in the scripts directory.
#   - Pipeline outputs are stored in the outputs directory.
#

set -euo pipefail
pip install -r scripts/requirements.txt
export PYTHONWARNINGS="ignore::SyntaxWarning"

INPUT=example.coregx

SCRIPTS=scripts
OUTPUT_DIR=outputs

ERROR_JSON="$OUTPUT_DIR/error.json"
FIXED="$OUTPUT_DIR/fixed.coregx"
OUTPUT="$OUTPUT_DIR/output.svg"


mkdir -p "$OUTPUT_DIR"


python3 "$SCRIPTS/cgx-json.py" \
    < "$INPUT" \
    > "$ERROR_JSON"


python3 "$SCRIPTS/error-remover.py" \
    "$ERROR_JSON" \
    < "$INPUT" \
    > "$FIXED"


python3 "$SCRIPTS/cgx-svg.py" \
    < "$FIXED" \
    > "$OUTPUT"


echo "Repaired CoreGX: $FIXED"
echo "SVG output:      $OUTPUT"