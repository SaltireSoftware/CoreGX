# Example

A CoreGX program is read from `example.coregx`, the equations are extracted, and the critical points of the resulting expression are calculated using SymPy. The critical points and their corresponding values are written to `output.json`.

```bash
export COREGX_API_KEY=your-api-key

./cgx-critical_points.sh
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
output.json
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./cgx-critical_points.sh
```

If you prefer not to use a Bash-compatible shell, see the corresponding Python examples for PowerShell and Command Prompt usage.