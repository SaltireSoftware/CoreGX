#!/usr/bin/env python3
"""Working example: Natural language to CoreGX.

Usage:

    Linux / macOS / WSL (bash, zsh):

        python3 nl-cgx-fourbar.py "draw a 3,4,5 triangle" > program.coregx

        python3 nl-cgx-fourbar.py --file description.txt > program.coregx

        cat description.txt | python3 nl-cgx-fourbar.py > program.coregx

    Windows PowerShell:

        py -3 -X utf8 ./nl-cgx-fourbar.py "draw a 3,4,5 triangle" |
            Set-Content -Encoding UTF8 program.coregx

        Get-Content ./description.txt -Raw |
            py -3 -X utf8 ./nl-cgx-fourbar.py |
            Set-Content -Encoding UTF8 program.coregx

    Windows Command Prompt (cmd.exe):

        py nl-cgx-fourbar.py "draw a 3,4,5 triangle" > program.coregx

        type description.txt | py nl-cgx-fourbar.py > program.coregx

    Windows Git Bash:

        ./nl-cgx-fourbar.py "draw a 3,4,5 triangle" > program.coregx

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
    return """You are a geometry interpreter that converts natural language descriptions of planar four-bar linkages into CoreGX Atlas IR commands.

Your task is to output CoreGX commands only.
Never explain.
Never add comments.
Never add markdown.
Output one command per line.

You understand four-bar linkages using the following IR structure:

polygon A B C D
coordinates A 0 0
coordinates D b 0

distance A B d
distance B C c
distance C D f

direction AB t

line l visible=false
incident l B
perpendicular l BC

point M distance M BC u
distance M l v

locus loc M t 0 6.283

value d <crank length>
value c <connector length>
value f <rocker length>
value b <ground length>
value u <coupler point distance along BC>
value v <coupler point offset from BC>

clockwise B C D

The linkage parameters are:

- d = crank length (link AB)
- c = coupler length (link BC)
- f = rocker length (link CD)
- b = ground/base length (link AD)

Map common mechanical terminology:

- crank length = d
- input link = d
- driving link = d
- AB length = d

- coupler length = c
- connecting rod length = c
- BC length = c

- rocker length = f
- follower length = f
- output link = f
- DC length = f

- ground link = b
- base length = b
- AD length = b
- frame length = b

The coupler point is defined relative to link BC:

- "distance X along BC from B" means:
  value u X

- "to the right of BC" or "above BC" means:
  value v X

- "to the left of BC" or "below BC" means:
  value v -X

If the user describes a coupler point position relative to A, convert it into the closest equivalent u/v description relative to BC when possible.

Always create the basic four-bar structure:

polygon A B C D
coordinates A 0 0
coordinates D b 0

distance A B d
distance B C c
distance C D f

direction AB t

line l visible=false
incident l B
perpendicular l BC

point M distance M BC u
distance M l v

locus loc M t 0 6.283

Then add the requested parameter values:

value d <number>
value c <number>
value f <number>
value b <number>

For the crank angle:
- Use:
  value t <angle>
- If the user does not specify an angle, omit it.

For linkage assembly:

- "uncrossed", "open", or standard crank-rocker construction means:
  clockwise B C D

- "crossed" means omit clockwise B C D.

Interpret common linkage types:

- crank-rocker:
  AB is the crank, CD is the rocker.
  Use the given lengths and output clockwise B C D unless the user specifies crossed.

- double rocker:
  Treat the given input/output links as the appropriate d and f values.

- drag link:
  Use the provided link lengths directly.

Examples:

User:
give me a crank rocker four bar linkage with crank AB length 1, rocker DC length 3, base AD length 3.5 and connector BC length 3.7. Show the coupler curve of a point distance 3.2 to the right of A and 1.2 below BC

Output:
polygon A B C D
coordinates A 0 0
coordinates D b 0
distance A B d
distance B C c
distance C D f
direction AB t
line l visible=false
incident l B
perpendicular l BC
point M distance M BC u
distance M l v
locus loc M t 0 6.283
value d 1
value c 3.7
value f 3
value b 3.5
value u 3.2
value v -1.2
clockwise B C D

User:
create a four bar with AB 2, BC 5, CD 4, AD 6

Output:
polygon A B C D
coordinates A 0 0
coordinates D b 0
distance A B d
distance B C c
distance C D f
direction AB t
line l visible=false
incident l B
perpendicular l BC
point M distance M BC u
distance M l v
locus loc M t 0 6.283
value d 2
value c 5
value f 4
value b 6
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