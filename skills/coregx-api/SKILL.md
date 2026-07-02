---
name: coregx-api
description: >-
  Generate geometry diagrams with the CoreGX geometry constraint solver. Use
  when the user describes a geometric figure, theorem, or construction in
  natural language and wants a diagram, SVG, XML, or symbolic equations — or
  when given a CoreGX program to run. Covers translating a natural-language
  geometry problem into a CoreGX program (without overconstraining) and calling
  the CoreGX HTTP API to render SVG / XML / equation output.
---

# CoreGX API

CoreGX is a geometry constraint solver. You describe geometry as a list of
**constructions and constraints** (a "CoreGX program"), and the solver finds a
configuration satisfying them and renders it as an SVG diagram, an XML scene
description, and/or symbolic equation results.

This skill covers two tasks:

1. **Authoring** — turning a natural-language geometry description into a CoreGX
   program.
2. **Running** — sending a CoreGX program to the CoreGX HTTP API to get back
   SVG / XML / equations.

A typical end-to-end request: the user describes a figure → you write a CoreGX
program (Task 1) → you POST it to `/run-coregx` (Task 2) → you return the SVG /
equations.

---

## Task 1 — Author a CoreGX program from natural language

You are a diagram generator. Given a natural-language geometry input (a problem
statement, theorem, or description), output **only** CoreGX commands, one per
line — no prose, no explanations, no numbered lists, no code fences in the
program itself.

If the input is a theorem or problem statement, first reason through:
1. What objects does this actually involve (not just what it names)?
2. What helper constructions/constraints are needed that it doesn't mention?
3. What is the minimal diagram that makes the result visible?
4. What would be overconstrained if added naively?

### The golden rule: do not overconstrain

CoreGX is a hybrid solver, **not** an algebraic constraint solver. Every
"construction" command is shorthand for a geometric relation, and the solver
synthesizes a construction sequence that satisfies the constraints in order.

> **Specify the minimum number of constraints to pin down the figure. CoreGX
> handles underconstrained figures fine, but FAILS on overconstrained ones
> (`unresolvable-constraints`). Never use redundant constraints.**

Count degrees of freedom per primitive and stop when consumed:
- `point` — 2 DOF
- `line` — 2 DOF
- `circle` — 3 DOF

Shared endpoints reduce the available DOF on connected primitives. Constraining
something to a **variable** (e.g. `angle B A C t`) still counts as a full
constraint — a variable is just a placeholder numeric value, so it is *not* safe
to overconstrain with variables either. A triangle accepts at most **two** angle
constraints; if a problem implies three, do the arithmetic yourself and emit two.

### Core conventions (follow strictly)

- Output only CoreGX commands. No English, commentary, or markdown.
- **Do not use explicit coordinates** (the `coordinates` command) unless the user
  explicitly asks, or the geometry is inherently parametric (e.g. tracing a
  curve). Always look for a non-coordinate, constraint-based formulation first.
- Avoid transformations unless they are the natural tool (e.g. rotational
  symmetry of a regular polygon).
- Use named objects from the input as names when given ("Let I be the
  incircle"). Otherwise use canonical single letters (A, B, C, O, U, V…); if
  exhausted, use X1, X2, …
- Circles must be named `C0`, `C1`, `C2`, … in order of creation (skipping names
  already taken by points). When the user names a circle, name its center point
  after the requested name where possible.
- Multiplication must be explicit in expressions: `"2*x"`, never `"2x"`.
- When the user asks to *find* a specific object, highlight it with `color=red`
  (or a user-specified color).
- Hide helper constructions/points that shouldn't appear in the final diagram
  with `visible=false`.

For the full set of conventions, command-specific guidance (incircle/excircle
ordering, `intersection other=`, `pointonsegment` vs `incident`, building
equilateral triangles with `oppositeside`, reflections/symmedians, envelopes,
etc.) and a library of worked input→output examples, **read
`reference/authoring-guide.md`**.

For the complete command/syntax reference (every command, its arguments,
options, and naming rules), **read `reference/syntax.md`**. You can also fetch
the live syntax guide at runtime — see Task 2.

### Minimal example

Input: *"In a parallelogram ABCD, the diagonals bisect each other."*

```
polygon A B C D
parallel AB CD
parallel BC AD
segment A C
segment B D
intersection O AC BD
midpoint P A C
midpoint Q B D
displayproperties O P Q color=red
```

---

## Task 2 — Run a CoreGX program via the API

Base URL: `https://api.coregx.dev/`

All endpoints return a JSON envelope. Always branch on `ok`:

```json
{ "ok": true,  "value": { ... } }
{ "ok": false, "error": "<error code>" }
```

Application outcomes (success *and* program errors) come back with HTTP 200 —
inspect `ok`, not the status code. Only routing problems use 404/405.

### `POST /run-coregx`

Runs a program and returns the requested output. Request body:

| Field | Type | Required | Notes |
|---|---|---|---|
| `program` | string | yes | The CoreGX program (newline-separated commands). |
| `apikey` | string | yes* | 64-char CoreGX API key. Consumes one CoreGX credit per call. |
| `seed` | number | no | Random seed; random if omitted. |
| `disableOptimization` | boolean | no | `true` skips point-location optimization — significantly faster. Default `false`. |
| `all` | boolean | no | `true` returns every output type and overrides the flags below. |
| `svg` | boolean | no | Include SVG output. |
| `xml` | boolean | no | Include XML output. |
| `equations` | boolean | no | Include symbolic equation results. |

\*Requests must carry a valid `apikey`. Ask the user for theirs if you don't
have one; never invent a key.

Request at least one output flag (or `all`) for the output you actually need.
Success response:

```json
{
  "ok": true,
  "value": {
    "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\">...</svg>",
    "xml": "<...>",
    "equations": [
      {
        "expression": "distance(A,C)",
        "expressionTex": "distance(A,C)",
        "valueTex": "5",
        "valueRealAsTex": "5"
      }
    ]
  }
}
```

Only the requested fields are present. To get measurement output, include a
`measure …` command in the program *and* request `equations`.

Each entry in `equations` is an object, not a plain string: `expression` is
the measured quantity as written in the `measure …` command, and `valueTex`
is its solved value (`expressionTex` and `valueRealAsTex` are TeX-formatted
variants for typeset display). Build a plain-text line yourself, e.g.
`${eq.expression} = ${eq.valueTex}`.

Example request:

```bash
curl -s https://api.coregx.dev/run-coregx \
  -H 'Content-Type: application/json' \
  -d '{
        "apikey": "<API_KEY>",
        "svg": true,
        "program": "triangle A B C\nmidpoint M B C\nsegment A M"
      }'
```

### `GET /get-syntax`

Returns the CoreGX syntax guide as a Markdown string. No auth, no parameters.
Use this to fetch the authoritative, up-to-date command reference at runtime if
you are unsure about a command or option (the bundled `reference/syntax.md` is a
snapshot of the same document).

```json
{ "ok": true, "value": "# Geometry Command Reference\n..." }
```

### Handling errors

On `ok: false`, the `error` string identifies the cause. Common codes:

- `invalid-request-format` — body malformed or `program` missing.
- `invalid-gengx-api-key` — key not found.
- `not-enough-gengx-credits` — key out of CoreGX credits.
- `concurrent-rate-limit` / `ip-rate-limit` — back off and retry.
- `unresolvable-constraints` — **overconstrained** (or contradictory). Re-read
  the golden rule, remove redundant constraints, and try again.
- `process-timed-out` — program too expensive; try `disableOptimization: true`.
- Any other string — a CoreGX error from a malformed command (e.g.
  `triangle requires 3 arguments`). Fix the program and retry.

See `reference/api.md` for the full endpoint and error reference.
