# Example

A CoreGX program is read from `example.coregx`, the equations are extracted, and the resulting expression is simplified using SymPy. The simplified expression is written as TeX to `output.tex`.

```bash
export COREGX_API_KEY=your-api-key

./cgx-simplify.sh
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
equations-simplify.py
      │
      ▼
output.tex
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./cgx-simplify.sh
```

If you prefer not to use a Bash-compatible shell, see the corresponding Python examples for PowerShell and Command Prompt usage.