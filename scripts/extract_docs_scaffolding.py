#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Materialise the shared docs scaffolding that mkdocs.yml inherits from.

mkdocs.yml opens with `INHERIT: .provide/foundry/base-mkdocs.yml`, and
.gitignore excludes `.provide/foundry/` because it is an extract of the
provide-foundry package rather than source of ours. Nothing in a fresh checkout
creates it, so `mkdocs build` there fails before reading a single page:

    Error: Inherited config file '.provide/foundry/base-mkdocs.yml' does not exist

which is what every documentation CI run has done. Locally the directory
happens to be present, so the failure is invisible on a developer machine.

Run this before mkdocs. It writes `.provide/foundry/` from the installed
provide-foundry: the base config, the theme referenced by `custom_dir`, the
shared partials, the docs helper scripts, and gen_ref_pages.py for the
mkdocs-gen-files plugin.

Exit codes:
  0 - scaffolding extracted
  1 - provide-foundry is not installed
"""

from __future__ import annotations

from pathlib import Path
import sys


def main() -> int:
    """Extract the docs scaffolding into the current working directory."""
    try:
        from provide.foundry.config import extract_base_mkdocs
    except ImportError:
        print(
            "provide-foundry is not installed, so the docs scaffolding cannot be\n"
            "extracted and `mkdocs build` will fail on its INHERIT line.\n"
            "It belongs to the `docs` dependency group: `uv sync --group docs`.",
            file=sys.stderr,
        )
        return 1

    base_mkdocs = extract_base_mkdocs(Path.cwd())
    print(f"✅ Docs scaffolding extracted to {base_mkdocs.parent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# 🧱🏗️🔚
