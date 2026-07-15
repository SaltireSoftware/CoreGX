#!/usr/bin/env python3
"""Convert a natural language geometry description into CoreGX source.

Usage:

    Linux / macOS / WSL (bash, zsh):
        LLM_API_KEY=your-key LLM_MODEL=model-name python3 description_to_coregx.py "draw a 3,4,5 triangle"

    Windows PowerShell:
        $env:LLM_API_KEY="your-key"
        $env:LLM_MODEL="model-name"
        python .\description_to_coregx.py "draw a 3,4,5 triangle"

    Windows Command Prompt (cmd.exe):
        set LLM_API_KEY=your-key
        set LLM_MODEL=model-name
        python description_to_coregx.py "draw a 3,4,5 triangle"

    Windows Git Bash:
        export LLM_API_KEY=your-key
        export LLM_MODEL=model-name
        ./description_to_coregx.py "draw a 3,4,5 triangle"

Notes:
    - Reads the description from the command line argument or stdin.
    - Writes CoreGX commands to stdout.
"""

import os
import sys
import openai


def build_system_prompt():
    return """You are a geometry interpreter that converts natural language into coreGX commands.

You only understand two commands:

1. triangle A B C
   - Creates triangle ABC.

2. distance X Y value
   - Sets the length of segment XY to the given number.

Rules:
- If the user names a triangle, create it.
- If the user gives side lengths, output distance commands.
- "3,4,5 triangle" means AB=3, BC=4, AC=5.
- Always output coreGX commands only.
- Never explain or add comments.

Examples:

User:
draw a 3,4,5 triangle

Output:
triangle A B C
distance A B 3
distance B C 4
distance A C 5
"""


def main():
    description = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else sys.stdin.read().strip()
    )

    if not description:
        raise SystemExit("No description provided.")

    api_key = os.environ.get("LLM_API_KEY")
    model = os.environ.get("LLM_MODEL")
    base_url = os.environ.get("LLM_BASE_URL")

    if not api_key:
        raise SystemExit("Set LLM_API_KEY.")
    if not model:
        raise SystemExit("Set LLM_MODEL.")

    client = (
        openai.OpenAI(base_url=base_url, api_key=api_key)
        if base_url
        else openai.OpenAI(api_key=api_key)
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": build_system_prompt(),
            },
            {
                "role": "user",
                "content": description,
            },
        ],
    )

    print(response.choices[0].message.content.strip())


if __name__ == "__main__":
    main()