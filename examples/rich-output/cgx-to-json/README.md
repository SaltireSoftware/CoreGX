# Example

A CoreGX program is read from `example.coregx` and the full CoreGX JSON response is written to `output.json`.

```bash
export COREGX_API_KEY=your-api-key

./cgx-json.sh
```

This usage may require `chmod +x *.sh` to make the shell scripts executable.

## Pipeline

```
example.coregx
      │
      ▼
cgx-json.py
      │
      ▼
output.json
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./cgx-json.sh
```
If you prefer not to use a Bash-compatible shell, see the corresponding Python example for PowerShell and Command Prompt usage.