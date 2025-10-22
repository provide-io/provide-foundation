# sitecustomize.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Auto-load setproctitle blocker for all Python processes.

This file is automatically loaded by Python when src/ is in PYTHONPATH.
It ensures the setproctitle import blocker is installed before any other
code runs, including pytest-xdist worker initialization.

The blocker prevents setproctitle from being imported, which causes
pytest-xdist to gracefully fall back to its no-op implementation instead
of using setproctitle (which causes macOS terminal freezing).
"""

from __future__ import annotations

import sys

# Only install blocker if testkit is available
try:
    from provide.testkit.pytest_plugin import SetproctitleImportBlocker

    # Install blocker if not already installed
    if not any(isinstance(hook, SetproctitleImportBlocker) for hook in sys.meta_path):
        sys.meta_path.insert(0, SetproctitleImportBlocker())
except ImportError:
    # testkit not installed, skip blocker
    pass


# <3 🧱🤝🧪🪄
