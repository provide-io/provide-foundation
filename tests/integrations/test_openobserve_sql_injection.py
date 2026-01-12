#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""SQL injection security tests for OpenObserve integration.

These tests verify that all SQL query construction properly sanitizes inputs
and prevents SQL injection attacks."""

from __future__ import annotations

import pytest

from provide.foundation.integrations.openobserve.search import (
    _sanitize_log_level,
    _sanitize_service_name,
    _sanitize_stream_name,
    _sanitize_trace_id,
    aggregate_by_level,
    search_by_level,
    search_by_service,
    search_by_trace_id,
)


class TestSanitization:
    """Test input sanitization functions."""

    def test_sanitize_stream_name_valid(self) -> None:
        """Test valid stream names pass sanitization."""
        assert _sanitize_stream_name("default") == "default"
        assert _sanitize_stream_name("test_stream") == "test_stream"
        assert _sanitize_stream_name("logs123") == "logs123"
        assert _sanitize_stream_name("ABC_def_123") == "ABC_def_123"

    def test_sanitize_stream_name_injection_attempts(self) -> None:
        """Test SQL injection attempts are blocked."""
        # SQL comment injection
        with pytest.raises(ValueError, match="Invalid stream name"):
            _sanitize_stream_name("default'; --")

        # UNION injection
        with pytest.raises(ValueError, match="Invalid stream name"):
            _sanitize_stream_name("default' UNION SELECT * FROM users--")

        # Special characters
        with pytest.raises(ValueError, match="Invalid stream name"):
            _sanitize_stream_name("default; DROP TABLE logs;")

        # Space character (not allowed)
        with pytest.raises(ValueError, match="Invalid stream name"):
            _sanitize_stream_name("default test")

        # Quote characters
        with pytest.raises(ValueError, match="Invalid stream name"):
            _sanitize_stream_name("default'OR'1'='1")

        # Parentheses
        with pytest.raises(ValueError, match="Invalid stream name"):
            _sanitize_stream_name("default()")

        # Backticks
        with pytest.raises(ValueError, match="Invalid stream name"):
            _sanitize_stream_name("`default`")

    def test_sanitize_trace_id_valid(self) -> None:
        """Test valid trace IDs pass sanitization."""
        assert _sanitize_trace_id("abc123def456") == "abc123def456"
        assert _sanitize_trace_id("ABCDEF0123456789") == "ABCDEF0123456789"
        assert (
            _sanitize_trace_id("12345678-1234-1234-1234-123456789012")
            == "12345678-1234-1234-1234-123456789012"
        )
        assert (
            _sanitize_trace_id("a1b2c3d4-e5f6-a7b8-c9d0-e1f2a3b4c5d6")
            == "a1b2c3d4-e5f6-a7b8-c9d0-e1f2a3b4c5d6"
        )

    def test_sanitize_trace_id_injection_attempts(self) -> None:
        """Test SQL injection attempts in trace ID are blocked."""
        # SQL comment
        with pytest.raises(ValueError, match="Invalid trace_id format"):
            _sanitize_trace_id("abc'; --")

        # UNION injection
        with pytest.raises(ValueError, match="Invalid trace_id format"):
            _sanitize_trace_id("abc' UNION SELECT")

        # Special characters
        with pytest.raises(ValueError, match="Invalid trace_id format"):
            _sanitize_trace_id("abc; DROP")

        # Invalid hex characters
        with pytest.raises(ValueError, match="Invalid trace_id format"):
            _sanitize_trace_id("xyz123")

        with pytest.raises(ValueError, match="Invalid trace_id format"):
            _sanitize_trace_id("abc@123")

    def test_sanitize_log_level_valid(self) -> None:
        """Test valid log levels pass sanitization."""
        assert _sanitize_log_level("TRACE") == "TRACE"
        assert _sanitize_log_level("DEBUG") == "DEBUG"
        assert _sanitize_log_level("INFO") == "INFO"
        assert _sanitize_log_level("WARNING") == "WARNING"
        assert _sanitize_log_level("ERROR") == "ERROR"
        assert _sanitize_log_level("CRITICAL") == "CRITICAL"

    def test_sanitize_log_level_injection_attempts(self) -> None:
        """Test SQL injection attempts in log level are blocked."""
        # Not in whitelist
        with pytest.raises(ValueError, match="Invalid log level"):
            _sanitize_log_level("ERROR'; --")

        with pytest.raises(ValueError, match="Invalid log level"):
            _sanitize_log_level("' OR '1'='1")

        with pytest.raises(ValueError, match="Invalid log level"):
            _sanitize_log_level("INVALID")

        with pytest.raises(ValueError, match="Invalid log level"):
            _sanitize_log_level("error")  # lowercase not allowed

    def test_sanitize_service_name_valid(self) -> None:
        """Test valid service names pass sanitization."""
        assert _sanitize_service_name("auth-service") == "auth-service"
        assert _sanitize_service_name("api_gateway") == "api_gateway"
        assert _sanitize_service_name("web.app") == "web.app"
        assert _sanitize_service_name("service-1.2.3") == "service-1.2.3"
        assert _sanitize_service_name("My-Service_v2.0") == "My-Service_v2.0"

    def test_sanitize_service_name_injection_attempts(self) -> None:
        """Test SQL injection attempts in service name are blocked."""
        # SQL comment
        with pytest.raises(ValueError, match="Invalid service name"):
            _sanitize_service_name("auth'; --")

        # UNION injection
        with pytest.raises(ValueError, match="Invalid service name"):
            _sanitize_service_name("auth' UNION SELECT * FROM passwords")

        # Special characters
        with pytest.raises(ValueError, match="Invalid service name"):
            _sanitize_service_name("auth; DROP TABLE")

        # Quotes
        with pytest.raises(ValueError, match="Invalid service name"):
            _sanitize_service_name("auth'OR'1'='1")

        # Spaces (not allowed)
        with pytest.raises(ValueError, match="Invalid service name"):
            _sanitize_service_name("auth service")

        # Parentheses
        with pytest.raises(ValueError, match="Invalid service name"):
            _sanitize_service_name("auth()")


class TestSQLQueryConstruction:
    """Test that SQL queries are safely constructed."""

    @pytest.mark.asyncio
    async def test_search_by_trace_id_safe_construction(self) -> None:
        """Test that search_by_trace_id constructs safe SQL."""
        # This should raise during sanitization before SQL construction
        with pytest.raises(ValueError, match="Invalid trace_id format"):
            await search_by_trace_id(
                trace_id="abc'; DROP TABLE logs;--",
                stream="default",
                client=None,  # Won't reach client call due to sanitization
            )

    @pytest.mark.asyncio
    async def test_search_by_level_safe_construction(self) -> None:
        """Test that search_by_level constructs safe SQL."""
        # This should raise during sanitization
        with pytest.raises(ValueError, match="Invalid log level"):
            await search_by_level(
                level="ERROR'; DELETE FROM logs;--",
                stream="default",
                client=None,
            )

    @pytest.mark.asyncio
    async def test_search_by_service_safe_construction(self) -> None:
        """Test that search_by_service constructs safe SQL."""
        # This should raise during sanitization
        with pytest.raises(ValueError, match="Invalid service name"):
            await search_by_service(
                service="auth'; DROP TABLE users;--",
                stream="default",
                client=None,
            )

    @pytest.mark.asyncio
    async def test_aggregate_by_level_safe_construction(self) -> None:
        """Test that aggregate_by_level constructs safe SQL."""
        # This should raise during sanitization
        with pytest.raises(ValueError, match="Invalid stream name"):
            await aggregate_by_level(
                stream="default'; DROP TABLE logs;--",
                client=None,
            )


class TestMultipleInjectionVectors:
    """Test multiple parameters with injection attempts."""

    @pytest.mark.asyncio
    async def test_combined_injection_attempts_blocked(self) -> None:
        """Test multiple injection vectors are all blocked."""
        # Stream injection
        with pytest.raises(ValueError, match="Invalid stream name"):
            await search_by_trace_id(
                trace_id="abc123",
                stream="default'; DROP TABLE logs;--",
                client=None,
            )

        # Trace ID injection
        with pytest.raises(ValueError, match="Invalid trace_id format"):
            await search_by_trace_id(
                trace_id="abc'; SELECT * FROM users;--",
                stream="default",
                client=None,
            )

    @pytest.mark.asyncio
    async def test_encoded_injection_attempts_blocked(self) -> None:
        """Test URL-encoded and escaped injection attempts are blocked."""
        # URL-encoded apostrophe
        with pytest.raises(ValueError, match="Invalid stream name"):
            await search_by_level(
                level="ERROR",
                stream="default%27%3B--",
                client=None,
            )

        # Escaped characters
        with pytest.raises(ValueError, match="Invalid service name"):
            await search_by_service(
                service="auth\\\\'--",
                stream="default",
                client=None,
            )

    @pytest.mark.asyncio
    async def test_unicode_injection_attempts_blocked(self) -> None:
        """Test unicode and special character injection attempts are blocked."""
        # Unicode apostrophe
        with pytest.raises(ValueError, match="Invalid stream name"):
            await search_by_level(
                level="ERROR",
                stream="default\u0027; DROP",
                client=None,
            )

        # Null byte
        with pytest.raises(ValueError, match="Invalid service name"):
            await search_by_service(
                service="auth\x00; DROP",
                stream="default",
                client=None,
            )


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_strings(self) -> None:
        """Test empty strings are rejected."""
        with pytest.raises(ValueError, match="Invalid stream name"):
            _sanitize_stream_name("")

        with pytest.raises(ValueError, match="Invalid trace_id format"):
            _sanitize_trace_id("")

        with pytest.raises(ValueError, match="Invalid service name"):
            _sanitize_service_name("")

    def test_very_long_inputs(self) -> None:
        """Test very long inputs are handled."""
        # Valid long stream name
        long_valid = "a" * 1000
        assert _sanitize_stream_name(long_valid) == long_valid

        # Long invalid stream name
        long_invalid = "a" * 999 + "'"
        with pytest.raises(ValueError, match="Invalid stream name"):
            _sanitize_stream_name(long_invalid)

    def test_case_sensitivity(self) -> None:
        """Test case sensitivity in validation."""
        # Stream names are case-sensitive and allow both cases
        assert _sanitize_stream_name("Default") == "Default"
        assert _sanitize_stream_name("DEFAULT") == "DEFAULT"

        # Log levels must be exact case
        with pytest.raises(ValueError, match="Invalid log level"):
            _sanitize_log_level("error")  # lowercase

        with pytest.raises(ValueError, match="Invalid log level"):
            _sanitize_log_level("Error")  # mixed case


__all__ = [
    "TestEdgeCases",
    "TestMultipleInjectionVectors",
    "TestSQLQueryConstruction",
    "TestSanitization",
]

# 🧱🏗️🔚
