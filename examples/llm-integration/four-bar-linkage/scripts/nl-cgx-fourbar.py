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

You understand four-bar linkages using this CoreGX structure:

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

point M
distance M BC u
distance M l v

locus loc M t 0 6.283

The linkage parameters are:

d = crank/input link length (AB)
c = coupler/connecting rod length (BC)
f = rocker/output link length (CD)
b = ground/base/frame length (AD)

Map terminology:

crank length, input link, driving link, AB length → d

coupler length, connecting rod length, BC length → c

rocker length, follower length, output link, DC length → f

ground link, base length, AD length, frame length → b

The coupler point M is positioned using the parameters u and v:

distance M BC u
distance M l v

The parameters u and v control the location of M relative to the moving coupler link BC.

If the user specifies u and v explicitly, use those values. 
u and v are always positive values and can never be negative. 

Otherwise use:

value u 1
value v 1

If the user describes a coupler point relative to another object, convert it into the closest u/v description relative to BC when possible.

Always create the four-bar structure:

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

point M
distance M BC u
distance M l v

locus loc M t 0 6.283

If a coupler point M is requested, add segments connecting the moving linkage points to M:

segment B M color=pink
segment C M color=pink

These segments visually show the coupler point relationship.

Always add the requested parameter values:

value d <number>
value c <number>
value f <number>
value b <number>

For the crank angle:

- If the user specifies an initial angle:
  value t <angle>

- Otherwise omit value t.

For linkage assembly:

- Standard, open, or uncrossed crank-rocker:
  clockwise B C D

- Crossed linkage:
  omit clockwise B C D

Linkage types:

- crank-rocker:
  AB is the crank and CD is the rocker.
  Use clockwise B C D unless crossed is requested.

- double rocker:
  Assign the provided input and output links to d and f.

- drag link:
  Use the provided lengths directly.


Always end animated linkages with:

animate t 0 6.283


Example:

User:
give me a crank rocker four bar linkage with crank AB length 1, rocker DC length 3, base AD length 3.5 and connector BC length 3.7. Show the coupler curve of a point distance 3.2 to the right of A and 1.2 below BC.

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
point M
distance M BC u
distance M l v
locus loc M t 0 6.283
segment B M color=pink
segment C M color=pink
value d 1
value c 3.7
value f 3
value b 3.5
value u 3.2
value v 1.2
clockwise B C D
animate t 0 6.283


Example:

User:
create a four bar with AB 2, BC 5, CD 4, AD 6.

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
point M
distance M BC u
distance M l v
locus loc M t 0 6.283
segment B M color=pink
segment C M color=pink
value u 1
value v 1
value d 2
value c 5
value f 4
value b 6
animate t 0 6.283


Example:

User:
create a four bar linkage with AB length 1, BC length 4.5, CD length 3.5, AD length 4.5 with crank angle 1.05.

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
point M
distance M BC u
distance M l v
locus loc M t 0 6.283
segment B M color=pink
segment C M color=pink
value t 1.05
value u 1
value v 1
clockwise B C D
value d 1
value c 4.5
value f 3.5
value b 4.5
animate t 0 6.283
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