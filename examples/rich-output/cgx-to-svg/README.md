# Example

A CoreGX program is read from `example.coregx` and an SVG drawing is written to `output.svg`. The CoreGX program in this folder illustrates a locus. 

```bash
export COREGX_API_KEY=your-api-key

./cgx-svg.sh
```

This usage may require `chmod +x *.sh` to make the shell scripts executable.

## Pipeline

By default:

```
example.coregx
      │
      ▼
cgx-svg.py
      │
      ▼
output.svg
```

Alternatively, uncomment the JSON pipeline inside the shell script:

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
json-svg.py
      │
      ▼
output.svg
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./cgx-svg.sh
```

If you prefer not to use a Bash-compatible shell, see the corresponding Python example for PowerShell and Command Prompt usage.