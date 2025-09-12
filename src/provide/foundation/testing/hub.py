"""
Hub Testing Fixtures for Foundation.

Provides pytest fixtures for testing hub and component functionality,
including container directories and component registration scenarios.
"""

from pathlib import Path

import pytest

from provide.foundation.file import temp_dir as foundation_temp_dir


@pytest.fixture(scope="session")
def default_container_directory():
    """
    Provides a default directory for container operations in tests.

    This fixture is used by tests that need a temporary directory
    for container-related operations.
    """
    with foundation_temp_dir() as tmp_dir:
        yield tmp_dir
