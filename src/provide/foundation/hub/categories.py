#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Component category definitions for Foundation Hub.

This module contains only the ComponentCategory enum to avoid circular imports.
It can be safely imported by any other hub module."""

from __future__ import annotations

from enum import Enum


class ComponentCategory(Enum):
    """Predefined component categories for Foundation.

    These are the standard dimension values used internally by Foundation.
    External components can still use custom string dimensions for compatibility.
    """

    # Core categories
    COMMAND = "command"
    COMPONENT = "component"

    # Configuration and data sources
    CONFIG_SOURCE = "config_source"
    CONFIG_SCHEMA = "config_schema"

    # Processing pipeline
    PROCESSOR = "processor"
    ERROR_HANDLER = "error_handler"
    FORMATTER = "formatter"
    FILTER = "filter"

    # Transport layer
    TRANSPORT = "transport"
    TRANSPORT_MIDDLEWARE = "transport.middleware"
    TRANSPORT_AUTH = "transport.auth"
    TRANSPORT_CACHE = "transport.cache"

    # Event system
    EVENT_SET = "eventset"


__all__ = ["ComponentCategory"]

# 🧱🏗️🔚
