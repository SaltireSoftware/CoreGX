#!/usr/bin/env node
// Minimal working example: CoreGX source to SVG.
//
// Usage:
//   COREGX_API_KEY=your-key node minimal.mjs < program.coregx > output.svg

const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const program = Buffer.concat(chunks).toString("utf8");

const response = await fetch("https://api.coregx.dev/dev/api/run-coregx", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ apikey: process.env.COREGX_API_KEY, program, svg: true }),
});
const result = await response.json();

if (!result.ok) {
  console.error(`CoreGX error: ${result.error}`);
  process.exit(1);
}

console.log(result.value.svg);
