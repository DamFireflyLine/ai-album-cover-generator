# Contributing to ai-album-cover-generator

Thanks for wanting to help build the best open-source AI album cover generator. This is a plugin-host desktop application: a stable core host plus a registry of extension modules that plug into it. Read this before opening a PR.

## Architecture in one paragraph

The host (`albumforge/host/`) owns the window, the event bus, and the plugin lifecycle. Extensions live under `albumforge/extensions/` and register themselves against the shared contracts in `albumforge/contracts/`. Nothing in the host imports a concrete extension by name — the loader discovers them at runtime via the registry. If you find yourself writing `from albumforge.extensions.sdxl_renderer import ...` inside the host, stop, you're doing it wrong.

## Setting up

```bash
git clone https://github.com/yourname/ai-album-cover-generator
cd ai-album-cover-generator
python -m venv .venv
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt
python -m albumforge
```

First run pulls the default diffusion checkpoint into `models/`. That's ~4GB. Be patient. The progress bar is real, not decorative.

## Adding an extension

1. Create a folder under `albumforge/extensions/your_extension/`.
2. Drop an `extension.toml` manifest in it. Copy `albumforge/extensions/_template/extension.toml` as a starting point.
3. Implement the relevant contract. Renderers implement `RendererContract`. Prompt enhancers implement `PromptEnhancerContract`. Post-processors implement `PostProcessorContract`. Exporters implement `ExporterContract`.
4. Call `registry.register(...)` in your module's `activate()` function.
5. Add a test under `tests/extensions/`. Extensions without tests get closed.

## Code style

- Black, line length 100. `black albumforge tests`
- Ruff for linting. `ruff check albumforge tests`
- Type hints on every public function. We run mypy in CI with `--strict` on `albumforge/contracts/` and `albumforge/host/`.
- No `print()` in library code. Use `albumforge.utils.logging.get_logger(__name__)`.

## Commit messages

Imperative mood. `fix:`, `feat:`, `refactor:`, `docs:`, `test:` prefixes. One logical change per commit. If your commit message needs the word "and" more than once, split it.

## Pull requests

- Branch off `main`. Rebase, don't merge.
- One PR, one feature.
- Update `CHANGELOG.md` under `## Unreleased`.
- CI must be green. No exceptions, no "I'll fix the lint in a follow-up."

## Reporting bugs

Open an issue with the template. Include: OS build, Python version, GPU + driver, the checkpoint you were using, and the full traceback. "It doesn't work" is not a bug report.

## Security

See `SECURITY.md`. Do not open public issues for security problems.