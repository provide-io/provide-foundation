#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from attrs import define

from provide.foundation.config.base import field
from provide.foundation.config.converters import parse_bool_extended
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.serialization.defaults import (
    DEFAULT_SERIALIZATION_CACHE_ENABLED,
    DEFAULT_SERIALIZATION_CACHE_SIZE,
)

"""Serialization configuration for Foundation."""


@define(slots=True, repr=False)
class SerializationCacheConfig(RuntimeConfig):
    """Configuration for serialization caching behavior."""

    cache_enabled: bool = field(
        default=DEFAULT_SERIALIZATION_CACHE_ENABLED,
        env_var="FOUNDATION_SERIALIZATION_CACHE_ENABLED",
        converter=parse_bool_extended,
        description="Enable serialization caching",
    )
    cache_size: int = field(
        default=DEFAULT_SERIALIZATION_CACHE_SIZE,
        env_var="FOUNDATION_SERIALIZATION_CACHE_SIZE",
        converter=int,
        description="Maximum number of cached serialization results",
    )


# 🧱🏗️🔚
