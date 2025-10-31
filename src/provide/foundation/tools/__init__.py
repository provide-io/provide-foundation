#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.tools.base import (
    BaseToolManager,
    ToolError,
    ToolMetadata,
)
from provide.foundation.tools.cache import ToolCache
from provide.foundation.tools.downloader import ToolDownloader
from provide.foundation.tools.installer import ToolInstaller
from provide.foundation.tools.registry import (
    get_tool_manager,
    get_tool_registry,
    register_tool_manager,
)
from provide.foundation.tools.resolver import VersionResolver

"""Provide Foundation Tools Module
================================

Unified tool management system for downloading, verifying, installing, and
managing development tools across the provide-io ecosystem.

This module provides:
- Base classes for tool managers
- Download orchestration with progress reporting
- Checksum and signature verification
- Installation handling for various formats
- Version resolution (latest, semver, wildcards)
- Caching with TTL support
- Tool registry integration

Example:
    >>> from provide.foundation.tools import get_tool_manager
    >>> from provide.foundation.config import BaseConfig
    >>>
    >>> config = BaseConfig()
    >>> tf_manager = get_tool_manager("terraform", config)
    >>> tf_manager.install("1.5.0")
    PosixPath('/home/user/.provide-foundation/tools/terraform/1.5.0')

"""

__all__ = [
    # Base classes
    "BaseToolManager",
    # Components
    "ToolCache",
    "ToolDownloader",
    "ToolError",
    "ToolInstaller",
    "ToolMetadata",
    "VersionResolver",
    # Registry functions
    "get_tool_manager",
    "get_tool_registry",
    "register_tool_manager",
]

# 🧱🏗️🔚
