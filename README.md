# Vulnerable Frontend Test Fixtures

Intentionally vulnerable HTML/JS pages for exercising a shift-left security
scanner (SAST / secret-scanning / SCA / GenAI-based review) inside a CI/CD
pipeline. **Do not deploy these publicly or reuse the patterns in real
code** — each file is a minimal, self-contained trigger for one class of
finding, with the vulnerable line marked `// <-- sink` or similar and a
`FIX (for reference)` note underneath.

| File | Vulnerability class | CWE | OWASP category |
|---|---|---|---|
| `dom-xss.html` | DOM-based XSS via `innerHTML` | CWE-79 | A03: Injection |
| `stored-xss.html` | Stored XSS via unsanitized render | CWE-79 | A03: Injection |
| `hardcoded-secrets.js` | Hardcoded API keys / JWT secret / DB creds | CWE-798 | A02/A05 |
| `insecure-storage.html` | Sensitive data (PAN, session token) in `localStorage` | CWE-312 | A02: Crypto Failures |
| `eval-injection.html` | Code injection via `eval()` | CWE-95 | A03: Injection |
| `open-redirect.html` | Unvalidated redirect target | CWE-601 | A01: Broken Access Control |
| `csrf-vulnerable-form.html` | State-changing form, no CSRF token | CWE-352 | A01: Broken Access Control |
| `insecure-postmessage.html` | `postMessage` handler, no origin check | CWE-346 | A03/A05 |
| `outdated-dependency.html` | Old jQuery/Lodash builds with known CVEs | CWE-1104 | A06: Vulnerable Components |
| `clickjacking.html` | No frame protection on sensitive action | CWE-1021 | A05: Security Misconfiguration |
| `prototype-pollution.html` | Unsafe deep merge of URL-controlled JSON | CWE-1321 | A03: Injection |
| `weak-token-generation.js` | `Math.random()` used for session/reset tokens | CWE-338 | A02: Crypto Failures |
| `client-side-auth-bypass.html` | Authorization enforced only in client JS/CSS | CWE-602 | A01: Broken Access Control |
| `missing-sri.html` | CDN script with no integrity/crossorigin attrs | CWE-829 | A08: Software/Data Integrity |
| `redos-validation.js` | Catastrophic-backtracking regex (ReDoS) | CWE-1333 | A05: Security Misconfiguration |
| `insecure-file-upload.html` | Extension-only file validation, client-side | CWE-434 | A04: Insecure Design |
| `cleartext-transmission.html` | Login form posts over plain `http://` | CWE-319 | A02: Crypto Failures |

## Suggested use

1. Point your pipeline's scan stage (SAST + secret scan + SCA) at this
   folder as a fixture/regression set.
2. Assert that each file produces at least one finding of its listed CWE.
3. Optionally add a "clean" counterpart per file (using the `FIX` notes)
   to also test for false positives once remediated.

## Not included on purpose

No backend/server code is included — these are frontend-only sinks. If
your pipeline also scans backend code, you'll want a parallel fixture set
for server-side classes (SQLi, SSRF, path traversal, insecure
deserialization, etc.) — happy to generate that separately if useful.
