# CoreGX SVG Pipeline Example

A workflow example showing a complete pipeline where a CoreGX program with an animation is read from `example.coregx` and converted into an animated SVG. The generated SVG is written to the `output` directory.

```
[CoreGX program] ── CoreGX API ─➤ [animated SVG]
```

## Setup

Set your CoreGX API key:

```bash
export COREGX_API_KEY=your-api-key
```

The shell script also suppresses Python `SyntaxWarning` messages during execution.

## Run

```bash
./get-svg.sh
```

This usage may require:

```bash
chmod +x *.sh
```

to make the shell scripts executable.

The pipeline automatically:

1. Reads the CoreGX program.
2. Converts the program into an animated SVG.
3. Writes the generated SVG into the `outputs` directory.

## Pipeline

By default:

```
example.coregx
      │
      ▼
scripts/cgx-svg.py
      │
      ▼
output/output.svg
```

Alternatively, uncomment the JSON pipeline inside the shell script:

```
example.coregx
      │
      ▼
scripts/cgx-json.py
      │
      ▼
output/output.json
      │
      ▼
scripts/json-svg.py
      │
      ▼
output/output.svg
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./get-svg.sh
```

If you prefer not to use a Bash-compatible shell, run the individual Python scripts directly from PowerShell or Command Prompt.
