# CoreGX API Reference

Public endpoints for running CoreGX programs and fetching the syntax guide.

- **Base URL:** `https://api.coregx.dev/`
- **Method/body:** endpoints take `POST` with a JSON body unless noted.
- **Envelope:** every response is one of:
  ```json
  { "ok": true,  "value": { ... } }
  { "ok": false, "error": "<error code>" }
  ```
- **Status codes:** application outcomes — both success and program/validation
  errors — return HTTP 200. Branch on the `ok` field, not the HTTP status. Only
  request-routing problems use 404 (endpoint/host not found) or 405 (wrong
  method).
- **Auth:** `POST /run-coregx` requires a valid 64-character `apikey` in the
  body. Each successful call decrements the CoreGX credit pool by one. Failed
  calls also consume a credit, except rate-limit and `invalid-request-format`
  errors. `GET /get-syntax` needs no auth.

---

## POST `/run-coregx`

Runs a CoreGX program. First verifies all constraints can be resolved; if so,
produces the requested output.

### Request body

| Field | Type | Required | Description |
|---|---|---|---|
| `program` | string | yes | The CoreGX program (newline-separated commands). |
| `apikey` | string | yes | A valid CoreGX API key. Consumes one CoreGX credit. |
| `seed` | number | no | Random seed passed to CoreGX. Random integer if omitted. |
| `disableOptimization` | boolean | no | If `true`, disables point-location optimization, significantly speeding up the run. Default `false`. |
| `all` | boolean | no | If `true`, returns every output type (SVG, XML, equations) and overrides the individual flags below. |
| `svg` | boolean | no | Include SVG output in the response. |
| `xml` | boolean | no | Include XML output in the response. |
| `equations` | boolean | no | Include symbolic equation (measurement) results. |

Request at least one output flag (or `all`). To receive equation output, the
program must contain at least one `measure …` command *and* the request must set
`equations: true` (or `all`).

### Success response

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

Only the fields corresponding to requested output flags are present.

Each entry in `equations` is an object, not a plain string: `expression` is the
measured quantity as written in the `measure …` command, and `valueTex` is its
solved value (both `expressionTex` and `valueRealAsTex` are TeX-formatted
variants for typeset display). To show a plain-text line, join them yourself,
e.g. `` `${eq.expression} = ${eq.valueTex}` ``.

### Error codes

| Code | Meaning |
|---|---|
| `invalid-request-format` | Body missing or `program` absent. (Does not consume a credit.) |
| `invalid-gengx-api-key` | `apikey` not found. |
| `not-enough-gengx-credits` | Key has no remaining CoreGX credits. |
| `concurrent-rate-limit` | Too many in-flight requests from this IP. (No credit consumed.) |
| `ip-rate-limit` | Too many requests from this IP in the last minute. (No credit consumed.) |
| `unresolvable-constraints` | Constraints could not be resolved — the figure is overconstrained or contradictory. |
| `process-timed-out` | CoreGX did not finish within the time limit. Try `disableOptimization: true`. |
| `output-parse-error` / `server-error` | Server-side failure producing or parsing output. |
| *any other string* | A CoreGX error from a malformed command, e.g. `triangle requires 3 arguments`. Fix the program. |

### Example

```bash
curl -s https://api.coregx.dev/run-coregx \
  -H 'Content-Type: application/json' \
  -d '{
        "apikey": "<API_KEY>",
        "svg": true,
        "equations": true,
        "program": "anglemode degree\ntriangle A B C\nangle A B C 37.5\nangle A C B 67.5\nmeasure angle(B,A,C)"
      }'
```

---

## GET `/get-syntax`

Returns the CoreGX syntax guide (the full command/syntax reference) as a
Markdown string. No authentication, no parameters.

### Success response

```json
{ "ok": true, "value": "# Geometry Command Reference\n..." }
```

### Errors

| Code | Meaning |
|---|---|
| `method-not-allowed` | The endpoint only accepts `GET`. |
| `location-not-found` | Endpoint not found, or request not routed through an allowed host. |

Use this to retrieve the authoritative, up-to-date syntax at runtime. The
bundled `reference/syntax.md` is a snapshot of the same document.

---

## Rate limits

Applied per IP. Subject to change.

| Rule | CoreGX limit |
|---|---|
| Max concurrent requests | 3 |
| Max requests per IP per minute | 500 |

A rate-limited request does not consume a credit. On `concurrent-rate-limit` or
`ip-rate-limit`, back off briefly and retry.
