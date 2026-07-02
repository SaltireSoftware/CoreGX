# Minimal Working Example

The smallest possible CoreGX pipeline: a CoreGX program goes in on stdin, SVG comes out on stdout. The Python, Node, and Deno versions are dependency-free beyond what's built into the language runtime. The bash version uses `curl` and `jq`.

```bash
export COREGX_API_KEY=your-api-key

# Python 3
./minimal.py  < example.coregx > output.svg

# Bash
./minimal.sh  < example.coregx > output.svg

# Node
./minimal.js  < example.coregx > output.svg

# Deno
./minimal.ts  < example.coregx > output.svg
```

`minimal.ts` needs network and environment-variable access (`--allow-net --allow-env`), granted via its shebang — if you invoke it as `deno run minimal.ts` instead, pass those flags explicitly.

Run one of those commands, then open `output.svg` in a browser or image viewer.
