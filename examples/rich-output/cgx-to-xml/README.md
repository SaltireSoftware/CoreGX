# Example

A CoreGX program is read from `example.coregx` and XML is written to `output.xml`.

```bash
export COREGX_API_KEY=your-api-key

./cgx-xml.sh
```

This usage may require `chmod +x *.sh` to make the shell scripts executable.

## Pipeline

By default:

```
example.coregx
      │
      ▼
cgx-xml.py
      │
      ▼
output.xml
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
json-xml.py
      │
      ▼
output.xml
```

## Windows

These examples are Bash shell scripts. You can run them using Git Bash, WSL, or another POSIX-compatible shell on Windows.

```bash
export COREGX_API_KEY=your-api-key

./cgx-xml.sh
```

If you prefer not to use a Bash-compatible shell, see the corresponding Python example for PowerShell and Command Prompt usage.