#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for logger OTLP helpers.

Tests all functions in logger/otlp/helpers.py including trace context
extraction, endpoint building, header construction, and attribute normalization."""

from __future__ import annotations

import json
from typing import Any

from provide.testkit.mocking import Mock, patch
import pytest

# Skip all tests in this module if opentelemetry is not installed
pytest.importorskip("opentelemetry")

from provide.foundation.logger.otlp.helpers import (
    add_trace_context_to_attributes,
    build_otlp_endpoint,
    build_otlp_headers,
    extract_trace_context,
    normalize_attributes,
)


class TestExtractTraceContext:
    """Tests for extract_trace_context function."""

    @patch("opentelemetry.trace.get_current_span")
    def test_extract_with_valid_span(self, mock_get_span: Mock) -> None:
        """Test extracting trace context from valid recording span."""
        span = Mock()
        span.is_recording.return_value = True
        span_context = Mock()
        span_context.is_valid = True
        span_context.trace_id = 0x1234567890ABCDEF1234567890ABCDEF
        span_context.span_id = 0xFEDCBA9876543210
        span.get_span_context.return_value = span_context
        mock_get_span.return_value = span

        result = extract_trace_context()

        assert result is not None
        assert result["trace_id"] == "1234567890abcdef1234567890abcdef"
        assert result["span_id"] == "fedcba9876543210"

    @patch("opentelemetry.trace.get_current_span")
    def test_extract_without_span(self, mock_get_span: Mock) -> None:
        """Test that None is returned when no span is available."""
        mock_get_span.return_value = None

        result = extract_trace_context()

        assert result is None

    @patch("opentelemetry.trace.get_current_span")
    def test_extract_with_non_recording_span(self, mock_get_span: Mock) -> None:
        """Test that None is returned when span is not recording."""
        span = Mock()
        span.is_recording.return_value = False
        mock_get_span.return_value = span

        result = extract_trace_context()

        assert result is None

    @patch("opentelemetry.trace.get_current_span")
    def test_extract_with_invalid_span_context(self, mock_get_span: Mock) -> None:
        """Test that None is returned when span context is invalid."""
        span = Mock()
        span.is_recording.return_value = True
        span_context = Mock()
        span_context.is_valid = False
        span.get_span_context.return_value = span_context
        mock_get_span.return_value = span

        result = extract_trace_context()

        assert result is None

    @patch("opentelemetry.trace.get_current_span", side_effect=ImportError)
    def test_extract_without_opentelemetry(self, mock_get_span: Mock) -> None:
        """Test that None is returned when OpenTelemetry is not available."""
        result = extract_trace_context()

        assert result is None

    @patch("opentelemetry.trace.get_current_span")
    def test_extract_formats_ids_correctly(self, mock_get_span: Mock) -> None:
        """Test that trace and span IDs are formatted as hex strings."""
        span = Mock()
        span.is_recording.return_value = True
        span_context = Mock()
        span_context.is_valid = True
        # Test with specific values to verify formatting
        span_context.trace_id = 0xABCDEF1234567890ABCDEF1234567890
        span_context.span_id = 0x1234567890ABCDEF
        span.get_span_context.return_value = span_context
        mock_get_span.return_value = span

        result = extract_trace_context()

        assert result is not None
        # Trace ID should be 32 hex chars (lowercase)
        assert result["trace_id"] == "abcdef1234567890abcdef1234567890"
        assert len(result["trace_id"]) == 32
        # Span ID should be 16 hex chars (lowercase)
        assert result["span_id"] == "1234567890abcdef"
        assert len(result["span_id"]) == 16


class TestAddTraceContextToAttributes:
    """Tests for add_trace_context_to_attributes function."""

    @patch("provide.foundation.logger.otlp.helpers.extract_trace_context")
    def test_add_context_with_valid_context(self, mock_extract: Mock) -> None:
        """Test adding trace context when context is available."""
        mock_extract.return_value = {
            "trace_id": "abc123",
            "span_id": "def456",
        }

        attributes: dict[str, Any] = {"existing": "value"}
        add_trace_context_to_attributes(attributes)

        assert attributes["trace_id"] == "abc123"
        assert attributes["span_id"] == "def456"
        assert attributes["existing"] == "value"

    @patch("provide.foundation.logger.otlp.helpers.extract_trace_context")
    def test_add_context_without_context(self, mock_extract: Mock) -> None:
        """Test that attributes are unchanged when no context is available."""
        mock_extract.return_value = None

        attributes: dict[str, Any] = {"existing": "value"}
        add_trace_context_to_attributes(attributes)

        assert "trace_id" not in attributes
        assert "span_id" not in attributes
        assert attributes["existing"] == "value"

    @patch("provide.foundation.logger.otlp.helpers.extract_trace_context")
    def test_add_context_to_empty_dict(self, mock_extract: Mock) -> None:
        """Test adding trace context to empty attributes dict."""
        mock_extract.return_value = {
            "trace_id": "trace123",
            "span_id": "span456",
        }

        attributes: dict[str, Any] = {}
        add_trace_context_to_attributes(attributes)

        assert attributes == {
            "trace_id": "trace123",
            "span_id": "span456",
        }

    @patch("provide.foundation.logger.otlp.helpers.extract_trace_context")
    def test_add_context_modifies_in_place(self, mock_extract: Mock) -> None:
        """Test that function modifies attributes dict in place."""
        mock_extract.return_value = {
            "trace_id": "trace",
            "span_id": "span",
        }

        original_dict: dict[str, Any] = {"key": "value"}
        attributes = original_dict

        add_trace_context_to_attributes(attributes)

        # Should be the same object (in-place modification)
        assert attributes is original_dict
        assert original_dict["trace_id"] == "trace"


class TestBuildOtlpEndpoint:
    """Tests for build_otlp_endpoint function."""

    def test_build_endpoint_default_logs(self) -> None:
        """Test building endpoint with default signal type (logs)."""
        endpoint = build_otlp_endpoint("https://api.example.com")

        assert endpoint == "https://api.example.com/v1/logs"

    def test_build_endpoint_traces(self) -> None:
        """Test building endpoint for traces signal type."""
        endpoint = build_otlp_endpoint("https://api.example.com", "traces")

        assert endpoint == "https://api.example.com/v1/traces"

    def test_build_endpoint_metrics(self) -> None:
        """Test building endpoint for metrics signal type."""
        endpoint = build_otlp_endpoint("https://api.example.com", "metrics")

        assert endpoint == "https://api.example.com/v1/metrics"

    def test_build_endpoint_with_trailing_slash(self) -> None:
        """Test that trailing slashes are handled correctly."""
        endpoint = build_otlp_endpoint("https://api.example.com/", "logs")

        assert endpoint == "https://api.example.com/v1/logs"

    def test_build_endpoint_idempotent(self) -> None:
        """Test that function is idempotent (won't double-add paths)."""
        endpoint = build_otlp_endpoint(
            "https://api.example.com/v1/logs",
            "logs",
        )

        assert endpoint == "https://api.example.com/v1/logs"

    def test_build_endpoint_idempotent_traces(self) -> None:
        """Test idempotency for traces endpoint."""
        endpoint = build_otlp_endpoint(
            "https://api.example.com/v1/traces",
            "traces",
        )

        assert endpoint == "https://api.example.com/v1/traces"

    def test_build_endpoint_localhost(self) -> None:
        """Test building endpoint with localhost."""
        endpoint = build_otlp_endpoint("http://localhost:4318", "logs")

        assert endpoint == "http://localhost:4318/v1/logs"

    def test_build_endpoint_with_port(self) -> None:
        """Test building endpoint with custom port."""
        endpoint = build_otlp_endpoint("https://api.example.com:8080", "traces")

        assert endpoint == "https://api.example.com:8080/v1/traces"

    def test_build_endpoint_with_path(self) -> None:
        """Test building endpoint when base URL has existing path."""
        endpoint = build_otlp_endpoint(
            "https://api.example.com/otlp",
            "logs",
        )

        assert endpoint == "https://api.example.com/otlp/v1/logs"

    def test_build_endpoint_custom_signal_type(self) -> None:
        """Test building endpoint with custom signal type."""
        endpoint = build_otlp_endpoint(
            "https://api.example.com",
            "custom-signal",
        )

        assert endpoint == "https://api.example.com/v1/custom-signal"


class TestBuildOtlpHeaders:
    """Tests for build_otlp_headers function."""

    def test_build_headers_default(self) -> None:
        """Test building headers with default values."""
        headers = build_otlp_headers()

        assert headers == {"Content-Type": "application/x-protobuf"}

    def test_build_headers_with_auth_token(self) -> None:
        """Test building headers with bearer token authentication."""
        headers = build_otlp_headers(auth_token="secret-token-123")

        assert headers["Content-Type"] == "application/x-protobuf"
        assert headers["Authorization"] == "Bearer secret-token-123"

    def test_build_headers_with_base_headers(self) -> None:
        """Test building headers with base headers included."""
        base_headers = {
            "X-Custom-Header": "custom-value",
            "X-Another-Header": "another-value",
        }

        headers = build_otlp_headers(base_headers=base_headers)

        assert headers["Content-Type"] == "application/x-protobuf"
        assert headers["X-Custom-Header"] == "custom-value"
        assert headers["X-Another-Header"] == "another-value"

    def test_build_headers_with_base_and_auth(self) -> None:
        """Test building headers with both base headers and auth token."""
        base_headers = {"X-Custom": "value"}

        headers = build_otlp_headers(
            base_headers=base_headers,
            auth_token="token123",
        )

        assert headers["Content-Type"] == "application/x-protobuf"
        assert headers["Authorization"] == "Bearer token123"
        assert headers["X-Custom"] == "value"

    def test_build_headers_preserves_custom_content_type(self) -> None:
        """Test that custom Content-Type in base headers is preserved."""
        base_headers = {"Content-Type": "application/json"}

        headers = build_otlp_headers(base_headers=base_headers)

        # Should preserve custom Content-Type (setdefault behavior)
        assert headers["Content-Type"] == "application/json"

    def test_build_headers_empty_base_headers(self) -> None:
        """Test building headers with empty base headers dict."""
        headers = build_otlp_headers(base_headers={})

        assert headers == {"Content-Type": "application/x-protobuf"}

    def test_build_headers_none_auth_token(self) -> None:
        """Test that None auth token is handled correctly."""
        headers = build_otlp_headers(auth_token=None)

        assert "Authorization" not in headers
        assert headers["Content-Type"] == "application/x-protobuf"


class TestNormalizeAttributes:
    """Tests for normalize_attributes function."""

    def test_normalize_string_values(self) -> None:
        """Test that string values are preserved."""
        attributes = {"key": "value", "another": "string"}

        result = normalize_attributes(attributes)

        assert result == {"key": "value", "another": "string"}

    def test_normalize_numeric_values(self) -> None:
        """Test that numeric values (int, float) are preserved."""
        attributes = {"int_val": 42, "float_val": 3.14, "negative": -10}

        result = normalize_attributes(attributes)

        assert result == {"int_val": 42, "float_val": 3.14, "negative": -10}

    def test_normalize_boolean_values(self) -> None:
        """Test that boolean values are preserved."""
        attributes = {"true_val": True, "false_val": False}

        result = normalize_attributes(attributes)

        assert result == {"true_val": True, "false_val": False}

    def test_normalize_none_values(self) -> None:
        """Test that None values are converted to empty strings."""
        attributes = {"none_val": None, "another_none": None}

        result = normalize_attributes(attributes)

        assert result == {"none_val": "", "another_none": ""}

    def test_normalize_dict_values(self) -> None:
        """Test that dict values are JSON-serialized."""
        attributes = {
            "simple_dict": {"a": 1, "b": 2},
            "nested_dict": {"outer": {"inner": "value"}},
        }

        result = normalize_attributes(attributes)

        assert json.loads(result["simple_dict"]) == {"a": 1, "b": 2}
        assert json.loads(result["nested_dict"]) == {"outer": {"inner": "value"}}

    def test_normalize_list_values(self) -> None:
        """Test that list values are JSON-serialized."""
        attributes = {
            "simple_list": [1, 2, 3],
            "string_list": ["a", "b", "c"],
            "nested_list": [[1, 2], [3, 4]],
        }

        result = normalize_attributes(attributes)

        assert json.loads(result["simple_list"]) == [1, 2, 3]
        assert json.loads(result["string_list"]) == ["a", "b", "c"]
        assert json.loads(result["nested_list"]) == [[1, 2], [3, 4]]

    def test_normalize_mixed_types(self) -> None:
        """Test normalizing attributes with mixed types."""
        attributes = {
            "string": "value",
            "int": 42,
            "float": 3.14,
            "bool": True,
            "none": None,
            "dict": {"key": "value"},
            "list": [1, 2, 3],
        }

        result = normalize_attributes(attributes)

        assert result["string"] == "value"
        assert result["int"] == 42
        assert result["float"] == 3.14
        assert result["bool"] is True
        assert result["none"] == ""
        assert json.loads(result["dict"]) == {"key": "value"}
        assert json.loads(result["list"]) == [1, 2, 3]

    def test_normalize_custom_object(self) -> None:
        """Test that custom objects are converted to strings."""

        class CustomObject:
            def __str__(self) -> str:
                return "custom-object-str"

        attributes = {"custom": CustomObject()}

        result = normalize_attributes(attributes)

        assert result["custom"] == "custom-object-str"

    def test_normalize_empty_dict(self) -> None:
        """Test normalizing empty attributes dict."""
        result = normalize_attributes({})

        assert result == {}

    def test_normalize_returns_new_dict(self) -> None:
        """Test that function returns new dict (doesn't modify input)."""
        original = {"key": "value", "dict": {"a": 1}}

        result = normalize_attributes(original)

        # Should be different objects
        assert result is not original
        # Original should be unchanged
        assert original["dict"] == {"a": 1}

    def test_normalize_non_serializable_dict(self) -> None:
        """Test handling of dict with non-JSON-serializable values."""

        class NonSerializable:
            def __str__(self) -> str:
                return "non-serializable"

        # Create dict that can't be JSON serialized
        attributes = {"bad_dict": {"key": NonSerializable()}}

        result = normalize_attributes(attributes)

        # Should fall back to str() conversion
        assert isinstance(result["bad_dict"], str)
        assert "non-serializable" in result["bad_dict"] or "key" in result["bad_dict"]

    def test_normalize_preserves_primitives(self) -> None:
        """Test that primitive values are not converted unnecessarily."""
        attributes = {
            "str": "test",
            "int": 123,
            "float": 45.67,
            "bool_true": True,
            "bool_false": False,
        }

        result = normalize_attributes(attributes)

        # Values should be identical (not just equal)
        assert result["str"] is attributes["str"]
        assert result["int"] is attributes["int"]
        assert result["float"] is attributes["float"]
        assert result["bool_true"] is attributes["bool_true"]
        assert result["bool_false"] is attributes["bool_false"]


# 🧱🏗️🔚
