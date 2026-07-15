# Example

A CoreGX program is read from `example.coregx` and a standalone HTML web app is written to `output.html`.

```bash
export COREGX_API_KEY=your-api-key

./cgx-webapp.sh
```

This usage may require `chmod +x *.sh` to make the shell scripts executable.

## Pipeline

By default:

```
example.coregx
      │
      ▼
cgx-webapp.py
      │
      ▼
output.html
```

Alternatively:

```
example.coregx
      │
      ▼
cgx-json.py
      │
      ▼
output.json
      │
      ▼
json-webapp.py
      │
      ▼
output.html
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./cgx-webapp.sh
```

If you prefer not to use a Bash-compatible shell, see the corresponding Python example for PowerShell and Command Prompt usage.