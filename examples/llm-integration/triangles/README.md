# Small Prompt Triangle Pipeline Example

A workflow example showing a complete pipeline using a natural language triangle description, an LLM, and the CoreGX API to turn a prompt into a CoreGX program and SVG diagram.

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

Python dependencies are listed in `requirements.txt`.

The shell script automatically installs dependencies before running:

```bash
pip install -r requirements.txt
```

The requirements include the OpenAI Python package needed for LLM integration.

## Folder Structure

```
nl-svg-triangle.sh
requirements.txt
scripts/
    nl-cgx-triangle.py
    cgx-svg.py
outputs/
    program.coregx
    output.svg
```

## Run

The shell script accepts either a description file or a description passed directly on the command line.

### Using a description file

Place your prompt in `description.txt` and run:

```bash
./nl-svg-triangle.sh description.txt
```

### Using a command-line description

```bash
./nl-svg-triangle.sh "Draw triangle ABC with AB = 3, BC = 4, AC = 5."
```

The pipeline automatically:

1. Installs Python dependencies from `requirements.txt`.
2. Suppresses Python syntax warnings during execution.
3. Generates a CoreGX program using the LLM.
4. Saves the generated CoreGX program to `outputs/program.coregx`.
5. Sends the CoreGX program to the CoreGX API.
6. Writes the resulting SVG to `outputs/output.svg`.

The intermediate CoreGX program is preserved in the output folder, making it easy to inspect or edit before rendering.

## Windows

Run the shell script using Git Bash, WSL, or another Bash-compatible environment.

### PowerShell

```powershell
$env:LLM_API_KEY = "your-llm-api-key"
$env:LLM_BASE_URL = "https://your-url"
$env:LLM_MODEL = "your-model-name"

$env:COREGX_API_KEY = "your-coregx-api-key"

# Using description.txt
bash .\nl-svg-triangle.sh description.txt

# Or provide the description directly
bash .\nl-svg-triangle.sh "Draw triangle ABC with AB = 3, BC = 4, AC = 5."
```

### Command Prompt (cmd.exe)

```bat
set LLM_API_KEY=your-llm-api-key
set LLM_BASE_URL=https://your-url
set LLM_MODEL=your-model-name

set COREGX_API_KEY=your-coregx-api-key

REM Using description.txt
bash nl-svg-triangle.sh description.txt

REM Or provide the description directly
bash nl-svg-triangle.sh "Draw triangle ABC with AB = 3, BC = 4, AC = 5."
```