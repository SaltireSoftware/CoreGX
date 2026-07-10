#!/usr/bin/env python3
"""Working example: CoreGX source to JSON.

Usage:
    COREGX_API_KEY=your-key python minimaljson.py < program.coregx > output.json

    Powershell:
    Get-Content .\example.coregx | python .\minimaljson.py |  output.json
"""

import json
import os
import sys
import urllib.request

program = sys.stdin.read()

request = urllib.request.Request(
    "https://api.coregx.dev/dev/api/run-coregx",
    method="POST",
    headers={"Content-Type": "application/json", "User-Agent": "some-other-user-agent"},
    data=json.dumps(
        {
            "apikey": os.environ["COREGX_API_KEY"],
            "program": program,
            "all": True,
        }
    ).encode(),
)

with urllib.request.urlopen(request) as response:
    result = json.load(response)

if not result["ok"]:
    raise SystemExit(f"CoreGX error: {result['error']}")

print(json.dumps(result, indent=2))
