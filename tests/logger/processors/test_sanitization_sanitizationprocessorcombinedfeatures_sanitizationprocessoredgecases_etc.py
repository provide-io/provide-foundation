#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for logger/processors/sanitization.py module."""

from provide.testkit import FoundationTestCase


class TestSanitizationProcessorCombinedFeatures(FoundationTestCase):
    """Test combined pattern masking and dict sanitization."""

    def test_both_features_enabled(self) -> None:
        """Test both pattern masking and dict sanitization together."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=True,
            sanitize_dicts=True,
        )

        event_dict = {
            "event": "test",
            "message": "Connecting with api_key=sk-1234567890abcdef",  # String value - pattern masked
            "headers": {
                "Authorization": "Bearer secret123",  # Dict value - sanitized
            },
        }

        result = processor(None, "info", event_dict)

        # String should be pattern masked
        assert "api_key=[MASKED]" in result["message"]
        # Dict value should be sanitized
        assert result["headers"]["Authorization"] == "[REDACTED]"

    def test_combined_on_complex_structure(self) -> None:
        """Test sanitization on complex nested structure."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=True,
            sanitize_dicts=True,
        )

        event_dict = {
            "event": "api_call",
            "message": "Using api_key=sk-abcdef123456",
            "request": {
                "headers": {
                    "Authorization": "Bearer token123",
                    "Content-Type": "application/json",
                },
                "body": "some data",
            },
            "user_id": 42,
        }

        result = processor(None, "info", event_dict)

        # Check string masking
        assert "api_key=[MASKED]" in result["message"]
        # Check dict sanitization
        assert result["request"]["headers"]["Authorization"] == "[REDACTED]"
        # Check non-sensitive data preserved
        assert result["request"]["headers"]["Content-Type"] == "application/json"
        assert result["request"]["body"] == "some data"
        assert result["user_id"] == 42


class TestSanitizationProcessorEdgeCases(FoundationTestCase):
    """Test edge cases and error handling."""

    def test_empty_event_dict(self) -> None:
        """Test processor with empty event dict."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(enabled=True)
        event_dict = {}

        result = processor(None, "info", event_dict)

        assert result == {}

    def test_event_dict_with_none_values(self) -> None:
        """Test processor with None values."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(enabled=True)
        event_dict = {
            "event": "test",
            "api_key": None,
            "headers": None,
        }

        result = processor(None, "info", event_dict)

        # Should handle None gracefully
        assert "event" in result
        assert result["event"] == "test"

    def test_event_dict_with_empty_dict(self) -> None:
        """Test processor with empty dictionary value."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(enabled=True, sanitize_dicts=True)
        event_dict = {
            "event": "test",
            "headers": {},
        }

        result = processor(None, "info", event_dict)

        # Should handle empty dict gracefully
        assert result["headers"] == {}

    def test_event_dict_with_nested_empty_dicts(self) -> None:
        """Test processor with nested empty dictionaries."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(enabled=True)
        event_dict = {
            "event": "test",
            "config": {
                "nested": {},
            },
        }

        result = processor(None, "info", event_dict)

        # Should preserve structure
        assert result["config"]["nested"] == {}

    def test_immutability_of_original_event_dict(self) -> None:
        """Test that processor doesn't modify original event dict."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(enabled=True, mask_patterns=True)
        original_event_dict = {
            "event": "test",
            "api_key": "sk-1234567890abcdef",
        }
        original_copy = original_event_dict.copy()

        _ = processor(None, "info", original_event_dict)

        # Original should be unchanged (processor creates a copy)
        assert original_event_dict == original_copy


class TestSanitizationProcessorIntegration(FoundationTestCase):
    """Test sanitization processor integration scenarios."""

    def test_real_world_api_call_scenario(self) -> None:
        """Test sanitization in realistic API call logging scenario."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=True,
            sanitize_dicts=True,
        )

        event_dict = {
            "event": "API call made",
            "method": "POST",
            "url": "/api/v1/users",
            "message": "Using api_key=sk-prod-1234567890abcdef",
            "headers": {
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                "Content-Type": "application/json",
                "X-Request-ID": "req-123",
            },
            "status_code": 200,
            "duration_ms": 123.45,
        }

        result = processor(None, "info", event_dict)

        # Verify sensitive data is sanitized
        assert "api_key=[MASKED]" in result["message"]
        assert result["headers"]["Authorization"] == "[REDACTED]"
        # Verify non-sensitive data is preserved
        assert result["method"] == "POST"
        assert result["url"] == "/api/v1/users"
        assert result["headers"]["Content-Type"] == "application/json"
        assert result["headers"]["X-Request-ID"] == "req-123"
        assert result["status_code"] == 200
        assert result["duration_ms"] == 123.45

    def test_database_connection_scenario(self) -> None:
        """Test sanitization in database connection logging scenario."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        processor = create_sanitization_processor(
            enabled=True,
            mask_patterns=True,
            sanitize_dicts=True,
        )

        event_dict = {
            "event": "Database connection established",
            "message": "Connecting with password=super_secret_password",
            "connection_config": {
                "host": "db.example.com",
                "port": 5432,
                "database": "myapp",
                "username": "app_user",
                "password": "actual_secret",
                "ssl_mode": "require",
            },
        }

        result = processor(None, "info", event_dict)

        # Verify password in message is masked
        assert "password=[MASKED]" in result["message"]
        # Verify password in dict is sanitized
        assert result["connection_config"]["password"] == "[REDACTED]"
        # Verify other connection details are preserved
        assert result["connection_config"]["host"] == "db.example.com"
        assert result["connection_config"]["port"] == 5432
        assert result["connection_config"]["database"] == "myapp"
        assert result["connection_config"]["username"] == "app_user"
        assert result["connection_config"]["ssl_mode"] == "require"


class TestSanitizationProcessorModuleImports(FoundationTestCase):
    """Test module imports and exports."""

    def test_module_imports(self) -> None:
        """Test that the module can be imported."""
        from provide.foundation.logger.processors import sanitization

        assert sanitization is not None
        assert hasattr(sanitization, "create_sanitization_processor")

    def test_module_exports(self) -> None:
        """Test module __all__ exports."""
        from provide.foundation.logger.processors import sanitization

        assert hasattr(sanitization, "__all__")
        assert "create_sanitization_processor" in sanitization.__all__

    def test_function_callable(self) -> None:
        """Test that create_sanitization_processor is callable."""
        from provide.foundation.logger.processors.sanitization import (
            create_sanitization_processor,
        )

        assert callable(create_sanitization_processor)


# 🧱🏗️🔚
