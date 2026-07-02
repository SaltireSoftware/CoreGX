#!/usr/bin/env -S deno run --allow-net --allow-env
// Minimal working example: CoreGX source to SVG.
//
// Usage:
//   COREGX_API_KEY=your-key ./minimal.ts < example.coregx > output.svg

const program = await new Response(Deno.stdin.readable).text();

const response = await fetch("https://api.coregx.dev/run-coregx", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ apikey: Deno.env.get("COREGX_API_KEY"), program, svg: true }),
});
const result = await response.json();

if (!result.ok) {
  console.error(`CoreGX error: ${result.error}`);
  Deno.exit(1);
}

console.log(result.value.svg);
