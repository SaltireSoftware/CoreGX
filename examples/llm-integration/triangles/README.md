# Small Prompt Triangle Pipeline Example

A workflow example showing a complete pipeline using a natural language triangle description, an LLM, and the CoreGX API to turn a prompt into a CoreGX program and SVG diagram.

The provided prompt can be edited in `scripts/system-prompt.txt`.


```
[natural language] ── LLM ─➤ [CoreGX program] ── CoreGX API ─➤ [SVG]
```

## Model and prompt design

The example outputs included in this folder were produced with [`Qwen/Qwen2.5-14B-Instruct-1M`](https://huggingface.co/Qwen/Qwen2.5-14B-Instruct-1M). This model is not required: the pipeline can work with other instruction-following models of different sizes, including smaller models that can be run locally. Results may vary with the selected model, quantization, context-window size, and inference settings.

The prompt in `scripts/system-prompt.txt` is intentionally constrained to one specific task: translating natural-language triangle descriptions into a small, predictable set of CoreGX commands. It defines the supported commands, mapping rules, and output format while excluding explanations and unrelated output. This narrow scope keeps the prompt and expected response compact, making the example suitable for limited-context LLMs and local model servers while still giving the model enough guidance to construct triangles and apply side-length constraints in CoreGX.

## Setup

Works with any OpenAI-compatible chat completions API. Pass your API key, model name, and optionally a base URL via environment variables. If no base URL is provided, the default OpenAI API is used.

```bash
export LLM_API_KEY=your-llm-api-key
export LLM_BASE_URL=https://your-url
export LLM_MODEL=your-model-name

export COREGX_API_KEY=your-coregx-api-key
```

Python dependencies are listed in `requirements.txt`.

Install with:

```bash
pip install -r scripts/requirements.txt
```

The requirements file contains the dependencies needed for LLM integration.

## Run

The shell script accepts either a description file or a description passed directly on the command line.

### Using a description file

Place your prompt in `description.txt` and run:

```bash
./triangles.sh description.txt
```

### Using a command-line description

```bash
./triangles.sh "Draw triangle ABC with AB = 3, BC = 4, AC = 5."
```

The pipeline automatically:

1. Generates a CoreGX program using the LLM.
2. Saves the generated CoreGX program to `outputs/program.coregx`.
3. Sends the CoreGX program to the CoreGX API.
4. Writes the resulting SVG to `output/output.svg`.

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
bash .\triangles.sh description.txt

# Or provide the description directly
bash .\triangles.sh "Draw triangle ABC with AB = 3, BC = 4, AC = 5."
```

### Command Prompt (cmd.exe)

```bat
set LLM_API_KEY=your-llm-api-key
set LLM_BASE_URL=https://your-url
set LLM_MODEL=your-model-name

set COREGX_API_KEY=your-coregx-api-key

REM Using description.txt
bash triangles.sh description.txt

REM Or provide the description directly
bash triangles.sh "Draw triangle ABC with AB = 3, BC = 4, AC = 5."
```
