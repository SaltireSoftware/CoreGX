# Minimal Working Example: XML

A CoreGX program goes in on stdin, XML comes out on stdout. Every version is dependency-free beyond what's built into the language runtime, except the bash version, which uses `curl` and `jq`.

```bash
export COREGX_API_KEY=your-api-key

# Python 3
./minimalxml.py  < example.coregx > output.xml

```

This usage may require `chmod +x minimal.*` to make the files executable. You can always pass the file directly to the interpreter as well, e.g. `python3 minimalxml.py`.

## Windows

Windows doesn't honor the shebang lines or the executable bit, so you need to invoke the interpreter directly instead of running the script. For example, if you want to run with Python:

### PowerShell

```powershell
$env:COREGX_API_KEY = your-api-key
Get-Content example.coregx | python3 minimalxml.py | Set-Content output.xml
```

### Command Prompt (cmd.exe)

```bat
set COREGX_API_KEY=your-api-key
python3 minimalxml.py < example.coregx > output.xml
```
