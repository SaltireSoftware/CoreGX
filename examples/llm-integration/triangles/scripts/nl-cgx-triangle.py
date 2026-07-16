#!/usr/bin/env python3
"""Working example: Natural language to CoreGX.

Usage:

    Linux / macOS / WSL (bash, zsh):

        python3 nl-cgx-triangle.py "draw a 3,4,5 triangle" > program.coregx

        python3 nl-cgx-triangle.py --file description.txt > program.coregx

        cat description.txt | python3 nl-cgx-triangle.py > program.coregx

    Windows PowerShell:

        py -3 -X utf8 ./nl-cgx-triangle.py "draw a 3,4,5 triangle" |
            Set-Content -Encoding UTF8 program.coregx

        Get-Content ./description.txt -Raw |
            py -3 -X utf8 ./nl-cgx-triangle.py |
            Set-Content -Encoding UTF8 program.coregx

    Windows Command Prompt (cmd.exe):

        py nl-cgx-triangle.py "draw a 3,4,5 triangle" > program.coregx

        type description.txt | py nl-cgx-triangle.py > program.coregx

    Windows Git Bash:

        ./nl-cgx-triangle.py "draw a 3,4,5 triangle" > program.coregx

Notes:
    - Reads the description from a command-line argument, a file, or stdin.
    - Outputs a CoreGX program.
    - LLM configuration is taken from LLM_API_KEY, LLM_MODEL, and optionally LLM_BASE_URL.
"""

import argparse
import os
import sys

import openai


def build_system_prompt() -> str:
    return """You are a geometry interpreter that converts natural language into coreGX commands.
You only understand two commands:

1. triangle A B C
   - Creates triangle ABC.

2. distance X Y value
   - Sets the length of segment XY to the given number.

Rules:
- If the user names a triangle (e.g., "triangle ABC"), create it.
- If the user gives side lengths (e.g., "AB = 3"), output distance commands.
- If the user gives a pattern like "3,4,5 triangle", interpret it as AB=3, BC=4, AC=5.
- If the user says "draw a 3,4,5 triangle", output triangle ABC plus the three distances.
- Always output CoreGX commands only, one per line.
- Never explain, never comment, never add text.

Examples:

User: triangle ABC has sides AB=3, BC=4, AC=5

Output:
triangle A B C
distance A B 3
distance B C 4
distance A C 5

User: draw a 3,4,5 triangle

Output:
triangle A B C
distance A B 3
distance B C 4
distance A C 5
"""


def generate_program(client, model, prompt, description):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": description},
        ],
    )
    return response.choices[0].message.content.strip()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "description",
        nargs="?",
        help="Geometry description. If omitted, read from --file or stdin.",
    )

    parser.add_argument(
        "--file",
        help="Read description from a file.",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Write CoreGX program to this file instead of stdout.",
    )

    parser.add_argument("--base-url")
    parser.add_argument("--llm-key")
    parser.add_argument("--model")

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if args.file and args.description:
        raise SystemExit("Pass either a description or --file, not both.")

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            description = f.read().strip()
    elif args.description:
        description = args.description
    else:
        description = sys.stdin.read().strip()

    if not description:
        raise SystemExit("No description provided.")

    api_key = args.llm_key or os.environ.get("LLM_API_KEY")
    if not api_key:
        raise SystemExit("Set LLM_API_KEY.")

    model = args.model or os.environ.get("LLM_MODEL")
    if not model:
        raise SystemExit("Set LLM_MODEL.")

    base_url = args.base_url or os.environ.get("LLM_BASE_URL")

    client = (
        openai.OpenAI(api_key=api_key)
        if base_url is None
        else openai.OpenAI(api_key=api_key, base_url=base_url)
    )

    program = generate_program(
        client,
        model,
        build_system_prompt(),
        description,
    )

    if args.verbose:
        print("=== Description ===", file=sys.stderr)
        print(description, file=sys.stderr)
        print(file=sys.stderr)
        print("=== CoreGX program ===", file=sys.stderr)
        print(program, file=sys.stderr)
        print(file=sys.stderr)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(program)
    else:
        print(program)


if __name__ == "__main__":
    main()