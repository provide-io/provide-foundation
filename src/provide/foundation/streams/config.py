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

"""Stream configuration for console output settings.

This module provides configuration for console stream behavior,
including color support and testing mode detection.
"""


@define(slots=True, repr=False)
class StreamConfig(RuntimeConfig):
    """Configuration for console stream output behavior."""

    no_color: bool = field(
        default=False,
        env_var="NO_COLOR",
        converter=parse_bool_extended,
        description="Disable color output in console",
    )

    force_color: bool = field(
        default=False,
        env_var="FORCE_COLOR",
        converter=parse_bool_extended,
        description="Force color output even when not in TTY",
    )

    click_testing: bool = field(
        default=False,
        env_var="CLICK_TESTING",
        converter=parse_bool_extended,
        description="Indicates if running inside Click testing framework",
    )

    force_stream_redirect: bool = field(
        default=False,
        env_var="FOUNDATION_FORCE_STREAM_REDIRECT",
        converter=parse_bool_extended,
        description="Force stream redirection in testing (bypasses Click testing guard)",
    )

    def supports_color(self) -> bool:
        """Determine if the console supports color output.

        Returns:
            True if color is supported, False otherwise

        """
        if self.no_color:
            return False

        if self.force_color:
            return True

        # Additional logic for TTY detection would go here
        # For now, just return based on the flags
        return not self.no_color


# Global instance for easy access
_stream_config: StreamConfig | None = None


def get_stream_config() -> StreamConfig:
    """Get the global stream configuration instance.

    Returns:
        StreamConfig instance loaded from environment

    """
    global _stream_config
    if _stream_config is None:
        _stream_config = StreamConfig.from_env()
    return _stream_config


def reset_stream_config() -> None:
    """Reset the global stream configuration (mainly for testing)."""
    global _stream_config
    _stream_config = None


# 🧱🏗️🔚
