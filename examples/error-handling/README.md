# CoreGX Overconstraint Repair Example

A CoreGX program is read from `example.coregx`, executed through CoreGX, and checked for overconstraint errors. If an overconstraint is detected, the conflicting constraint line is removed from the original CoreGX program. The repaired program is then rendered to SVG.

~~~
bash
export COREGX_API_KEY=your-api-key

./repair_pipeline.sh
~~~

This usage may require `chmod +x *.sh` to make the shell scripts executable.

## Pipeline

~~~
example.coregx
      │
      ▼
cgx-json.py
      │
      ▼
coregx.json
      │
      ▼
error-remover.py
      │
      ▼
fixed.coregx
      │
      ▼
cgx-svg.py
      │
      ▼
output.svg
~~~

## Windows

This example uses a Bash shell script. You can run it using Git Bash, WSL, or another POSIX-compatible shell on Windows.

~~~bash
export COREGX_API_KEY=your-api-key

./repair_pipeline.sh
~~~

If you prefer not to use a Bash-compatible shell, run the individual Python scripts directly from PowerShell or Command Prompt.