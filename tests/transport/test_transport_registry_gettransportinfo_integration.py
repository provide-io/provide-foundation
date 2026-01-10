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
    get_transport_info,
    list_registered_transports,
    register_transport,
)
from provide.foundation.transport.types import TransportType
from tests.transport.test_transport_basic import MockTransport


class TestGetTransportInfo(FoundationTestCase):
    """Test get_transport_info function."""

    def test_get_transport_info_by_name(self) -> None:
        """Test getting transport info by name."""
        mock_entry = Mock()
        mock_entry.name = "http"
        mock_entry.dimension = ComponentCategory.TRANSPORT.value
        mock_entry.value = MockTransport
        mock_entry.metadata = {
            "schemes": ["http", "https"],
            "transport_type": TransportType.HTTP,
            "version": "1.0",
        }

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = get_transport_info("http")

            expected = {
                "name": "http",
                "class": MockTransport,
                "schemes": ["http", "https"],
                "transport_type": TransportType.HTTP,
                "metadata": {
                    "schemes": ["http", "https"],
                    "transport_type": TransportType.HTTP,
                    "version": "1.0",
                },
            }
            assert result == expected

    def test_get_transport_info_by_scheme(self) -> None:
        """Test getting transport info by scheme."""
        mock_entry = Mock()
        mock_entry.name = "http_transport"
        mock_entry.dimension = ComponentCategory.TRANSPORT.value
        mock_entry.value = MockTransport
        mock_entry.metadata = {
            "schemes": ["http", "https"],
            "transport_type": TransportType.HTTP,
        }

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = get_transport_info("https")

            expected = {
                "name": "http_transport",
                "class": MockTransport,
                "schemes": ["http", "https"],
                "transport_type": TransportType.HTTP,
                "metadata": {
                    "schemes": ["http", "https"],
                    "transport_type": TransportType.HTTP,
                },
            }
            assert result == expected

    def test_get_transport_info_case_insensitive_scheme(self) -> None:
        """Test getting transport info with case-insensitive scheme matching."""
        mock_entry = Mock()
        mock_entry.name = "http_transport"
        mock_entry.dimension = ComponentCategory.TRANSPORT.value
        mock_entry.value = MockTransport
        mock_entry.metadata = {"schemes": ["http"], "transport_type": TransportType.HTTP}

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = get_transport_info("HTTP")

            assert result is not None
            assert result["name"] == "http_transport"

    def test_get_transport_info_not_found(self) -> None:
        """Test getting transport info for non-existent transport."""
        mock_registry = []

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = get_transport_info("nonexistent")

            assert result is None

    def test_get_transport_info_wrong_dimension(self) -> None:
        """Test that entries with wrong dimension are ignored."""
        mock_entry = Mock()
        mock_entry.name = "http"
        mock_entry.dimension = "wrong_dimension"
        mock_entry.value = MockTransport
        mock_entry.metadata = {"schemes": ["http"]}

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = get_transport_info("http")

            assert result is None

    def test_get_transport_info_missing_schemes(self) -> None:
        """Test getting transport info when schemes metadata is missing."""
        mock_entry = Mock()
        mock_entry.name = "minimal"
        mock_entry.dimension = ComponentCategory.TRANSPORT.value
        mock_entry.value = MockTransport
        mock_entry.metadata = {"transport_type": TransportType.HTTP}  # No schemes

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            # Should find by name
            result = get_transport_info("minimal")
            assert result is not None
            assert result["schemes"] == []

            # Should not find by scheme since schemes is missing
            result = get_transport_info("http")
            assert result is None

    def test_get_transport_info_name_vs_scheme_priority(self) -> None:
        """Test that name matching takes priority over scheme matching."""
        mock_entry = Mock()
        mock_entry.name = "http"  # Name matches
        mock_entry.dimension = ComponentCategory.TRANSPORT.value
        mock_entry.value = MockTransport
        mock_entry.metadata = {
            "schemes": ["https"],
            "transport_type": TransportType.HTTP,
        }  # Scheme doesn't match

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = get_transport_info("http")

            assert result is not None
            assert result["name"] == "http"
            assert result["schemes"] == ["https"]


class TestIntegration(FoundationTestCase):
    """Integration tests for registry functions working together."""

    def test_full_transport_lifecycle(self) -> None:
        """Test complete transport registration and retrieval workflow."""
        mock_registry_data = []
        mock_registry = Mock()
        mock_registry.__iter__ = lambda self: iter(mock_registry_data)

        def mock_register(
            name: str, value: any, dimension: str, metadata: dict[str, any], replace: bool
        ) -> None:
            entry = Mock()
            entry.name = name
            entry.value = value
            entry.dimension = dimension
            entry.metadata = metadata
            mock_registry_data.append(entry)

        mock_registry.register = mock_register

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            # Register a transport
            register_transport(
                transport_type=TransportType.HTTP,
                transport_class=MockTransport,
                schemes=["http", "https"],
                version="1.0",
            )

            # Verify it appears in the list
            transports = list_registered_transports()
            assert "http" in transports
            assert transports["http"]["class"] == MockTransport
            assert transports["http"]["schemes"] == ["http", "https"]

            # Verify we can get the transport class by scheme
            transport_class = get_transport_for_scheme("http")
            assert transport_class == MockTransport

            transport_class = get_transport_for_scheme("https")
            assert transport_class == MockTransport

            # Verify we can get transport instances
            transport_instance = get_transport("http://example.com")
            assert isinstance(transport_instance, MockTransport)

            transport_instance = get_transport("https://example.com")
            assert isinstance(transport_instance, MockTransport)

            # Verify we can get transport info
            info = get_transport_info("http")
            assert info is not None
            assert info["name"] == "http"
            assert info["class"] == MockTransport

            info = get_transport_info("https")
            assert info is not None
            assert info["name"] == "http"  # Should find the same transport

    def test_multiple_transports(self) -> None:
        """Test working with multiple registered transports."""
        mock_registry_data = []
        mock_registry = Mock()
        mock_registry.__iter__ = lambda self: iter(mock_registry_data)

        def mock_register(
            name: str, value: any, dimension: str, metadata: dict[str, any], replace: bool
        ) -> None:
            entry = Mock()
            entry.name = name
            entry.value = value
            entry.dimension = dimension
            entry.metadata = metadata
            mock_registry_data.append(entry)

        mock_registry.register = mock_register

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            # Register multiple transports
            register_transport(
                transport_type=TransportType.HTTP,
                transport_class=MockTransport,
                schemes=["http", "https"],
            )

            register_transport(
                transport_type=TransportType.WS,
                transport_class=MockTransport,
                schemes=["ws", "wss"],
            )

            # Verify all transports are listed
            transports = list_registered_transports()
            assert len(transports) == 2
            assert "http" in transports
            assert "ws" in transports

            # Verify scheme resolution works for all
            assert get_transport_for_scheme("http") == MockTransport
            assert get_transport_for_scheme("https") == MockTransport
            assert get_transport_for_scheme("ws") == MockTransport
            assert get_transport_for_scheme("wss") == MockTransport

            # Verify unregistered scheme fails
            with pytest.raises(TransportNotFoundError):
                get_transport_for_scheme("ftp")


# 🧱🏗️🔚
