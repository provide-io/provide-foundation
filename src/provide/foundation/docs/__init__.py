#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Documentation generation utilities for MkDocs with mkdocstrings."""

from __future__ import annotations

from provide.foundation.docs.generator import (
    _HAS_MKDOCS,
    APIDocGenerator,
    generate_api_docs,
)

__all__ = [
    # Internal flags (for tests)
    "_HAS_MKDOCS",
    "APIDocGenerator",
    "generate_api_docs",
]

# 🧱🏗️🔚
