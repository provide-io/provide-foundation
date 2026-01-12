#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from provide.foundation.utils.optional_deps import OptionalDependency

"""Centralized Click dependency handling.

This module contains all the logic for handling the optional 'click' package.
When click is not installed, stub implementations are provided that raise
helpful ImportErrors with installation instructions.

This now uses the centralized OptionalDependency utility to eliminate
repetitive try/except ImportError boilerplate.
"""


# Load click using centralized dependency handler
_click_dep = OptionalDependency("click", "cli")
_HAS_CLICK = _click_dep.is_available()
click = _click_dep.import_package()


__all__ = ["_HAS_CLICK", "click"]

# 🧱🏗️🔚
