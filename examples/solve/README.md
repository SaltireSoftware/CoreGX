# Minimal Working Example

A CoreGX program goes in on stdin, SymPy is used to solve, and TEX comes out on stdout. 

```bash
export COREGX_API_KEY=your-api-key

# Python 3
./solve.py  < example.coregx > output.tex

```

This usage may require `chmod +x minimal.*` to make the files executable. You can always pass the file directly to the interpreter as well, e.g. `python3 solve.py`.

## Windows

Windows doesn't honor the shebang lines or the executable bit, so you need to invoke the interpreter directly instead of running the script. For example, if you want to run with Python:

### PowerShell

```powershell
$env:COREGX_API_KEY = your-api-key
Get-Content example.coregx | python3 solve.py | Set-Content output.tex
```

### Command Prompt (cmd.exe)

```bat
set COREGX_API_KEY=your-api-key
python3 solve.py < example.coregx > output.tex
```
