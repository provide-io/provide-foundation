#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Hub DI testing fixtures."""

from __future__ import annotations

import pytest


def test_isolated_container_fixture(isolated_container) -> None:
    """Test that isolated_container fixture provides fresh Container."""
    from provide.foundation.hub import Container

    assert isolated_container is not None
    assert isinstance(isolated_container, Container)

    # Register a test dependency by type
    class TestService:
        def __init__(self) -> None:
            self.value = "test_value"

    test_instance = TestService()
    isolated_container.register(TestService, test_instance)
    resolved = isolated_container.get(TestService)
    assert resolved is test_instance
    assert resolved.value == "test_value"


def test_isolated_hub_fixture(isolated_hub) -> None:
    """Test that isolated_hub fixture provides Hub with isolated registries."""
    from provide.foundation.hub import Hub

    assert isolated_hub is not None
    assert isinstance(isolated_hub, Hub)
    assert isolated_hub._component_registry is not None
    assert isolated_hub._command_registry is not None


def test_isolated_containers_are_independent(isolated_container) -> None:
    """Test that each test gets its own isolated container."""

    # This test registers a value that should NOT be visible to other tests
    class IsolationTestService:
        value = "first_test_value"

    isolated_container.register(IsolationTestService, IsolationTestService())
    resolved = isolated_container.get(IsolationTestService)
    assert resolved.value == "first_test_value"


def test_isolated_containers_second_test(isolated_container) -> None:
    """Test that container is fresh and doesn't have previous test's data."""

    # This should not find the value from test_isolated_containers_are_independent
    class IsolationTestService:
        value = "should_not_exist"

    # Container should NOT have this type from previous test
    assert isolated_container.get(IsolationTestService) is None


@pytest.mark.asyncio
async def test_isolated_hub_with_universal_client(isolated_hub) -> None:
    """Test using isolated Hub with UniversalClient for DI testing."""
    from provide.foundation.transport import UniversalClient

    # Create client with isolated Hub - no global state pollution
    client = UniversalClient(hub=isolated_hub)

    assert client.hub is isolated_hub
    assert client.hub is not None


def test_isolated_fixtures_documentation() -> None:
    """Verify that fixtures have proper documentation for users."""
    from provide.testkit.hub.fixtures import isolated_container, isolated_hub

    assert isolated_container.__doc__ is not None
    assert "isolated" in isolated_container.__doc__.lower()
    assert "Container" in isolated_container.__doc__

    assert isolated_hub.__doc__ is not None
    assert "isolated" in isolated_hub.__doc__.lower()
    assert "Hub" in isolated_hub.__doc__


# 🧱🏗️🔚
