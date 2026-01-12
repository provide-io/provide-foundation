#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for utils/timing.py module."""

from __future__ import annotations

import contextvars
import time

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.utils.timing import _PROVIDE_CONTEXT_TRACE_ID, timed_block


class TestTimedBlock(FoundationTestCase):
    """Test timed_block context manager."""

    def test_timed_block_success(self) -> None:
        """Test timed_block with successful operation."""
        mock_logger = Mock()

        with timed_block(mock_logger, "test_operation") as ctx:
            ctx["custom_key"] = "custom_value"
            time.sleep(0.01)  # Small delay to ensure measurable duration

        # Should call debug on start and info on completion
        assert mock_logger.debug.call_count == 1
        assert mock_logger.info.call_count == 1
        assert mock_logger.error.call_count == 0

        # Check start log
        start_call = mock_logger.debug.call_args
        assert "test_operation started" in start_call[0]

        # Check completion log
        completion_call = mock_logger.info.call_args
        assert "test_operation completed" in completion_call[0]

        # Check that duration and context are included
        completion_kwargs = completion_call[1]
        assert "duration_seconds" in completion_kwargs
        assert "outcome" in completion_kwargs
        assert completion_kwargs["outcome"] == "success"
        assert "custom_key" in completion_kwargs
        assert completion_kwargs["custom_key"] == "custom_value"
        assert completion_kwargs["duration_seconds"] > 0

    def test_timed_block_with_exception(self) -> None:
        """Test timed_block with exception."""
        mock_logger = Mock()

        with pytest.raises(ValueError, match="test error"):
            with timed_block(mock_logger, "test_operation") as ctx:
                ctx["custom_key"] = "custom_value"
                time.sleep(0.01)
                raise ValueError("test error")

        # Should call debug on start and error on exception
        assert mock_logger.debug.call_count == 1
        assert mock_logger.info.call_count == 0
        assert mock_logger.error.call_count == 1

        # Check error log
        error_call = mock_logger.error.call_args
        assert "test_operation failed" in error_call[0]

        # Check that error details are included
        error_kwargs = error_call[1]
        assert "duration_seconds" in error_kwargs
        assert "outcome" in error_kwargs
        assert error_kwargs["outcome"] == "error"
        assert "error.message" in error_kwargs
        assert error_kwargs["error.message"] == "test error"
        assert "error.type" in error_kwargs
        assert error_kwargs["error.type"] == "ValueError"
        assert "custom_key" in error_kwargs
        assert error_kwargs["custom_key"] == "custom_value"
        assert error_kwargs["duration_seconds"] > 0
        assert "exc_info" in error_kwargs
        assert error_kwargs["exc_info"] is True

    def test_timed_block_with_layer_keys(self) -> None:
        """Test timed_block with layer keys."""
        mock_logger = Mock()
        layer_keys = {"layer": "database", "operation": "query"}

        with timed_block(mock_logger, "db_query", layer_keys=layer_keys):
            pass

        # Check that layer keys are included in logs
        start_call = mock_logger.debug.call_args
        start_kwargs = start_call[1]
        assert "layer" in start_kwargs
        assert start_kwargs["layer"] == "database"
        assert "operation" in start_kwargs
        assert start_kwargs["operation"] == "query"

        completion_call = mock_logger.info.call_args
        completion_kwargs = completion_call[1]
        assert "layer" in completion_kwargs
        assert completion_kwargs["layer"] == "database"
        assert "operation" in completion_kwargs
        assert completion_kwargs["operation"] == "query"

    def test_timed_block_with_initial_kvs(self) -> None:
        """Test timed_block with initial key-value pairs."""
        mock_logger = Mock()
        initial_kvs = {"query_type": "SELECT", "table": "users"}

        with timed_block(mock_logger, "db_query", initial_kvs=initial_kvs):
            pass

        # Check that initial kvs are included in logs
        start_call = mock_logger.debug.call_args
        start_kwargs = start_call[1]
        assert "query_type" in start_kwargs
        assert start_kwargs["query_type"] == "SELECT"
        assert "table" in start_kwargs
        assert start_kwargs["table"] == "users"

    def test_timed_block_with_extra_kvs(self) -> None:
        """Test timed_block with extra keyword arguments."""
        mock_logger = Mock()

        with timed_block(mock_logger, "test_op", user_id=123, session_id="abc"):
            pass

        # Check that extra kvs are included in logs
        start_call = mock_logger.debug.call_args
        start_kwargs = start_call[1]
        assert "user_id" in start_kwargs
        assert start_kwargs["user_id"] == 123
        assert "session_id" in start_kwargs
        assert start_kwargs["session_id"] == "abc"

    def test_timed_block_kvs_priority(self) -> None:
        """Test key-value pair priority (extra_kvs override initial_kvs)."""
        mock_logger = Mock()
        layer_keys = {"priority": "layer"}
        initial_kvs = {"priority": "initial", "key1": "value1"}

        with timed_block(
            mock_logger,
            "test_op",
            layer_keys=layer_keys,
            initial_kvs=initial_kvs,
            priority="extra",
            key2="value2",
        ):
            pass

        # Check that extra_kvs override initial_kvs which override layer_keys
        start_call = mock_logger.debug.call_args
        start_kwargs = start_call[1]
        assert start_kwargs["priority"] == "extra"  # extra_kvs wins
        assert start_kwargs["key1"] == "value1"  # from initial_kvs
        assert start_kwargs["key2"] == "value2"  # from extra_kvs

    def test_timed_block_with_trace_id(self) -> None:
        """Test timed_block with trace_id in context."""
        mock_logger = Mock()
        trace_id = "trace-123-456"

        # Set trace_id in context
        token = _PROVIDE_CONTEXT_TRACE_ID.set(trace_id)
        try:
            with timed_block(mock_logger, "test_operation"):
                pass
        finally:
            _PROVIDE_CONTEXT_TRACE_ID.reset(token)

        # Check that trace_id is included in logs
        start_call = mock_logger.debug.call_args
        start_kwargs = start_call[1]
        assert "trace_id" in start_kwargs
        assert start_kwargs["trace_id"] == trace_id

    def test_timed_block_trace_id_not_overridden(self) -> None:
        """Test that explicit trace_id is not overridden by context."""
        mock_logger = Mock()
        context_trace_id = "context-trace-123"
        explicit_trace_id = "explicit-trace-456"

        # Set trace_id in context
        token = _PROVIDE_CONTEXT_TRACE_ID.set(context_trace_id)
        try:
            with timed_block(mock_logger, "test_operation", trace_id=explicit_trace_id):
                pass
        finally:
            _PROVIDE_CONTEXT_TRACE_ID.reset(token)

        # Check that explicit trace_id is used, not context one
        start_call = mock_logger.debug.call_args
        start_kwargs = start_call[1]
        assert "trace_id" in start_kwargs
        assert start_kwargs["trace_id"] == explicit_trace_id

    def test_timed_block_no_trace_id(self) -> None:
        """Test timed_block without trace_id in context."""
        mock_logger = Mock()

        # Ensure no trace_id in context
        token = _PROVIDE_CONTEXT_TRACE_ID.set(None)
        try:
            with timed_block(mock_logger, "test_operation"):
                pass
        finally:
            _PROVIDE_CONTEXT_TRACE_ID.reset(token)

        # Check that no trace_id is added
        start_call = mock_logger.debug.call_args
        start_kwargs = start_call[1]
        assert "trace_id" not in start_kwargs

    def test_timed_block_context_modification(self) -> None:
        """Test that context modifications are reflected in final log."""
        mock_logger = Mock()

        with timed_block(mock_logger, "test_operation") as ctx:
            ctx["step"] = "started"
            time.sleep(0.01)
            ctx["step"] = "processing"
            ctx["items_processed"] = 42
            ctx["final_step"] = "completed"

        # Check that all context modifications are in final log
        completion_call = mock_logger.info.call_args
        completion_kwargs = completion_call[1]
        assert "step" in completion_kwargs
        assert completion_kwargs["step"] == "processing"  # Last value set
        assert "items_processed" in completion_kwargs
        assert completion_kwargs["items_processed"] == 42
        assert "final_step" in completion_kwargs
        assert completion_kwargs["final_step"] == "completed"

    def test_timed_block_duration_precision(self) -> None:
        """Test that duration is rounded to 3 decimal places."""
        mock_logger = Mock()

        with patch("time.perf_counter", side_effect=[1.123456789, 2.987654321]):
            with timed_block(mock_logger, "test_operation"):
                pass

        completion_call = mock_logger.info.call_args
        completion_kwargs = completion_call[1]
        assert "duration_seconds" in completion_kwargs
        # 2.987654321 - 1.123456789 = 1.864197532, rounded to 3 places = 1.864
        assert completion_kwargs["duration_seconds"] == 1.864

    def test_timed_block_exception_duration_precision(self) -> None:
        """Test that duration is rounded to 3 decimal places on exception."""
        mock_logger = Mock()

        with patch("time.perf_counter", side_effect=[1.0, 1.5678901]), pytest.raises(RuntimeError):
            with timed_block(mock_logger, "test_operation"):
                raise RuntimeError("test error")

        error_call = mock_logger.error.call_args
        error_kwargs = error_call[1]
        assert "duration_seconds" in error_kwargs
        # 1.5678901 - 1.0 = 0.5678901, rounded to 3 places = 0.568
        assert error_kwargs["duration_seconds"] == 0.568

    def test_timed_block_empty_context(self) -> None:
        """Test timed_block with no additional context."""
        mock_logger = Mock()

        with timed_block(mock_logger, "simple_operation"):
            pass

        # Should work with minimal setup
        assert mock_logger.debug.call_count == 1
        assert mock_logger.info.call_count == 1

        completion_call = mock_logger.info.call_args
        completion_kwargs = completion_call[1]
        assert "duration_seconds" in completion_kwargs
        assert "outcome" in completion_kwargs
        assert completion_kwargs["outcome"] == "success"

    def test_timed_block_complex_exception(self) -> None:
        """Test timed_block with complex exception types."""
        mock_logger = Mock()

        class CustomError(Exception):
            def __init__(self, message: str, code: int) -> None:
                super().__init__(message)
                self.code = code

        with pytest.raises(CustomError), timed_block(mock_logger, "test_operation"):
            raise CustomError("Custom error message", 404)

        error_call = mock_logger.error.call_args
        error_kwargs = error_call[1]
        assert error_kwargs["error.type"] == "CustomError"
        assert error_kwargs["error.message"] == "Custom error message"


class TestContextVariable:
    """Test the context variable functionality."""

    def test_context_var_default(self) -> None:
        """Test that context variable has correct default."""
        # Reset to ensure clean state
        current_value = _PROVIDE_CONTEXT_TRACE_ID.get()
        assert current_value is None

    def test_context_var_set_and_get(self) -> None:
        """Test setting and getting context variable."""
        trace_id = "test-trace-123"
        token = _PROVIDE_CONTEXT_TRACE_ID.set(trace_id)

        try:
            retrieved_value = _PROVIDE_CONTEXT_TRACE_ID.get()
            assert retrieved_value == trace_id
        finally:
            _PROVIDE_CONTEXT_TRACE_ID.reset(token)

        # Should be back to default after reset
        assert _PROVIDE_CONTEXT_TRACE_ID.get() is None

    def test_context_var_isolation(self) -> None:
        """Test that context variable changes are isolated."""
        # Initial state
        assert _PROVIDE_CONTEXT_TRACE_ID.get() is None

        # Set value in one context
        token1 = _PROVIDE_CONTEXT_TRACE_ID.set("trace-1")
        try:
            assert _PROVIDE_CONTEXT_TRACE_ID.get() == "trace-1"

            # Set different value in nested context
            token2 = _PROVIDE_CONTEXT_TRACE_ID.set("trace-2")
            try:
                assert _PROVIDE_CONTEXT_TRACE_ID.get() == "trace-2"
            finally:
                _PROVIDE_CONTEXT_TRACE_ID.reset(token2)

            # Should be back to first value
            assert _PROVIDE_CONTEXT_TRACE_ID.get() == "trace-1"
        finally:
            _PROVIDE_CONTEXT_TRACE_ID.reset(token1)

        # Should be back to default
        assert _PROVIDE_CONTEXT_TRACE_ID.get() is None


class TestModuleConstants:
    """Test module-level constants and exports."""

    def test_context_var_name(self) -> None:
        """Test that context variable has correct name."""
        assert _PROVIDE_CONTEXT_TRACE_ID.name == "foundation_context_trace_id"

    def test_module_exports(self) -> None:
        """Test that expected functions are importable."""
        # These should be importable from the module
        from provide.foundation.utils.timing import _PROVIDE_CONTEXT_TRACE_ID, timed_block

        assert callable(timed_block)
        assert isinstance(_PROVIDE_CONTEXT_TRACE_ID, contextvars.ContextVar)


class TestTimedBlockIntegration:
    """Test timed_block in integration scenarios."""

    def test_nested_timed_blocks(self) -> None:
        """Test nested timed_block calls."""
        mock_logger = Mock()

        with timed_block(mock_logger, "outer_operation") as outer_ctx:
            outer_ctx["step"] = "outer_start"

            with timed_block(mock_logger, "inner_operation") as inner_ctx:
                inner_ctx["step"] = "inner"
                time.sleep(0.01)

            outer_ctx["step"] = "outer_end"

        # Should have 4 log calls total (2 debug, 2 info)
        assert mock_logger.debug.call_count == 2
        assert mock_logger.info.call_count == 2

        # Both operations should complete successfully
        info_calls = mock_logger.info.call_args_list
        assert "outer_operation completed" in info_calls[1][0]
        assert "inner_operation completed" in info_calls[0][0]

    def test_timed_block_with_trace_propagation(self) -> None:
        """Test trace_id propagation across nested operations."""
        mock_logger = Mock()
        trace_id = "propagated-trace-123"

        token = _PROVIDE_CONTEXT_TRACE_ID.set(trace_id)
        try:
            with timed_block(mock_logger, "operation_1"), timed_block(mock_logger, "operation_2"):
                pass
        finally:
            _PROVIDE_CONTEXT_TRACE_ID.reset(token)

        # All operations should have the same trace_id
        debug_calls = mock_logger.debug.call_args_list
        for call in debug_calls:
            assert "trace_id" in call[1]
            assert call[1]["trace_id"] == trace_id


# 🧱🏗️🔚
