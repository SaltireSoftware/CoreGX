# Small Prompt Pipeline Example

A workflow example showing a complete pipeline using the CoreGX API, a small constrained prompt, and an LLM to take a natural language description and generate a diagram.

```
[natural language]  ── LLM ─➤  [CoreGX program]  ── CoreGX API ─➤  [diagram]
```

## Setup

Works with any OpenAI-compatible chat completions API. Pass your API key, model name, and optionally a base URL via environment variables. If no base URL is provided, the default OpenAI API is used.

```bash
export LLM_API_KEY=your-llm-api-key
export LLM_BASE_URL=https://api.openai.com/v1  # optional - omit to use the default OpenAI API, or point at another provider
export LLM_MODEL=gpt-5.4
export COREGX_API_KEY=your-coregx-key
```

Each of these can also be passed as a command-line flag: `--llm-key`, `--base-url`, `--model`, `--coregx-key`.

Requires the `openai` Python package:

```bash
pip install openai
```

## Run

The natural language description can be provided as a positional argument, a file with `--file`, or stdin:

```bash
# argument
python triangle-llm.py "A right triangle with legs 3 and 4, showing the area"

# stdin
echo "A right triangle with legs 3 and 4, showing the area" | python triangle-llm.py

# file
python triangle-llm.py --file description.txt
```

The output format is chosen with `--format`: `svg` (default), `xml`, `equations`, or `json`. With JSON, you get the full CoreGX response, including all formats. It's written to stdout by default. To write to a file instead use `-o`/`--output` with the desired filename:

```bash
# stdout
python triangle-llm.py --file description.txt --format svg > output.svg

# file output
python triangle-llm.py --file description.txt --format xml -o result.xml
python triangle-llm.py --file description.txt --format json --output result.json
```

By default the script only prints the requested output (or writes it to `-o`), which keeps output pipeable. Pass `-v`/`--verbose` to see more details about the process.

```bash
python triangle-llm.py --file description.txt -o output.svg -v
```

If CoreGX rejects the program, it's retried with the error fed back to the LLM, up to `--max-tries` times (default: 1):

```bash
python triangle-llm.py --file description.txt --max-tries 5
```
