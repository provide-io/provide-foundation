#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for provide.foundation.errors.context module."""

from __future__ import annotations

from datetime import datetime

from provide.testkit import FoundationTestCase

from provide.foundation.errors.auth import AuthenticationError
from provide.foundation.errors.base import FoundationError
from provide.foundation.errors.config import ValidationError
from provide.foundation.errors.context import (
    ErrorCategory,
    ErrorContext,
    ErrorSeverity,
    capture_error_context,
)
from provide.foundation.errors.integration import IntegrationError, NetworkError


class TestErrorSeverity(FoundationTestCase):
    """Test ErrorSeverity enum."""

    def test_severity_values(self) -> None:
        """Test severity enum values."""
        assert ErrorSeverity.LOW.value == "low"
        assert ErrorSeverity.MEDIUM.value == "medium"
        assert ErrorSeverity.HIGH.value == "high"
        assert ErrorSeverity.CRITICAL.value == "critical"

    def test_severity_comparison(self) -> None:
        """Test that severities are strings."""
        assert ErrorSeverity.LOW == "low"
        assert ErrorSeverity.HIGH.value == "high"


class TestErrorCategory(FoundationTestCase):
    """Test ErrorCategory enum."""

    def test_category_values(self) -> None:
        """Test category enum values."""
        assert ErrorCategory.USER.value == "user"
        assert ErrorCategory.SYSTEM.value == "system"
        assert ErrorCategory.EXTERNAL.value == "external"

    def test_category_comparison(self) -> None:
        """Test that categories are strings."""
        assert ErrorCategory.USER.value == "user"
        assert ErrorCategory.SYSTEM.value == "system"


class TestErrorContext(FoundationTestCase):
    """Test ErrorContext class."""

    def test_default_creation(self) -> None:
        """Test creating ErrorContext with defaults."""
        ctx = ErrorContext()

        assert isinstance(ctx.timestamp, datetime)
        assert ctx.severity == ErrorSeverity.MEDIUM
        assert ctx.category == ErrorCategory.SYSTEM
        assert ctx.metadata == {}
        assert ctx.tags == set()
        assert ctx.trace_id is None
        assert ctx.span_id is None

    def test_creation_with_parameters(self) -> None:
        """Test creating ErrorContext with parameters."""
        now = datetime.now()
        ctx = ErrorContext(
            timestamp=now,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.EXTERNAL,
            trace_id="trace_123",
            span_id="span_456",
        )

        assert ctx.timestamp == now
        assert ctx.severity == ErrorSeverity.HIGH
        assert ctx.category == ErrorCategory.EXTERNAL
        assert ctx.trace_id == "trace_123"
        assert ctx.span_id == "span_456"

    def test_add_namespace(self) -> None:
        """Test adding namespaced metadata."""
        ctx = ErrorContext()

        result = ctx.add_namespace("aws", {"region": "us-east-1", "account": "123"})

        assert result is ctx  # Returns self for chaining
        assert ctx.metadata["aws"] == {"region": "us-east-1", "account": "123"}

    def test_add_namespace_chaining(self) -> None:
        """Test chaining namespace additions."""
        ctx = ErrorContext()

        ctx.add_namespace("terraform", {"provider": "aws"}).add_namespace(
            "http",
            {"status": 500, "method": "POST"},
        )

        assert ctx.metadata["terraform"] == {"provider": "aws"}
        assert ctx.metadata["http"] == {"status": 500, "method": "POST"}

    def test_update_namespace(self) -> None:
        """Test updating existing namespace."""
        ctx = ErrorContext()

        ctx.add_namespace("aws", {"region": "us-east-1"})
        ctx.update_namespace("aws", {"account": "123", "region": "us-west-2"})

        assert ctx.metadata["aws"]["region"] == "us-west-2"  # Updated
        assert ctx.metadata["aws"]["account"] == "123"  # Added

    def test_update_namespace_creates_if_missing(self) -> None:
        """Test that update_namespace creates namespace if missing."""
        ctx = ErrorContext()

        ctx.update_namespace("new", {"key": "value"})

        assert ctx.metadata["new"] == {"key": "value"}

    def test_get_namespace(self) -> None:
        """Test retrieving namespace metadata."""
        ctx = ErrorContext()
        ctx.add_namespace("test", {"data": "value"})

        assert ctx.get_namespace("test") == {"data": "value"}
        assert ctx.get_namespace("missing") is None

    def test_add_tag(self) -> None:
        """Test adding a single tag."""
        ctx = ErrorContext()

        result = ctx.add_tag("production")

        assert result is ctx  # Returns self
        assert "production" in ctx.tags

    def test_add_tags(self) -> None:
        """Test adding multiple tags."""
        ctx = ErrorContext()

        result = ctx.add_tags("production", "critical", "database")

        assert result is ctx
        assert ctx.tags == {"production", "critical", "database"}

    def test_tags_are_unique(self) -> None:
        """Test that tags are unique (set behavior)."""
        ctx = ErrorContext()

        ctx.add_tag("test")
        ctx.add_tag("test")
        ctx.add_tags("test", "other")

        assert ctx.tags == {"test", "other"}

    def test_to_dict_basic(self) -> None:
        """Test converting to dictionary."""
        now = datetime(2024, 1, 1, 12, 0, 0)
        ctx = ErrorContext(
            timestamp=now,
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.EXTERNAL,
        )

        result = ctx.to_dict()

        assert result["timestamp"] == "2024-01-01T12:00:00"
        assert result["severity"] == "high"
        assert result["category"] == "external"

    def test_to_dict_with_tracing(self) -> None:
        """Test to_dict includes tracing info."""
        ctx = ErrorContext(trace_id="trace_123", span_id="span_456")

        result = ctx.to_dict()

        assert result["trace_id"] == "trace_123"
        assert result["span_id"] == "span_456"

    def test_to_dict_flattens_metadata(self) -> None:
        """Test that to_dict flattens namespaced metadata."""
        ctx = ErrorContext()
        ctx.add_namespace("aws", {"region": "us-east-1", "account": "123"})
        ctx.add_namespace("http", {"status": 500, "method": "POST"})

        result = ctx.to_dict()

        assert result["aws.region"] == "us-east-1"
        assert result["aws.account"] == "123"
        assert result["http.status"] == 500
        assert result["http.method"] == "POST"

    def test_to_dict_includes_tags(self) -> None:
        """Test that to_dict includes sorted tags."""
        ctx = ErrorContext()
        ctx.add_tags("zebra", "alpha", "beta")

        result = ctx.to_dict()

        assert result["tags"] == ["alpha", "beta", "zebra"]  # Sorted

    def test_to_dict_excludes_empty_tags(self) -> None:
        """Test that empty tags are not included."""
        ctx = ErrorContext()

        result = ctx.to_dict()

        assert "tags" not in result

    def test_to_logging_context(self) -> None:
        """Test to_logging_context method."""
        ctx = ErrorContext()
        ctx.add_namespace("test", {"key": "value"})

        # Should be same as to_dict
        assert ctx.to_logging_context() == ctx.to_dict()

    def test_to_terraform_diagnostic(self) -> None:
        """Test conversion to Terraform diagnostic format."""
        ctx = ErrorContext(severity=ErrorSeverity.HIGH)
        ctx.add_namespace(
            "terraform",
            {
                "provider": "aws",
                "resource": "aws_instance.example",
                "workspace": "production",
            },
        )
        ctx.add_namespace("aws", {"region": "us-east-1"})

        result = ctx.to_terraform_diagnostic()

        assert result["severity"] == "error"  # HIGH maps to error
        assert result["detail"]["provider"] == "aws"
        assert result["detail"]["resource"] == "aws_instance.example"
        assert result["detail"]["workspace"] == "production"
        assert result["detail"]["aws"] == {"region": "us-east-1"}

    def test_terraform_diagnostic_severity_mapping(self) -> None:
        """Test Terraform diagnostic severity mapping."""
        test_cases = [
            (ErrorSeverity.LOW, "warning"),
            (ErrorSeverity.MEDIUM, "warning"),
            (ErrorSeverity.HIGH, "error"),
            (ErrorSeverity.CRITICAL, "error"),
        ]

        for severity, expected in test_cases:
            ctx = ErrorContext(severity=severity)
            result = ctx.to_terraform_diagnostic()
            assert result["severity"] == expected

    def test_terraform_diagnostic_without_terraform_namespace(self) -> None:
        """Test Terraform diagnostic without terraform namespace."""
        ctx = ErrorContext()
        ctx.add_namespace("other", {"key": "value"})

        result = ctx.to_terraform_diagnostic()

        assert result["detail"]["other"] == {"key": "value"}
        assert "terraform" not in result["detail"]


class TestCaptureErrorContext(FoundationTestCase):
    """Test capture_error_context function."""

    def test_capture_basic_exception(self) -> None:
        """Test capturing context from a basic exception."""
        error = Exception("Test error")

        ctx = capture_error_context(error)

        assert ctx.severity == ErrorSeverity.HIGH  # Default for unknown
        assert ctx.category == ErrorCategory.SYSTEM  # Default
        assert ctx.get_namespace("error") == {
            "type": "Exception",
            "message": "Test error",
        }

    def test_capture_with_severity_override(self) -> None:
        """Test capturing with severity override."""
        error = Exception("Test")

        ctx = capture_error_context(error, severity=ErrorSeverity.LOW)

        assert ctx.severity == ErrorSeverity.LOW

    def test_capture_with_category_override(self) -> None:
        """Test capturing with category override."""
        error = Exception("Test")

        ctx = capture_error_context(error, category=ErrorCategory.EXTERNAL)

        assert ctx.category == ErrorCategory.EXTERNAL

    def test_capture_with_namespaces(self) -> None:
        """Test capturing with additional namespaces."""
        error = Exception("Test")

        ctx = capture_error_context(
            error,
            aws={"region": "us-east-1"},
            http={"status": 500},
        )

        assert ctx.get_namespace("aws") == {"region": "us-east-1"}
        assert ctx.get_namespace("http") == {"status": 500}

    def test_severity_inference_for_value_errors(self) -> None:
        """Test severity inference for value-related errors."""
        errors = [
            (AssertionError("test"), ErrorSeverity.MEDIUM),
            (ValueError("test"), ErrorSeverity.MEDIUM),
            (TypeError("test"), ErrorSeverity.MEDIUM),
        ]

        for error, expected_severity in errors:
            ctx = capture_error_context(error)
            assert ctx.severity == expected_severity

    def test_severity_inference_for_lookup_errors(self) -> None:
        """Test severity inference for lookup errors."""
        errors = [
            (KeyError("test"), ErrorSeverity.LOW),
            (IndexError("test"), ErrorSeverity.LOW),
            (AttributeError("test"), ErrorSeverity.LOW),
        ]

        for error, expected_severity in errors:
            ctx = capture_error_context(error)
            assert ctx.severity == expected_severity

    def test_category_inference_for_user_errors(self) -> None:
        """Test category inference for user-related errors."""
        errors = [
            ValidationError("test"),
            AuthenticationError("test"),
        ]

        for error in errors:
            ctx = capture_error_context(error)
            assert ctx.category == ErrorCategory.USER

    def test_category_inference_for_external_errors(self) -> None:
        """Test category inference for external errors."""
        errors = [
            IntegrationError("test"),
            NetworkError("test"),
        ]

        for error in errors:
            ctx = capture_error_context(error)
            assert ctx.category == ErrorCategory.EXTERNAL

    def test_capture_foundation_error_context(self) -> None:
        """Test capturing context from FoundationError."""
        error = FoundationError("Test error")
        error.add_context("key1", "value1")
        error.add_context("aws.region", "us-east-1")
        error.add_context("http.status", 500)

        ctx = capture_error_context(error)

        # Non-namespaced items go to 'context' namespace
        assert ctx.get_namespace("context") == {"key1": "value1"}

        # Namespaced items are grouped
        assert ctx.get_namespace("aws") == {"region": "us-east-1"}
        assert ctx.get_namespace("http") == {"status": 500}

    def test_capture_foundation_error_merges_namespaces(self) -> None:
        """Test that capture merges with provided namespaces."""
        error = FoundationError("Test")
        error.add_context("aws.region", "us-east-1")

        ctx = capture_error_context(
            error,
            aws={"account": "123"},  # Additional AWS context
        )

        # Should merge both AWS contexts
        assert ctx.get_namespace("aws") == {"region": "us-east-1", "account": "123"}

    def test_capture_complex_namespace_parsing(self) -> None:
        """Test parsing complex namespaced keys."""
        error = FoundationError("Test")
        error.add_context("a.b.c", "deep")
        error.add_context("a.d", "shallow")

        ctx = capture_error_context(error)

        # Only splits on first dot
        assert ctx.get_namespace("a") == {"b.c": "deep", "d": "shallow"}


class TestErrorContextIntegration(FoundationTestCase):
    """Test ErrorContext integration scenarios."""

    def test_full_context_workflow(self) -> None:
        """Test a complete context workflow."""
        # Create context
        ctx = ErrorContext(
            severity=ErrorSeverity.CRITICAL,
            category=ErrorCategory.EXTERNAL,
            trace_id="trace_123",
        )

        # Add various metadata
        ctx.add_namespace("terraform", {"provider": "aws", "version": "5.0.0"})
        ctx.add_namespace(
            "aws",
            {"region": "us-east-1", "error_code": "ThrottlingException"},
        )
        ctx.add_tags("production", "critical", "retry")

        # Convert to dict for logging
        log_data = ctx.to_logging_context()

        assert log_data["severity"] == "critical"
        assert log_data["category"] == "external"
        assert log_data["trace_id"] == "trace_123"
        assert log_data["terraform.provider"] == "aws"
        assert log_data["aws.error_code"] == "ThrottlingException"
        assert "production" in log_data["tags"]

    def test_context_with_error_chain(self) -> None:
        """Test context with error chaining."""
        # Create original error
        original = NetworkError("Connection failed", host="api.example.com")

        # Create wrapper error
        wrapper = IntegrationError(
            "Service unavailable",
            service="user-api",
            cause=original,
        )

        # Capture context
        ctx = capture_error_context(wrapper)

        assert ctx.category == ErrorCategory.EXTERNAL
        assert ctx.get_namespace("error")["type"] == "IntegrationError"


# 🧱🏗️🔚
