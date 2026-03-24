# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅ Yes     |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Please report security issues by emailing **darshjme@gmail.com** with:

- A description of the vulnerability.
- Steps to reproduce.
- Potential impact.
- Any suggested fix (optional).

You will receive an acknowledgement within 48 hours and a resolution timeline within 5 business days.

## Security Model

`agent-selector` is a pure Python routing library with zero runtime dependencies.
It does not:

- Make network calls.
- Persist data to disk.
- Execute arbitrary code beyond what callers explicitly pass as `handler` callables.

The primary security surface is the `handler` callable passed to `Candidate`. Callers
are responsible for ensuring that handlers they register are trusted.
