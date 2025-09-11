"""
Mocking utilities for the provide-io ecosystem.

Standardized mocking patterns, fixtures, and utilities to reduce
boilerplate and ensure consistent mocking across all tests.
"""

from provide.foundation.testing.mocking.fixtures import (
    ANY,
    AsyncMock,
    MagicMock,
    Mock,
    PropertyMock,
    assert_mock_calls,
    async_mock_factory,
    auto_patch,
    call,
    magic_mock_factory,
    mock_factory,
    mock_open_fixture,
    patch,
    patch_fixture,
    patch_multiple_fixture,
    property_mock_factory,
    spy_fixture,
)

__all__ = [
    "ANY",
    "AsyncMock",
    "MagicMock",
    "Mock",
    "PropertyMock",
    "assert_mock_calls",
    "async_mock_factory",
    "auto_patch",
    "call",
    "magic_mock_factory",
    "mock_factory",
    "mock_open_fixture",
    "patch",
    "patch_fixture",
    "patch_multiple_fixture",
    "property_mock_factory",
    "spy_fixture",
]
