# CoreGX Overconstraint Repair Example

A CoreGX program is read from `example.coregx`, executed through CoreGX, and checked for overconstraint errors. If an overconstraint is detected, the conflicting constraint line is removed from the original CoreGX program. The repaired program is then rendered to SVG.

The pipeline optionally installs Python dependencies from `requirements.txt` before running. The main dependency is SymPy, which is used by the Python scripts when symbolic processing is required.

```bash
export COREGX_API_KEY=your-api-key

./repair_pipeline.sh
```

This usage may require `chmod +x *.sh` to make the shell scripts executable.


## Pipeline

```
example.coregx
      │
      ▼
scripts/cgx-json.py
      │
      ▼
outputs/coregx.json
      │
      ▼
scripts/error-remover.py
      │
      ▼
outputs/fixed.coregx
      │
      ▼
scripts/cgx-svg.py
      │
      ▼
outputs/output.svg
```

## Description

The pipeline:

1. Reads the CoreGX source program from `example.coregx`.
2. Sends the program to CoreGX and saves the returned JSON response.
3. Detects overconstraint errors and identifies the offending source lines.
4. Removes the conflicting constraints from the original CoreGX program.
5. Writes the repaired CoreGX program to `outputs/fixed.coregx`.
6. Generates an SVG visualization from the repaired program.

## Dependencies

Python dependencies are listed in `requirements.txt`.

Install with:

```bash
pip install -r requirements.txt
```

## Windows

This example uses a Bash shell script. You can run it using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./repair_pipeline.sh
```

If you prefer not to use a Bash-compatible shell, run the individual Python scripts directly from PowerShell or Command Prompt after installing the requirements.
```