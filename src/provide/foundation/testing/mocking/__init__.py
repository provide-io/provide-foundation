"""
Mocking utilities for the provide-io ecosystem.

Standardized mocking patterns, fixtures, and utilities to reduce
boilerplate and ensure consistent mocking across all tests.
"""

from provide.foundation.testing.mocking.fixtures import (
    Mock,
    MagicMock,
    AsyncMock,
    PropertyMock,
    patch,
    call,
    ANY,
    mock_factory,
    magic_mock_factory,
    async_mock_factory,
    property_mock_factory,
    patch_fixture,
    patch_multiple_fixture,
    auto_patch,
    mock_open_fixture,
    spy_fixture,
    assert_mock_calls,
)

__all__ = [
    "Mock",
    "MagicMock",
    "AsyncMock",
    "PropertyMock",
    "patch",
    "call",
    "ANY",
    "mock_factory",
    "magic_mock_factory",
    "async_mock_factory",
    "property_mock_factory",
    "patch_fixture",
    "patch_multiple_fixture",
    "auto_patch",
    "mock_open_fixture",
    "spy_fixture",
    "assert_mock_calls",
]