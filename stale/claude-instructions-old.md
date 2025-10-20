<!--
STALE DOCUMENTATION - MOVED 2025-10-19
This file was moved to stale/ because it referenced non-existent setup files (env.sh)
and conflicted with the actual development environment setup.

The project uses standard Python virtual environment with uv:
- Create: uv venv
- Activate: source .venv/bin/activate (or workenv/provide-foundation_darwin_arm64/bin/activate)
- Install: uv sync

See the main CLAUDE.md file in the project root for current instructions.
-->

- use source env.sh, and ensure that '.venv' is *not* used. it should be using the logic to proision in 'workenv/'
- I do not need migration logic. Or backward compatibility logic. None of that unless i explicitly approve it.
- It must all use moddern typing too. no Dict,List,Optiopnal, etc. only modern. across all files. everywhere. make sure to remember that
- Rather than "no hardcoded defaults" i mean "no inline defaults." defaults may be stored in a common file for the project. either defaults.py or constants.py, and THOSE will ALWAYS be used instead of inline defaults.
- ignore any bfiles.
- it is okay to use future annotation for unquoted types.
- it is okay to use futures for unquoted annotations.
- it is okay to use __future__ annotatrion for unquoted types
- It is okay to use `from __future__ import annotations`. Especially to support unquoted types.
- After an updated to a Python file, you will run `ruff format` on it, and `ruff check --fix` and any other pertinent code quality in order to prevent problems up front.
- After writing each Python file, run the code quality tools - ruff check --fix --unsafe-fixes, ty check, mypy, ruff format, then run each of the tools again. this way CQ is performed during the dev process.
- Every time a TUI is run, upon exit run the mouse terminal-reset codes - `printf '\e[?1000l\e[?1002l\e[?1003l\e[?10061l'`
- never use relative imports. only absolute imports always.