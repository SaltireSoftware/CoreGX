import argparse
import json
import sys
import os
import urllib.error
import urllib.request

import openai


COREGX_BASE_URL = "https://api.coregx.dev/dev/api/run-coregx"

def build_system_prompt() -> str:
    """Give the model specialized instructions"""
    parts = ["""You are a geometry interpreter that converts natural language into coreGX commands.
You only understand two commands:

1. triangle A B C
   - Creates triangle ABC.

2. distance X Y value
   - Sets the length of segment XY to the given number.

Rules:
- If the user names a triangle (e.g., “triangle ABC”), create it.
- If the user gives side lengths (e.g., “AB = 3”), output distance commands.
- If the user gives a pattern like “3,4,5 triangle”, interpret it as AB=3, BC=4, AC=5.
- If the user says “draw a 3,4,5 triangle”, output triangle ABC plus the three distances.
- Always output coreGX commands only, one per line.
- Never explain, never comment, never add text.

Examples:

User: triangle ABC has sides AB=3, BC=4, AC=5
Output:
triangle A B C
distance A B  3
distance B C   4
distance A C   5

User: draw a 3,4,5 triangle
Output:
triangle A B C
distance A B   3
distance B C   4
distance A C   5"""]
    return "\n\n---\n\n".join(parts)

def generate_program(client: openai.OpenAI, model: str, system_prompt: str, messages: list) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_prompt}] + messages,
    )
    return response.choices[0].message.content.strip()


FORMAT_REQUEST_FLAGS = {
    "svg": {"svg": True},
    "xml": {"xml": True},
    "tex": {"tex": True},
    "json": {"all": True},
}


def run_coregx(coregx_api_key: str, program: str, request_flags: dict) -> dict:
    request = urllib.request.Request(
        f"{COREGX_BASE_URL}/run-coregx",
        method="POST",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {
                "apikey": coregx_api_key,
                "program": program,
                **request_flags,
            }
        ).encode(),
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.load(response)
    except urllib.error.URLError as e:
        raise SystemExit(f"Could not reach {COREGX_BASE_URL}: {e}")


def format_output(format: str, value: dict) -> str:
    if format == "svg":
        return value["svg"]
    if format == "xml":
        return value["xml"]
    if format == "tex":
        return json.dumps(value.get("equations", {}), indent=2)
    return json.dumps(value, indent=2)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("description", nargs="?", help="The description of the geometry to generate. Otherwise read from --file, or stdin.")
    parser.add_argument("--file", help="Read the description from this file instead of stdin.")
    parser.add_argument("-o", "--output", help="Write the result to this file instead of stdout.")
    parser.add_argument(
        "--format",
        choices=sorted(FORMAT_REQUEST_FLAGS),
        default="svg",
        help="Output format to request from CoreGX (default: svg).",
    )
    parser.add_argument(
        "--max-tries",
        type=int,
        default=1,
        help="Max tries if CoreGX rejects the initial program (default: 1).",
    )
    parser.add_argument("--base-url", help="LLM API base URL (overrides LLM_BASE_URL).")
    parser.add_argument("--llm-key", help="LLM API key (overrides LLM_API_KEY).")
    parser.add_argument("--model", help="LLM model name (overrides LLM_MODEL).")
    parser.add_argument("--coregx-key", help="CoreGX API key (overrides COREGX_API_KEY).")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show debug output (raw program, retries, equations).")
    return parser.parse_args()


def main():
    args = parse_args()

    def print_verbose(*values, **kwargs):
        if args.verbose:
            print(*values, **kwargs)

    if args.file and args.description:
        raise SystemExit("Pass either a description argument or -f/--file, not both.")

    if args.file:
        with open(args.file) as f:
            description = f.read().strip()
    elif args.description:
        description = args.description.strip()
    else:
        description = sys.stdin.read().strip()
    if not description:
        raise SystemExit("No description provided.")

    coregx_api_key = args.coregx_key or os.environ.get("COREGX_API_KEY")
    if not coregx_api_key:
        raise SystemExit("Set the COREGX_API_KEY environment variable or pass --coregx-key.")

    api_key = args.llm_key or os.environ.get("LLM_API_KEY")
    if not api_key:
        raise SystemExit("Set the LLM_API_KEY environment variable or pass --llm-key.")

    model = args.model or os.environ.get("LLM_MODEL")
    if not model:
        raise SystemExit("Set the LLM_MODEL environment variable or pass --model.")

    base_url = args.base_url or os.environ.get("LLM_BASE_URL")
    if not base_url:
        print_verbose("No base URL set. Using default OpenAI API.")

    client = openai.OpenAI(base_url=base_url, api_key=api_key) if base_url else openai.OpenAI(api_key=api_key)

    system_prompt = build_system_prompt()

    print_verbose(f"Description: {description}\n")

    messages = [{"role": "user", "content": description}]
    try:
        program = generate_program(client, model, system_prompt, messages)
    except openai.AuthenticationError:
        raise SystemExit("Invalid LLM API key.")
    except openai.RateLimitError:
        raise SystemExit("Rate limited.")
    except openai.APIError as e:
        raise SystemExit(f"API error: {e}")

    print_verbose("=== LLM-generated CoreGX program ===")
    print_verbose(program)
    print_verbose()

    request_flags = FORMAT_REQUEST_FLAGS[args.format]
    result = run_coregx(coregx_api_key, program, request_flags)

    tries = 1
    while not result["ok"] and tries < args.max_tries:
        # The LLM's program didn't hold up under CoreGX's solver.
        # Feed the error back and let the model correct it, then retry.
        print_verbose(f"CoreGX rejected the program: {result['error']}")

        tries += 1
        print_verbose(f"Retrying ({tries}/{args.max_tries}) with the error fed back to the LLM...\n")

        messages += [
            {"role": "assistant", "content": program},
            {
                "role": "user",
                "content": (
                    f"That program failed with error: {result['error']}\n"
                    "Output a corrected CoreGX program only."
                ),
            },
        ]
        program = generate_program(client, model, system_prompt, messages)

        print_verbose("=== LLM-generated CoreGX program ===")
        print_verbose(program)
        result = run_coregx(coregx_api_key, program, request_flags)

    print_verbose("=== Result from CoreGX API ===")
    if not result["ok"]:
        raise SystemExit(f"Still failed after {tries} tries: {result['error']}")

    output_content = format_output(args.format, result["value"])

    if args.output:
        print_verbose(output_content)
        with open(args.output, "w") as f:
            f.write(output_content)
        print_verbose(f"Wrote {args.output}")
    else:
        print(output_content)


if __name__ == "__main__":
    main()
