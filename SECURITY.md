# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.4.x   | yes       |
| 0.3.x   | security fixes only |
| < 0.3   | no        |

## Reporting a vulnerability

Do **not** open a public GitHub issue for security problems. Email `security@albumforge.dev` with:

- A description of the issue and its impact.
- Steps to reproduce, or a proof-of-concept.
- The affected version(s) and platform.
- Whether you'd like credit in the advisory.

We acknowledge within 72 hours and aim to ship a fix or mitigation within 14 days for high-severity issues.

## Scope

In scope:

- Arbitrary code execution via a malicious extension package.
- Path traversal in the checkpoint loader or the exporter.
- SSRF in the prompt-enhancer HTTP bridge.
- Unsafe deserialization of `.albumforge` project files.

Out of scope:

- Prompt injection against the diffusion model itself (that's a model problem, not a host problem).
- NSFW output from user-supplied prompts (the host has an optional content filter; it is off by default and documented as such).
- Denial of service from intentionally huge images (documented memory ceiling in `docs/limits.md`).

## Extension trust model

Extensions run in-process with full host privileges. This is a deliberate design choice for performance. **Only install extensions you trust.** The registry verifies a SHA-256 hash from `extension.toml` against the actual module file at load time, but this is integrity, not authenticity — it catches corruption, not malice. A future release adds an optional subprocess sandbox; see `docs/roadmap.md`.

## Dependency hygiene

We pin all direct dependencies in `requirements.txt` and audit them with `pip-audit` in CI. Transitive dependencies are pinned via `requirements.lock`. If you find a CVE in a transitive dep, open a PR bumping the lock file.