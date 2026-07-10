# Animated SVG

A CoreGX program with an animation goes in on stdin, animated SVG comes out on stdout. `.

```bash
export COREGX_API_KEY=your-api-key

# Python 3
./animatedsvg.py  < example.coregx > output.svg
```

This usage may require `chmod +x minimal.*` to make the files executable. You can always pass the file directly to the interpreter as well, e.g. `python3 animatedsvg.py`.

## Windows

Windows doesn't honor the shebang lines or the executable bit, so you need to invoke the interpreter directly instead of running the script. For example, if you want to run with Python:

### PowerShell

```powershell
$env:COREGX_API_KEY = your-api-key
Get-Content example.coregx | python3 animatedsvg.py | Set-Content output.svg
```

### Command Prompt (cmd.exe)

```bat
set COREGX_API_KEY=your-api-key
python3 animatedsvg.py < example.coregx > output.svg
```
