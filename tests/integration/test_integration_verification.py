#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Verification tests for lazy initialization fixes."""

from __future__ import annotations

import os

from provide.testkit import FoundationTestCase


class TestIntegrationVerification(FoundationTestCase):
    """Verification tests for lazy initialization."""

    def test_basic_lazy_init(self) -> None:
        """Test basic lazy initialization works."""
        # Clear environment
        env_vars_to_clear = [
            "PROVIDE_SERVICE_NAME",
            "PROVIDE_LOG_CONSOLE_FORMATTER",
            "PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED",
            "PROVIDE_LOG_DAS_EMOJI_ENABLED",
        ]
        for var in env_vars_to_clear:
            os.environ.pop(var, None)

        from provide.foundation import logger

        logger.info("Basic lazy initialization test")
        # If we get here without error, the test passes

    def test_service_name_injection(self) -> None:
        """Test service name injection with JSON format."""

        from provide.testkit.mocking import patch

        # Set environment like the failing test (restored automatically after context)
        with patch.dict(
            os.environ,
            {
                "PROVIDE_SERVICE_NAME": "test-service",
                "PROVIDE_LOG_CONSOLE_FORMATTER": "json",
            },
            clear=False,
        ):
            from provide.foundation import logger

            logger.info("Message with service name")
            # If we get here without error, the test passes

    def test_emergency_fallback(self) -> None:
        """Test emergency fallback doesn't crash."""

        from provide.foundation.logger.base import FoundationLogger

        test_logger = FoundationLogger()

        # Trigger emergency fallback by setting error state
        from provide.foundation.logger.core import (
            _LAZY_SETUP_STATE,  # Ensure we use the state dict
        )

        _LAZY_SETUP_STATE["error"] = Exception("Test error")  # Set error state
        _LAZY_SETUP_STATE["done"] = False  # Ensure done is false so error path is taken

        try:
            test_logger.info("Emergency fallback test")
            # Further assertions could be made if _setup_emergency_fallback was mocked
            # or if there was discernible output from emergency logger.
            # For now, just ensuring it doesn't crash is the main goal of this test.
        except Exception as e:  # pragma: no cover
            raise AssertionError(f"Emergency fallback test failed: {e}") from e  # B904


# 🧱🏗️🔚
