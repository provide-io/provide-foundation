#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Additional tests for safe decorators to improve code coverage."""

from __future__ import annotations

import asyncio
from typing import Never

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors.safe_decorators import (
    log_only_error_context,
)


class TestSafeDecoratorsCoverage(FoundationTestCase):
    """Test safe decorators for improved coverage."""

    def test_logger_access_available(self) -> None:
        """Test that logger functionality is available through foundation."""
        from provide.foundation.hub.foundation import get_foundation_logger

        logger = get_foundation_logger()
        assert logger is not None
        assert hasattr(logger, "debug")
        assert hasattr(logger, "error")

    def test_log_only_error_context_sync_function_success(self) -> None:
        """Test log_only_error_context with sync function - success case."""

        @log_only_error_context(log_success=True, log_level="debug")
        def test_func(x, y):
            return x + y

        result = test_func(2, 3)
        assert result == 5

    def test_log_only_error_context_sync_function_with_context(self) -> None:
        """Test log_only_error_context with context provider."""

        def context_func():
            return {"operation": "test_operation", "user": "test_user"}

        @log_only_error_context(
            context_provider=context_func,
            log_level="debug",
            log_success=True,
        )
        def test_func(value):
            return value * 2

        result = test_func(5)
        assert result == 10

    def test_log_only_error_context_sync_function_error(self) -> None:
        """Test log_only_error_context with sync function - error case."""

        @log_only_error_context(context_provider=lambda: {"test": "context"})
        def test_func() -> Never:
            raise ValueError("Test error")

        with pytest.raises(ValueError) as exc_info:
            test_func()

        assert str(exc_info.value) == "Test error"

    def test_log_only_error_context_sync_function_trace_level(self) -> None:
        """Test log_only_error_context with trace log level."""

        @log_only_error_context(log_level="trace")
        def test_func(x):
            return x**2

        result = test_func(4)
        assert result == 16

    def test_log_only_error_context_sync_function_info_level(self) -> None:
        """Test log_only_error_context with info log level (no entry logging)."""

        @log_only_error_context(log_level="info")
        def test_func(x):
            return x + 10

        result = test_func(5)
        assert result == 15

    def test_log_only_error_context_sync_function_no_context_provider(self) -> None:
        """Test log_only_error_context without context provider."""

        @log_only_error_context(log_success=True)
        def test_func() -> str:
            return "success"

        result = test_func()
        assert result == "success"

    @pytest.mark.asyncio
    async def test_log_only_error_context_async_function_success(self) -> None:
        """Test log_only_error_context with async function - success case."""

        @log_only_error_context(log_success=True, log_level="debug")
        async def async_test_func(x, y):
            await asyncio.sleep(0)  # Yield control without timing dependency
            return x * y

        result = await async_test_func(3, 4)
        assert result == 12

    @pytest.mark.asyncio
    async def test_log_only_error_context_async_function_with_context(self) -> None:
        """Test log_only_error_context with async function and context."""

        def context_func():
            return {"async_operation": "multiplication", "version": "1.0"}

        @log_only_error_context(
            context_provider=context_func,
            log_level="trace",
            log_success=True,
        )
        async def async_test_func(value):
            await asyncio.sleep(0)
            return value**3

        result = await async_test_func(2)
        assert result == 8

    @pytest.mark.asyncio
    async def test_log_only_error_context_async_function_error(self) -> None:
        """Test log_only_error_context with async function - error case."""

        @log_only_error_context(context_provider=lambda: {"async": "context"})
        async def async_test_func() -> Never:
            await asyncio.sleep(0)
            raise RuntimeError("Async test error")

        with pytest.raises(RuntimeError) as exc_info:
            await async_test_func()

        assert str(exc_info.value) == "Async test error"

    @pytest.mark.asyncio
    async def test_log_only_error_context_async_function_no_context(self) -> None:
        """Test log_only_error_context with async function without context."""

        @log_only_error_context(log_level="debug", log_success=True)
        async def async_test_func(msg) -> str:
            await asyncio.sleep(0)
            return f"processed: {msg}"

        result = await async_test_func("hello")
        assert result == "processed: hello"

    def test_decorator_preserves_function_metadata(self) -> None:
        """Test that decorator preserves original function metadata."""

        def original_func(a, b):
            """Original docstring."""
            return a + b

        decorated_func = log_only_error_context()(original_func)

        assert decorated_func.__name__ == original_func.__name__
        assert decorated_func.__doc__ == original_func.__doc__

    @pytest.mark.asyncio
    async def test_async_decorator_preserves_function_metadata(self) -> None:
        """Test that async decorator preserves original function metadata."""

        async def original_async_func(x):
            """Original async docstring."""
            return x * 2

        decorated_func = log_only_error_context()(original_async_func)

        assert decorated_func.__name__ == original_async_func.__name__
        assert decorated_func.__doc__ == original_async_func.__doc__

    def test_sync_function_with_warning_log_level(self) -> None:
        """Test sync function with warning log level (no entry logging)."""

        @log_only_error_context(log_level="warning", log_success=True)
        def test_func() -> str:
            return "test"

        result = test_func()
        assert result == "test"

    @pytest.mark.asyncio
    async def test_async_function_with_warning_log_level(self) -> None:
        """Test async function with warning log level (no entry logging)."""

        @log_only_error_context(log_level="warning", log_success=True)
        async def async_test_func() -> str:
            return "async_test"

        result = await async_test_func()
        assert result == "async_test"

    def test_sync_function_context_provider_exception(self) -> None:
        """Test sync function when context provider raises exception."""

        def failing_context() -> Never:
            raise Exception("Context provider failed")

        @log_only_error_context(context_provider=failing_context)
        def test_func() -> str:
            return "should not reach here"

        # The decorator should not catch context provider exceptions
        with pytest.raises(Exception) as exc_info:
            test_func()
        assert "Context provider failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_async_function_context_provider_exception(self) -> None:
        """Test async function when context provider raises exception."""

        def failing_context() -> Never:
            raise Exception("Async context provider failed")

        @log_only_error_context(context_provider=failing_context)
        async def async_test_func() -> str:
            return "should not reach here"

        with pytest.raises(Exception) as exc_info:
            await async_test_func()
        assert "Async context provider failed" in str(exc_info.value)


# 🧱🏗️🔚
