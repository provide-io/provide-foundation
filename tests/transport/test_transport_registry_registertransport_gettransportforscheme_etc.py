#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for transport/registry.py module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.hub.components import ComponentCategory
from provide.foundation.transport.errors import TransportNotFoundError
from provide.foundation.transport.registry import (
    get_transport,
    get_transport_for_scheme,
    list_registered_transports,
    register_transport,
)
from provide.foundation.transport.types import TransportType
from tests.transport.test_transport_basic import MockTransport


class TestRegisterTransport(FoundationTestCase):
    """Test register_transport function."""

    def test_register_transport_basic(self) -> None:
        """Test basic transport registration."""
        mock_registry = Mock()

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            register_transport(
                transport_type=TransportType.HTTP,
                transport_class=MockTransport,
                schemes=["http", "https"],
            )

            mock_registry.register.assert_called_once_with(
                name="http",
                value=MockTransport,
                dimension=ComponentCategory.TRANSPORT.value,
                metadata={
                    "transport_type": TransportType.HTTP,
                    "schemes": ["http", "https"],
                    "class_name": "MockTransport",
                },
                replace=True,
            )

    def test_register_transport_default_schemes(self) -> None:
        """Test transport registration with default schemes."""
        mock_registry = Mock()

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            register_transport(
                transport_type=TransportType.HTTP,
                transport_class=MockTransport,
            )

            # Verify it uses transport type value as default scheme
            call_args = mock_registry.register.call_args
            assert call_args[1]["metadata"]["schemes"] == ["http"]

    def test_register_transport_with_metadata(self) -> None:
        """Test transport registration with additional metadata."""
        mock_registry = Mock()

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            register_transport(
                transport_type=TransportType.HTTP,
                transport_class=MockTransport,
                schemes=["http"],
                custom_key="custom_value",
                version="1.0.0",
            )

            call_args = mock_registry.register.call_args
            metadata = call_args[1]["metadata"]
            assert metadata["custom_key"] == "custom_value"
            assert metadata["version"] == "1.0.0"
            assert metadata["transport_type"] == TransportType.HTTP
            assert metadata["schemes"] == ["http"]
            assert metadata["class_name"] == "MockTransport"

    def test_register_transport_no_logging(self) -> None:
        """Test that transport registration no longer logs (to reduce test noise)."""
        mock_registry = Mock()

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            with patch("provide.foundation.transport.registry.log") as mock_log:
                register_transport(
                    transport_type=TransportType.HTTP,
                    transport_class=MockTransport,
                    schemes=["http", "https"],
                )

                # Verify no logging occurred
                mock_log.trace.assert_not_called()
                mock_log.debug.assert_not_called()
                mock_log.info.assert_not_called()


class TestGetTransportForScheme(FoundationTestCase):
    """Test get_transport_for_scheme function."""

    def test_get_transport_for_scheme_found(self) -> None:
        """Test getting transport for registered scheme."""
        mock_entry = Mock()
        mock_entry.dimension = ComponentCategory.TRANSPORT.value
        mock_entry.metadata = {"schemes": ["http", "https"]}
        mock_entry.value = MockTransport

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            with patch("provide.foundation.transport.registry.log") as mock_log:
                result = get_transport_for_scheme("http")

                assert result == MockTransport
                mock_log.trace.assert_called_once_with(
                    "Found transport MockTransport for scheme 'http'",
                )

    def test_get_transport_for_scheme_case_insensitive(self) -> None:
        """Test getting transport with case-insensitive scheme matching."""
        mock_entry = Mock()
        mock_entry.dimension = ComponentCategory.TRANSPORT.value
        mock_entry.metadata = {"schemes": ["http", "https"]}
        mock_entry.value = MockTransport

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = get_transport_for_scheme("HTTP")
            assert result == MockTransport

    def test_get_transport_for_scheme_not_found(self) -> None:
        """Test getting transport for unregistered scheme."""
        mock_registry = []

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            with pytest.raises(TransportNotFoundError) as exc_info:
                get_transport_for_scheme("unknown")

            assert "No transport registered for scheme: unknown" in str(exc_info.value)
            assert exc_info.value.scheme == "unknown"

    def test_get_transport_for_scheme_wrong_dimension(self) -> None:
        """Test that entries with wrong dimension are ignored."""
        mock_entry = Mock()
        mock_entry.dimension = "wrong_dimension"
        mock_entry.metadata = {"schemes": ["http"]}
        mock_entry.value = MockTransport

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            with pytest.raises(TransportNotFoundError):
                get_transport_for_scheme("http")

    def test_get_transport_for_scheme_no_schemes_metadata(self) -> None:
        """Test handling entry without schemes metadata."""
        mock_entry = Mock()
        mock_entry.dimension = ComponentCategory.TRANSPORT.value
        mock_entry.metadata = {}  # No schemes
        mock_entry.value = MockTransport

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            with pytest.raises(TransportNotFoundError):
                get_transport_for_scheme("http")


class TestGetTransport(FoundationTestCase):
    """Test get_transport function."""

    def test_get_transport_success(self) -> None:
        """Test getting transport instance for valid URI."""
        mock_entry = Mock()
        mock_entry.dimension = ComponentCategory.TRANSPORT.value
        mock_entry.metadata = {"schemes": ["http"]}
        mock_entry.value = MockTransport

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = get_transport("http://example.com")

            assert isinstance(result, MockTransport)

    def test_get_transport_https(self) -> None:
        """Test getting transport for HTTPS URI."""
        mock_entry = Mock()
        mock_entry.dimension = ComponentCategory.TRANSPORT.value
        mock_entry.metadata = {"schemes": ["https"]}
        mock_entry.value = MockTransport

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = get_transport("https://secure.example.com/path")

            assert isinstance(result, MockTransport)

    def test_get_transport_scheme_extraction(self) -> None:
        """Test that scheme is correctly extracted from complex URIs."""
        mock_entry = Mock()
        mock_entry.dimension = ComponentCategory.TRANSPORT.value
        mock_entry.metadata = {"schemes": ["custom"]}
        mock_entry.value = MockTransport

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = get_transport("custom://user:pass@host:port/path?query=value#fragment")

            assert isinstance(result, MockTransport)

    def test_get_transport_not_found(self) -> None:
        """Test getting transport for unsupported scheme."""
        mock_registry = []

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            with pytest.raises(TransportNotFoundError):
                get_transport("unknown://example.com")


class TestListRegisteredTransports(FoundationTestCase):
    """Test list_registered_transports function."""

    def test_list_registered_transports_empty(self) -> None:
        """Test listing transports when none are registered."""
        mock_registry = []

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = list_registered_transports()

            assert result == {}

    def test_list_registered_transports_single(self) -> None:
        """Test listing single registered transport."""
        mock_entry = Mock()
        mock_entry.name = "http"
        mock_entry.dimension = ComponentCategory.TRANSPORT.value
        mock_entry.value = MockTransport
        mock_entry.metadata = {
            "schemes": ["http", "https"],
            "transport_type": TransportType.HTTP,
            "custom": "value",
        }

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = list_registered_transports()

            expected = {
                "http": {
                    "class": MockTransport,
                    "schemes": ["http", "https"],
                    "transport_type": TransportType.HTTP,
                    "metadata": {
                        "schemes": ["http", "https"],
                        "transport_type": TransportType.HTTP,
                        "custom": "value",
                    },
                },
            }
            assert result == expected

    def test_list_registered_transports_multiple(self) -> None:
        """Test listing multiple registered transports."""
        mock_entry1 = Mock()
        mock_entry1.name = "http"
        mock_entry1.dimension = ComponentCategory.TRANSPORT.value
        mock_entry1.value = MockTransport
        mock_entry1.metadata = {"schemes": ["http"], "transport_type": TransportType.HTTP}

        mock_entry2 = Mock()
        mock_entry2.name = "ws"
        mock_entry2.dimension = ComponentCategory.TRANSPORT.value
        mock_entry2.value = MockTransport
        mock_entry2.metadata = {"schemes": ["ws"], "transport_type": TransportType.WS}

        # Add non-transport entry to verify filtering
        mock_entry3 = Mock()
        mock_entry3.name = "other"
        mock_entry3.dimension = "other_dimension"
        mock_entry3.value = Mock
        mock_entry3.metadata = {}

        mock_registry = [mock_entry1, mock_entry2, mock_entry3]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = list_registered_transports()

            assert len(result) == 2
            assert "http" in result
            assert "ws" in result
            assert "other" not in result

    def test_list_registered_transports_missing_metadata(self) -> None:
        """Test listing transports with missing metadata fields."""
        mock_entry = Mock()
        mock_entry.name = "minimal"
        mock_entry.dimension = ComponentCategory.TRANSPORT.value
        mock_entry.value = MockTransport
        mock_entry.metadata = {}  # Missing schemes and transport_type

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = list_registered_transports()

            expected = {
                "minimal": {
                    "class": MockTransport,
                    "schemes": [],  # Default when missing
                    "transport_type": None,  # Default when missing
                    "metadata": {},
                },
            }
            assert result == expected


# 🧱🏗️🔚
