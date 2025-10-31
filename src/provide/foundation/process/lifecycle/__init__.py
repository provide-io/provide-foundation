#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.process.lifecycle.managed import ManagedProcess
from provide.foundation.process.lifecycle.monitoring import wait_for_process_output

"""Process lifecycle management utilities.

This module provides utilities for managing long-running subprocesses with
proper lifecycle management, monitoring, and graceful shutdown capabilities.
"""

__all__ = [
    "ManagedProcess",
    "wait_for_process_output",
]

# 🧱🏗️🔚
