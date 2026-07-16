# Closed Loop Math Example

A CoreGX program is read from `example.coregx`, the equations are extracted, critical points are computed with SymPy, and the optimal value is substituted back into the original CoreGX program. The final solved geometry is rendered as SVG.

```bash
export COREGX_API_KEY=your-api-key

./solve-substitute.sh
```

This usage may require `chmod +x *.sh` to make the shell scripts executable.

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

## Generated Files

- `equations.json` — symbolic equations extracted from CoreGX.
- `critical.json` — critical points and corresponding function values computed by SymPy.
- `fixed.coregx` — CoreGX program with the optimized value substituted.
- `output.svg` — rendered SVG output.

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./solve-substitute.sh
```

If you prefer not to use a Bash-compatible shell, run the individual Python scripts directly from PowerShell or Command Prompt.