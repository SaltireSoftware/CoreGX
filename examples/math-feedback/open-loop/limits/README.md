# Example

A CoreGX program is read from `example.coregx`, the equations are extracted, and the symbolic limit is computed with SymPy. The resulting limit is written to `output.tex`.

```bash
export COREGX_API_KEY=your-api-key

./cgx-limit.sh
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
equations-limit.py
      │
      ▼
output.tex
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./cgx-limit.sh
```

If you prefer not to use a Bash-compatible shell, see the corresponding Python examples for PowerShell and Command Prompt usage.