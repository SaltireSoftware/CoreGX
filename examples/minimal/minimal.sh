#!/usr/bin/env bash
# Minimal working example: CoreGX source to SVG.
#
# Usage:
#   COREGX_API_KEY=your-key ./minimal.sh < program.coregx > output.svg
set -euo pipefail

program=$(cat)

response=$(curl -s -X POST "https://api.coregx.dev/dev/api/run-coregx" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg apikey "$COREGX_API_KEY" --arg program "$program" '{apikey: $apikey, program: $program, svg: true}')")

if [ "$(echo "$response" | jq -r '.ok')" != "true" ]; then
  echo "CoreGX error: $(echo "$response" | jq -r '.error')" >&2
  exit 1
fi

echo "$response" | jq -r '.value.svg'
