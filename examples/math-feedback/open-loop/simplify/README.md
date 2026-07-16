# CoreGX Simplification Pipeline Example

A workflow example showing a complete pipeline where a CoreGX program is read from `example.coregx`, equations are extracted through the CoreGX API, and the resulting expression is simplified using SymPy. The simplified expression is written as TeX to the `outputs` directory.

```
[CoreGX program] ── CoreGX API ─➤ [equations] ── SymPy ─➤ [simplified TeX]
```

## Setup

Set your CoreGX API key:

```bash
export COREGX_API_KEY=your-api-key
```

Python dependencies are installed automatically by the shell script from:

```
scripts/requirements.txt
```

The shell script also suppresses Python `SyntaxWarning` messages during execution.

## Run

```bash
./cgx-simplify.sh
```

This usage may require:

```bash
chmod +x *.sh
```

to make the shell scripts executable.

The pipeline automatically:

1. Installs Python dependencies from `scripts/requirements.txt`.
2. Extracts equations from the CoreGX program.
3. Simplifies the expression using SymPy.
4. Writes intermediate and final outputs into the `outputs` directory.

## Pipeline

```
example.coregx
      │
      ▼
scripts/cgx-equations.py
      │
      ▼
outputs/equations.json
      │
      ▼
scripts/equations-simplify.py
      │
      ▼
outputs/output.tex
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./cgx-simplify.sh
```

If you prefer not to use a Bash-compatible shell, run the individual Python scripts directly from PowerShell or Command Prompt.