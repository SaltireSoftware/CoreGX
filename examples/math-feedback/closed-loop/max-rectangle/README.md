# CoreGX Maximize Rectangle Area Pipeline Example

A CoreGX program is read from `example.coregx`, the equations are extracted, and critical points are computed using SymPy. The resulting solution is substituted back into the CoreGX program as a `value` statement, and the solved program is rendered as an SVG.

## Setup

The shell script installs Python dependencies automatically from:

```
scripts/requirements.txt
```

The requirements include the SymPy dependency used for symbolic computation.

Set your CoreGX API key:

```bash
export COREGX_API_KEY=your-api-key
```

Make the shell script executable if needed:

```bash
chmod +x *.sh
```

## Run

Run the pipeline:

```bash
./cgx-maximize-area.sh
```

The pipeline automatically:

1. Installs Python dependencies.
2. Suppresses Python `SyntaxWarning` messages.
3. Extracts equations from the CoreGX program.
4. Computes critical points using SymPy.
5. Substitutes the resulting value into the CoreGX program.
6. Generates an SVG visualization.

The intermediate files are preserved in the `output` directory:

The intermediate outputs allow each stage of the pipeline to be inspected independently.

## Pipeline

```
example.coregx
      │
      ▼
cgx-equations.py
      │
      ▼
equations.json
      │
      ▼
equations-critical_points.py
      │
      ▼
critical.json
      │
      ▼
solved-substitute.py
      │
      ▼
fixed.coregx
      │
      ▼
cgx-svg.py
      │
      ▼
output.svg
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./cgx-maximize-area.sh
```

If you prefer not to use a Bash-compatible shell, run the Python scripts directly from PowerShell or Command Prompt using the same pipeline order.