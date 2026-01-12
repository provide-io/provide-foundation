#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import os
from typing import Any

from provide.testkit import reset_foundation_setup_for_testing
import pytest


@pytest.fixture(autouse=True)
def reset_foundation() -> None:
    """Reset Foundation state before each test."""
    reset_foundation_setup_for_testing()


@pytest.fixture(autouse=True)
def clear_serialization_cache() -> None:
    """Clear serialization cache before each test."""
    # Clear the module-level cache state
    from provide.foundation.serialization import cache as cache_module

    cache_module._serialization_cache = None
    cache_module._CACHE_ENABLED = None
    cache_module._CACHE_SIZE = None


@pytest.fixture
def clean_env(monkeypatch) -> None:
    """Clean environment for cache configuration tests."""
    # Remove all FOUNDATION_SERIALIZATION_* env vars
    for key in list(os.environ.keys()):
        if key.startswith("FOUNDATION_SERIALIZATION_"):
            monkeypatch.delenv(key, raising=False)


@pytest.fixture
def mock_env_no_cache(monkeypatch) -> None:
    """Mock environment to disable caching."""
    monkeypatch.setenv("FOUNDATION_SERIALIZATION_CACHE_ENABLED", "false")
    monkeypatch.setenv("FOUNDATION_SERIALIZATION_CACHE_SIZE", "128")


@pytest.fixture
def mock_env_small_cache(monkeypatch) -> None:
    """Mock environment for small cache size."""
    monkeypatch.setenv("FOUNDATION_SERIALIZATION_CACHE_ENABLED", "true")
    monkeypatch.setenv("FOUNDATION_SERIALIZATION_CACHE_SIZE", "2")


@pytest.fixture
def sample_dict_data() -> dict[str, Any]:
    """Sample dictionary data for testing."""
    return {
        "string": "value",
        "number": 42,
        "float": 3.14,
        "boolean": True,
        "null": None,
        "list": [1, 2, 3],
        "nested": {"key": "nested_value"},
    }


@pytest.fixture
def sample_list_data() -> list[Any]:
    """Sample list data for testing."""
    return [1, "two", 3.0, True, None, {"dict": "value"}]


@pytest.fixture
def unicode_data() -> dict[str, str]:
    """Unicode test data."""
    return {
        "japanese": "こんにちは",
        "emoji": "🎉🚀💖",
        "symbols": "∑∆∞",
    }


@pytest.fixture
def nested_data() -> dict[str, Any]:
    """Deeply nested test data."""
    return {
        "level1": {
            "level2": {
                "level3": {
                    "data": [1, 2, 3],
                    "info": "deep value",
                }
            }
        }
    }


@pytest.fixture
def ini_sample_data() -> dict[str, dict[str, str]]:
    """Sample INI format data."""
    return {
        "section1": {"key1": "value1", "key2": "value2"},
        "section2": {"keyA": "valueA", "keyB": "valueB"},
    }


@pytest.fixture
def env_sample_data() -> dict[str, str]:
    """Sample .env format data."""
    return {
        "DATABASE_URL": "postgresql://localhost/db",
        "API_KEY": "secret123",
        "DEBUG": "true",
        "PORT": "8000",
    }


# 🧱🏗️🔚
