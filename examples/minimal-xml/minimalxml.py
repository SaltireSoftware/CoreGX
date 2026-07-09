#!/usr/bin/env python3
"""Working example: CoreGX source to XML.

Usage:
    COREGX_API_KEY=your-key python minimalxml.py < program.coregx > output.xml
    
    Powershell:
    Get-Content .\example.coregx | python .\minimalxml.py | output.xml
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
            "xml": True,
        }
    ).encode(),
)

with urllib.request.urlopen(request) as response:
    raw = response.read().decode("utf-8")
    print(raw)
    result = json.loads(raw)

if not result["ok"]:
    raise SystemExit(f"CoreGX error: {result['error']}")

print(result["value"]["xml"])