# Simple Web Demo

A small, static HTML/JS page that takes a CoreGX program and renders the diagram and any measurements. It calls `https://api.coregx.dev/run-coregx` directly from the browser.

Open `index.html` in a browser, then paste your CoreGX API key into the field at the top. The key is stored in `localStorage` so you don't have to re-enter it each time.

After submitting a program, the diagram will show the returned SVG and measurements will be shown below, rendered with KaTeX.
