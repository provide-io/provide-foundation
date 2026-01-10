#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for logger/processors/sanitization.py module."""

from provide.testkit import FoundationTestCase


class TestSanitizationProcessorCreation(FoundationTestCase):
    """Test sanitization processor creation and configuration."""

    def test_create_processor_all_enabled(self) -> None:
        """Test creating processor with all features enabled."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=True,
            sanitize_dicts=True,
        )

        assert processor is not None
        assert callable(processor)

    def test_create_processor_disabled(self) -> None:
        """Test creating processor with sanitization disabled."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=False,
            mask_patterns=True,
            sanitize_dicts=True,
        )

        # Should still return a processor, but it won't modify data
        assert processor is not None
        assert callable(processor)

    def test_create_processor_only_mask_patterns(self) -> None:
        """Test creating processor with only pattern masking enabled."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=True,
            sanitize_dicts=False,
        )

        assert processor is not None
        assert callable(processor)

    def test_create_processor_only_sanitize_dicts(self) -> None:
        """Test creating processor with only dict sanitization enabled."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=False,
            sanitize_dicts=True,
        )

        assert processor is not None
        assert callable(processor)


class TestSanitizationProcessorBasicBehavior(FoundationTestCase):
    """Test basic sanitization processor behavior."""

    def test_processor_when_disabled(self) -> None:
        """Test processor returns event dict unchanged when disabled."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(enabled=False)
        event_dict = {
            "event": "test",
            "api_key": "sk-1234567890abcdef",
            "password": "secret123",
        }
        original_event_dict = event_dict.copy()

        result = processor(None, "info", event_dict)

        # Should return unchanged
        assert result == original_event_dict

    def test_processor_returns_dict(self) -> None:
        """Test processor returns a dictionary."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(enabled=True)
        event_dict = {"event": "test"}

        result = processor(None, "info", event_dict)

        assert isinstance(result, dict)

    def test_processor_preserves_non_sensitive_data(self) -> None:
        """Test processor preserves non-sensitive data."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(enabled=True)
        event_dict = {
            "event": "test",
            "user_id": 123,
            "timestamp": "2024-01-01",
            "message": "Hello world",
        }

        result = processor(None, "info", event_dict)

        assert result["event"] == "test"
        assert result["user_id"] == 123
        assert result["timestamp"] == "2024-01-01"
        assert result["message"] == "Hello world"


class TestSanitizationProcessorPatternMasking(FoundationTestCase):
    """Test pattern-based secret masking."""

    def test_mask_api_key_pattern_in_string(self) -> None:
        """Test masking API key patterns within strings."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=True,
            sanitize_dicts=False,
        )

        event_dict = {
            "event": "test",
            "message": "Connecting with api_key=sk-1234567890abcdef",
        }

        result = processor(None, "info", event_dict)

        # API key in message should be masked
        assert "api_key=[MASKED]" in result["message"]
        assert "sk-1234567890abcdef" not in result["message"]

    def test_mask_token_pattern_in_string(self) -> None:
        """Test masking token patterns within strings."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=True,
            sanitize_dicts=False,
        )

        event_dict = {
            "event": "test",
            "message": "Using token=abc123def456 for auth",
        }

        result = processor(None, "info", event_dict)

        # Token should be masked
        assert "token=[MASKED]" in result["message"]
        assert "abc123def456" not in result["message"]

    def test_mask_password_pattern_in_string(self) -> None:
        """Test masking password patterns within strings."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=True,
            sanitize_dicts=False,
        )

        event_dict = {
            "event": "test",
            "message": "Logging in with password=secret123",
        }

        result = processor(None, "info", event_dict)

        # Password should be masked
        assert "password=[MASKED]" in result["message"]
        assert "secret123" not in result["message"]

    def test_mask_multiple_secrets_in_string(self) -> None:
        """Test masking multiple secrets in same string."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=True,
            sanitize_dicts=False,
        )

        event_dict = {
            "event": "test",
            "message": "Connecting with api_key=sk-12345 and password=secret123",
        }

        result = processor(None, "info", event_dict)

        # All secrets should be masked
        assert "api_key=[MASKED]" in result["message"]
        assert "password=[MASKED]" in result["message"]
        assert "sk-12345" not in result["message"]
        assert "secret123" not in result["message"]

    def test_no_masking_when_disabled(self) -> None:
        """Test no masking when pattern masking is disabled."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=False,
            sanitize_dicts=False,
        )

        event_dict = {
            "event": "test",
            "message": "api_key=sk-1234567890abcdef",
        }

        result = processor(None, "info", event_dict)

        # Should not mask when feature is disabled
        assert result["message"] == "api_key=sk-1234567890abcdef"


class TestSanitizationProcessorDictSanitization(FoundationTestCase):
    """Test dictionary value sanitization."""

    def test_sanitize_authorization_header(self) -> None:
        """Test sanitizing Authorization header."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=False,
            sanitize_dicts=True,
        )

        event_dict = {
            "event": "test",
            "headers": {
                "Authorization": "Bearer secret123",
                "Content-Type": "application/json",
            },
        }

        result = processor(None, "info", event_dict)

        # Authorization should be sanitized
        assert result["headers"]["Authorization"] == "[REDACTED]"
        # Other headers should remain unchanged
        assert result["headers"]["Content-Type"] == "application/json"

    def test_sanitize_api_key_header(self) -> None:
        """Test sanitizing X-API-Key header."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=False,
            sanitize_dicts=True,
        )

        event_dict = {
            "event": "test",
            "headers": {
                "X-API-Key": "sk-1234567890abcdef",
                "User-Agent": "TestClient/1.0",
            },
        }

        result = processor(None, "info", event_dict)

        # API key should be sanitized
        assert result["headers"]["X-API-Key"] == "[REDACTED]"
        # Other headers should remain unchanged
        assert result["headers"]["User-Agent"] == "TestClient/1.0"

    def test_sanitize_multiple_dict_values(self) -> None:
        """Test sanitizing multiple sensitive dictionary values."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=False,
            sanitize_dicts=True,
        )

        event_dict = {
            "event": "test",
            "config": {
                "api_key": "sk-1234567890abcdef",
                "password": "secret123",
                "username": "testuser",
                "timeout": 30,
            },
        }

        result = processor(None, "info", event_dict)

        # Sensitive keys should be sanitized
        assert result["config"]["api_key"] == "[REDACTED]"
        assert result["config"]["password"] == "[REDACTED]"
        # Non-sensitive keys should remain unchanged
        assert result["config"]["username"] == "testuser"
        assert result["config"]["timeout"] == 30

    def test_no_dict_sanitization_when_disabled(self) -> None:
        """Test no dict sanitization when feature is disabled."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=False,
            sanitize_dicts=False,
        )

        event_dict = {
            "event": "test",
            "headers": {
                "Authorization": "Bearer secret123",
            },
        }

        result = processor(None, "info", event_dict)

        # Should not sanitize when feature is disabled
        assert result["headers"]["Authorization"] == "Bearer secret123"


# 🧱🏗️🔚
