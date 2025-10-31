#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import sys

from provide.foundation.config.defaults import EXIT_ERROR, EXIT_SIGINT, EXIT_SUCCESS
from provide.foundation.hub.foundation import get_foundation_logger

"""Process exit utilities for standardized exit handling."""


def exit_success(message: str | None = None) -> None:
    """Exit with success status.

    Args:
        message: Optional message to log before exiting

    """
    if message:
        logger = get_foundation_logger()
        logger.info(f"Exiting successfully: {message}")
    sys.exit(EXIT_SUCCESS)


def exit_error(message: str | None = None, code: int = EXIT_ERROR) -> None:
    """Exit with error status.

    Args:
        message: Optional error message to log before exiting
        code: Exit code to use (defaults to EXIT_ERROR)

    """
    if message:
        logger = get_foundation_logger()
        logger.error(f"Exiting with error: {message}", exit_code=code)
    sys.exit(code)


def exit_interrupted(message: str = "Process interrupted") -> None:
    """Exit due to interrupt signal (SIGINT).

    Args:
        message: Message to log before exiting

    """
    logger = get_foundation_logger()
    logger.warning(f"Exiting due to interrupt: {message}")
    sys.exit(EXIT_SIGINT)


# 🧱🏗️🔚
