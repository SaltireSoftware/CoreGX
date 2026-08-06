# CoreGX Symbolic Limit Pipeline Example

A workflow example showing a complete pipeline where a CoreGX program is read from `example.coregx`, geometric equations are extracted through the CoreGX API, and a symbolic limit is computed using SymPy. The answer is written as a sentence in TeX format to the `output` directory.

```
[CoreGX program] ── CoreGX API ─➤ [equations] ── SymPy ─➤ [TeX sentence]
```

## Setup

Set your CoreGX API key:

```bash
export COREGX_API_KEY=your-api-key
```

The shell script optionally installs Python dependencies. Python dependencies are listed in `requirements.txt`.

Install with:

```bash
pip install -r scripts/requirements.txt
```

The requirements include the SymPy dependency used for symbolic computation.

The shell script also suppresses Python `SyntaxWarning` messages during execution.

## Run

```bash
./limit.sh
```

This usage may require:

```bash
chmod +x *.sh
```

to make the shell scripts executable.

The pipeline automatically:

1. Extracts equations from the CoreGX program.
2. Computes the symbolic limit using SymPy.
3. Writes intermediate and final outputs into the `outputs` directory.

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
scripts/limit.py
      │
      ▼
outputs/output.tex
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./limit.sh
```

If you prefer not to use a Bash-compatible shell, run the individual Python scripts directly from PowerShell or Command Prompt.
