"""Additional tests for safe decorators to improve code coverage."""

import asyncio
from unittest.mock import Mock, patch
import pytest

from provide.foundation.errors.safe_decorators import (
    log_only_error_context,
    _get_logger,
)


class TestSafeDecoratorsCoverage:
    """Test safe decorators for improved coverage."""

    def test_get_logger_function(self):
        """Test _get_logger function returns logger."""
        logger = _get_logger()
        assert logger is not None
        assert hasattr(logger, "debug")
        assert hasattr(logger, "error")

    def test_log_only_error_context_sync_function_success(self):
        """Test log_only_error_context with sync function - success case."""

        @log_only_error_context(log_success=True, log_level="debug")
        def test_func(x, y):
            return x + y

        result = test_func(2, 3)
        assert result == 5

    def test_log_only_error_context_sync_function_with_context(self):
        """Test log_only_error_context with context provider."""

        def context_func():
            return {"operation": "test_operation", "user": "test_user"}

        @log_only_error_context(
            context_provider=context_func, log_level="debug", log_success=True
        )
        def test_func(value):
            return value * 2

        result = test_func(5)
        assert result == 10

    def test_log_only_error_context_sync_function_error(self):
        """Test log_only_error_context with sync function - error case."""

        @log_only_error_context(context_provider=lambda: {"test": "context"})
        def test_func():
            raise ValueError("Test error")

        with pytest.raises(ValueError) as exc_info:
            test_func()

        assert str(exc_info.value) == "Test error"

    def test_log_only_error_context_sync_function_trace_level(self):
        """Test log_only_error_context with trace log level."""

        @log_only_error_context(log_level="trace")
        def test_func(x):
            return x**2

        result = test_func(4)
        assert result == 16

    def test_log_only_error_context_sync_function_info_level(self):
        """Test log_only_error_context with info log level (no entry logging)."""

        @log_only_error_context(log_level="info")
        def test_func(x):
            return x + 10

        result = test_func(5)
        assert result == 15

    def test_log_only_error_context_sync_function_no_context_provider(self):
        """Test log_only_error_context without context provider."""

        @log_only_error_context(log_success=True)
        def test_func():
            return "success"

        result = test_func()
        assert result == "success"

    @pytest.mark.asyncio
    async def test_log_only_error_context_async_function_success(self):
        """Test log_only_error_context with async function - success case."""

        @log_only_error_context(log_success=True, log_level="debug")
        async def async_test_func(x, y):
            await asyncio.sleep(0.001)  # Small delay to make it async
            return x * y

        result = await async_test_func(3, 4)
        assert result == 12

    @pytest.mark.asyncio
    async def test_log_only_error_context_async_function_with_context(self):
        """Test log_only_error_context with async function and context."""

        def context_func():
            return {"async_operation": "multiplication", "version": "1.0"}

        @log_only_error_context(
            context_provider=context_func, log_level="trace", log_success=True
        )
        async def async_test_func(value):
            await asyncio.sleep(0.001)
            return value**3

        result = await async_test_func(2)
        assert result == 8

    @pytest.mark.asyncio
    async def test_log_only_error_context_async_function_error(self):
        """Test log_only_error_context with async function - error case."""

        @log_only_error_context(context_provider=lambda: {"async": "context"})
        async def async_test_func():
            await asyncio.sleep(0.001)
            raise RuntimeError("Async test error")

        with pytest.raises(RuntimeError) as exc_info:
            await async_test_func()

        assert str(exc_info.value) == "Async test error"

    @pytest.mark.asyncio
    async def test_log_only_error_context_async_function_no_context(self):
        """Test log_only_error_context with async function without context."""

        @log_only_error_context(log_level="debug", log_success=True)
        async def async_test_func(msg):
            await asyncio.sleep(0.001)
            return f"processed: {msg}"

        result = await async_test_func("hello")
        assert result == "processed: hello"

    def test_decorator_preserves_function_metadata(self):
        """Test that decorator preserves original function metadata."""

        def original_func(a, b):
            """Original docstring."""
            return a + b

        decorated_func = log_only_error_context()(original_func)

        assert decorated_func.__name__ == original_func.__name__
        assert decorated_func.__doc__ == original_func.__doc__

    @pytest.mark.asyncio
    async def test_async_decorator_preserves_function_metadata(self):
        """Test that async decorator preserves original function metadata."""

        async def original_async_func(x):
            """Original async docstring."""
            return x * 2

        decorated_func = log_only_error_context()(original_async_func)

        assert decorated_func.__name__ == original_async_func.__name__
        assert decorated_func.__doc__ == original_async_func.__doc__

    def test_sync_function_with_warning_log_level(self):
        """Test sync function with warning log level (no entry logging)."""

        @log_only_error_context(log_level="warning", log_success=True)
        def test_func():
            return "test"

        result = test_func()
        assert result == "test"

    @pytest.mark.asyncio
    async def test_async_function_with_warning_log_level(self):
        """Test async function with warning log level (no entry logging)."""

        @log_only_error_context(log_level="warning", log_success=True)
        async def async_test_func():
            return "async_test"

        result = await async_test_func()
        assert result == "async_test"

    def test_sync_function_context_provider_exception(self):
        """Test sync function when context provider raises exception."""

        def failing_context():
            raise Exception("Context provider failed")

        @log_only_error_context(context_provider=failing_context)
        def test_func():
            return "should not reach here"

        # The decorator should not catch context provider exceptions
        with pytest.raises(Exception) as exc_info:
            test_func()
        assert "Context provider failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_async_function_context_provider_exception(self):
        """Test async function when context provider raises exception."""

        def failing_context():
            raise Exception("Async context provider failed")

        @log_only_error_context(context_provider=failing_context)
        async def async_test_func():
            return "should not reach here"

        with pytest.raises(Exception) as exc_info:
            await async_test_func()
        assert "Async context provider failed" in str(exc_info.value)
