# Example

A CoreGX program is read from `example.coregx`, the equations are extracted, solved symbolically with SymPy, and the solution is substituted back into the original expression. The final result is written as TeX to `output.tex`.

```bash
export COREGX_API_KEY=your-api-key

./solve_substitute.sh
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
equations-solve.py
      │
      ▼
solutions.json
      │
      ▼
solved-substitute.py
      │
      ▼
output.tex
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./solve_substitute.sh
```

If you prefer not to use a Bash-compatible shell, run the individual Python scripts directly from PowerShell or Command Prompt.