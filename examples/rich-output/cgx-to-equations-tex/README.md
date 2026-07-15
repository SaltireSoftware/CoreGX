# Example

A CoreGX program with a measurement is read from `example.coregx` and equations TeX is written to `output.tex`.

```bash
export COREGX_API_KEY=your-api-key

./cgx-tex.sh
```

This usage may require `chmod +x *.sh` to make the shell scripts executable.

## Pipeline

```
example.coregx
      │
      ▼
cgx-tex.py
      │
      ▼
output.tex
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./cgx-tex.sh
```

If you prefer not to use a Bash-compatible shell, see the corresponding Python example for PowerShell and Command Prompt usage.