# CoreGX Critical Points Pipeline Example

A workflow example showing a complete pipeline where a CoreGX program is read from `example.coregx`, equations are extracted through the CoreGX API, and the critical points of the resulting expression are calculated using SymPy. The critical points and their corresponding values are written to the `outputs` directory.

```
[CoreGX program] ── CoreGX API ─➤ [equations] ── SymPy ─➤ [critical points]
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

## Run

```bash
./cgx-critical_points.sh
```

This usage may require:

```bash
chmod +x *.sh
```

to make the shell scripts executable.

The pipeline automatically:

1. Installs Python dependencies from `scripts/requirements.txt`.
2. Extracts equations from the CoreGX program.
3. Computes critical points using SymPy.
4. Writes intermediate and final outputs into the `output` directory.

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
scripts/equations-critical_points.py
      │
      ▼
outputs/output.json
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./cgx-critical_points.sh
```

If you prefer not to use a Bash-compatible shell, run the individual Python scripts directly from PowerShell or Command Prompt.