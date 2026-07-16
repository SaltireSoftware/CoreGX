# Small Prompt Four-Bar Linkage Pipeline Example

A workflow example showing a complete pipeline using a small constrained prompt about four-bar linkages, an LLM, and the CoreGX API to turn a natural language description into a diagram.

```
[natural language] ── LLM ─➤ [CoreGX program] ── CoreGX API ─➤ [SVG]
```

## Setup

Works with any OpenAI-compatible chat completions API. Pass your API key, model name, and optionally a base URL via environment variables. If no base URL is provided, the default OpenAI API is used.

```bash
export LLM_API_KEY=your-llm-api-key
export LLM_BASE_URL=https://your-url
export LLM_MODEL=your-model-name

export COREGX_API_KEY=your-coregx-api-key
```

Python dependencies are installed automatically by the shell script from:

```
scripts/requirements.txt
```

The requirements file contains the dependencies needed for LLM integration.

## Run

The shell script accepts either a description file or a description passed directly on the command line.

### Using a description file

Place your prompt in `description.txt` and run:

```bash
./nl-svg-fourbar.sh description.txt
```

### Using a command-line description

```bash
./nl-svg-fourbar.sh "Give me a crank-rocker four-bar linkage with crank AB length 1, rocker DC length 3, base AD length 3.5, connector BC length 3.7. Show the coupler curve of a point 3.2 to the right of A and 1.2 below BC."
```

The pipeline automatically:

1. Installs Python dependencies from `scripts/requirements.txt`.
2. Generates a CoreGX program using the LLM.
3. Saves the generated program to `outputs/program.coregx`.
4. Sends the program to the CoreGX API.
5. Writes the resulting SVG to `outputs/output.svg`.

The intermediate CoreGX program is preserved in the output folder, making it easy to inspect or edit before rendering.

## Windows

Run the shell script using Git Bash.

### PowerShell

```powershell
$env:LLM_API_KEY = "your-llm-api-key"
$env:LLM_BASE_URL = "https://your-url"
$env:LLM_MODEL = "your-model-name"

$env:COREGX_API_KEY = "your-coregx-api-key"

# Using description.txt
bash .\nl-svg-fourbar.sh description.txt

# Or provide the description directly
bash .\nl-svg-fourbar.sh "Give me a crank-rocker four-bar linkage with crank AB length 1, rocker DC length 3, base AD length 3.5, connector BC length 3.7. Show the coupler curve of a point 3.2 to the right of A and 1.2 below BC."
```

### Command Prompt (cmd.exe)

```bat
set LLM_API_KEY=your-llm-api-key
set LLM_BASE_URL=https://your-url
set LLM_MODEL=your-model-name

set COREGX_API_KEY=your-coregx-api-key

REM Using description.txt
bash nl-svg-fourbar.sh description.txt

REM Or provide the description directly
bash nl-svg-fourbar.sh "Give me a crank-rocker four-bar linkage with crank AB length 1, rocker DC length 3, base AD length 3.5, connector BC length 3.7. Show the coupler curve of a point 3.2 to the right of A and 1.2 below BC."
```