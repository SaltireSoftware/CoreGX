# Closed Loop Math Example: Triangle Area

A CoreGX program goes in through `example.coregx`. The pipeline extracts equations from CoreGX, uses SymPy to solve for critical points, substitutes the solution back into the CoreGX program, and produces the final SVG output.

```bash
export COREGX_API_KEY=your-api-key

# Bash
./critical_pipeline.sh
```

This usage may require `chmod +x critical_pipeline.sh` to make the script executable. You can also run the individual Python scripts directly if you prefer not to use the shell pipeline.

## Windows

Windows does not honor shebang lines or executable bits, so use a Bash environment such as Git Bash, WSL, or another compatible shell.

```bash
export COREGX_API_KEY=your-api-key

./critical_pipeline.sh
```

If you do not want to use Bash, run the Python scripts individually with Python instead.

The pipeline generates:

* `equations.json` — equations extracted from CoreGX.
* `critical.json` — critical points and optimized values computed by SymPy.
* `fixed.coregx` — CoreGX program with the solution substituted.
* `output.svg` — final rendered output.
