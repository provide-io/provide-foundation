"""Comprehensive tests for transport/registry.py module."""

from unittest.mock import Mock, patch

import pytest

from provide.foundation.hub.components import ComponentCategory
from provide.foundation.transport.base import Transport
from provide.foundation.transport.errors import TransportNotFoundError
from provide.foundation.transport.registry import (
    get_transport,
    get_transport_for_scheme,
    get_transport_info,
    list_registered_transports,
    register_transport,
)
from provide.foundation.transport.types import TransportType


class MockTransport(Transport):
    """Mock transport implementation for testing."""

    def __init__(self, uri: str | None = None) -> None:
        self.uri = uri

    async def send(self, data: bytes, **kwargs) -> bytes:
        """Mock send implementation."""
        return b"mock_response"

    async def close(self) -> None:
        """Mock close implementation."""


class TestRegisterTransport:
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

    def test_register_transport_logging(self) -> None:
        """Test that transport registration logs debug message."""
        mock_registry = Mock()

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            with patch("provide.foundation.transport.registry.log") as mock_log:
                register_transport(
                    transport_type=TransportType.HTTP,
                    transport_class=MockTransport,
                    schemes=["http", "https"],
                )

                mock_log.debug.assert_called_once_with(
                    "Registered transport MockTransport for schemes: ['http', 'https']",
                )


class TestGetTransportForScheme:
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


class TestGetTransport:
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


class TestListRegisteredTransports:
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


class TestGetTransportInfo:
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
        mock_entry.metadata = {"schemes": ["https"], "transport_type": TransportType.HTTP}  # Scheme doesn't match

        mock_registry = [mock_entry]

        with patch("provide.foundation.transport.registry.get_component_registry", return_value=mock_registry):
            result = get_transport_info("http")

            assert result is not None
            assert result["name"] == "http"
            assert result["schemes"] == ["https"]


class TestIntegration:
    """Integration tests for registry functions working together."""

    def test_full_transport_lifecycle(self) -> None:
        """Test complete transport registration and retrieval workflow."""
        mock_registry_data = []
        mock_registry = Mock()
        mock_registry.__iter__ = lambda self: iter(mock_registry_data)

        def mock_register(name, value, dimension, metadata, replace) -> None:
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

        def mock_register(name, value, dimension, metadata, replace) -> None:
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
