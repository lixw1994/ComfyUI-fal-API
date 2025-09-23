# Repository Guidelines

## Project Structure & Modules
- `nodes/`: Implementation of ComfyUI custom nodes (image, video, llm, vlm, trainer, upscaler). Each file exposes `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS`.
- `__init__.py`: Aggregates all node mappings from `nodes/` for ComfyUI discovery.
- `requirements.txt`: Runtime dependencies (fal-client, torch, opencv-python).
- `pyproject.toml`: Package metadata and Comfy Registry config.
- `config.ini`: Local API configuration (`[API] FAL_KEY = ...`).
- `example_workflows/`: Sample ComfyUI workflows to validate nodes.

## Build, Test, and Development
- Install deps: `pip install -r requirements.txt`
- Local usage: clone/symlink into ComfyUI’s `custom_nodes/`, set `FAL_KEY`, restart ComfyUI.
- Quick sanity check: load a flow from `example_workflows/` and run an image/video node.
- Environment variable alternative: `export FAL_KEY=your_actual_api_key`

## Coding Style & Naming
- Python, 4‑space indent, keep functions small and explicit.
- Naming: `snake_case` for functions/vars, `PascalCase` for classes, module files as `*_node.py` inside `nodes/`.
- Node registration: expose `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS`; import patterns must not execute heavy work at import time.
- I/O: prefer explicit parameters; validate inputs; surface concise errors to ComfyUI.

## Testing Guidelines
- Manual tests: run example workflows; verify outputs, logs, and parameter validation.
- Add lightweight unit tests for pure utilities in `nodes/fal_utils.py` if modified; name files `test_*.py` and functions `test_*`.
- Regression: for new nodes, include a minimal example JSON in `example_workflows/`.

## Commit & Pull Requests
- Commits: imperative, concise subject; scope prefix helpful, e.g. `nodes: add Flux Pro Kontext Multi` or `fix: handle missing FAL_KEY`.
- PRs must include: summary, motivation, screenshots or sample outputs, steps to reproduce/validate, and any config changes.
- Link related issues and note breaking changes clearly.
- Keep diffs focused; update `README.md` and examples when user-facing behavior changes.

## Security & Configuration
- Never commit real API keys. Use `config.ini` locally or the `FAL_KEY` environment variable.
- Handle secrets via environment in CI; publishing to Comfy Registry is automated for maintainers via `.github/workflows/publish.yml`.
