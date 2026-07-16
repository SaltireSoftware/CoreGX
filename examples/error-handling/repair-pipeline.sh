#!/usr/bin/env bash
#
# Working example: CoreGX overconstraint repair.
#
# Usage:
#
#   ./repair_pipeline.sh
#
# Notes:
#   - Runs CoreGX.
#   - Solves overconstraint equations.
#   - Replaces variables in the original IR.
#

set -euo pipefail

INPUT=example.coregx
ERROR_JSON=coregx.json
REPAIR_JSON=repair.json
OUTPUT=fixed.coregx


python3 cgx-json.py \
    < "$INPUT" \
    > "$ERROR_JSON"


python3 error-solver.py \
    < "$ERROR_JSON" \
    > "$REPAIR_JSON"


python3 replacer.py \
    "$REPAIR_JSON" \
    < "$INPUT" \
    > "$OUTPUT"