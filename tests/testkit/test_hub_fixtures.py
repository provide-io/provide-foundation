"""Tests for Hub DI testing fixtures."""

from __future__ import annotations

import pytest


def test_isolated_container_fixture(isolated_container):
    """Test that isolated_container fixture provides fresh Container."""
    from provide.foundation.hub import Container

    assert isolated_container is not None
    assert isinstance(isolated_container, Container)

    # Register a test dependency
    isolated_container.register("test_service", "test_value")
    value = isolated_container.resolve("test_service")
    assert value == "test_value"


def test_isolated_hub_fixture(isolated_hub):
    """Test that isolated_hub fixture provides Hub with isolated Container."""
    from provide.foundation.hub import Hub

    assert isolated_hub is not None
    assert isinstance(isolated_hub, Hub)
    assert isolated_hub._container is not None


def test_isolated_containers_are_independent(isolated_container):
    """Test that each test gets its own isolated container."""
    # This test registers a value that should NOT be visible to other tests
    isolated_container.register("test_isolation", "first_test_value")
    assert isolated_container.resolve("test_isolation") == "first_test_value"


def test_isolated_containers_second_test(isolated_container):
    """Test that container is fresh and doesn't have previous test's data."""
    # This should not find the value from test_isolated_containers_are_independent
    with pytest.raises(Exception):  # Container raises when key not found
        isolated_container.resolve("test_isolation")


@pytest.mark.asyncio
async def test_isolated_hub_with_universal_client(isolated_hub):
    """Test using isolated Hub with UniversalClient for DI testing."""
    from provide.foundation.transport import UniversalClient

    # Create client with isolated Hub - no global state pollution
    client = UniversalClient(hub=isolated_hub)

    assert client.hub is isolated_hub
    assert client.hub is not None


def test_isolated_fixtures_documentation():
    """Verify that fixtures have proper documentation for users."""
    from provide.testkit.hub.fixtures import isolated_container, isolated_hub

    assert isolated_container.__doc__ is not None
    assert "isolated" in isolated_container.__doc__.lower()
    assert "Container" in isolated_container.__doc__

    assert isolated_hub.__doc__ is not None
    assert "isolated" in isolated_hub.__doc__.lower()
    assert "Hub" in isolated_hub.__doc__
