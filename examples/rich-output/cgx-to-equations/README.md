# CoreGX Equations Pipeline Example

A workflow example showing a complete pipeline where a CoreGX program is read from `example.coregx` and converted into equations JSON through the CoreGX API. The resulting equations JSON is written to the `output` directory.

```
[CoreGX program] ── CoreGX API ─➤ [equations JSON]
```

## Setup

Set your CoreGX API key:

```bash
export COREGX_API_KEY=your-api-key
```

The shell script also suppresses Python `SyntaxWarning` messages during execution.

## Run

```bash
./cgx-equations.sh
```

This usage may require:

```bash
chmod +x *.sh
```

to make the shell scripts executable.

The pipeline automatically:

1. Reads the CoreGX program.
2. Extracts the geometric equations through the CoreGX API.
3. Writes the equations JSON into the `output` directory.

## Pipeline

By default:

```
example.coregx
      │
      ▼
scripts/cgx-equations.py
      │
      ▼
output/output.json
```

Alternatively, uncomment the JSON pipeline inside the shell script:

```
example.coregx
      │
      ▼
scripts/cgx-json.py
      │
      ▼
output/output-full.json
      │
      ▼
scripts/json-equations.py
      │
      ▼
output/output.json
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./cgx-equations.sh
```

If you prefer not to use a Bash-compatible shell, run the individual Python scripts directly from PowerShell or Command Prompt.