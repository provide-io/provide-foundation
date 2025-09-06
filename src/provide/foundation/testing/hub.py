"""
Hub Testing Fixtures for Foundation.

Provides pytest fixtures for testing hub and component functionality,
including container directories and component registration scenarios.
"""

from pathlib import Path
import tempfile

import pytest


@pytest.fixture(scope="session")
def default_container_directory():
    """
    Provides a default directory for container operations in tests.

    This fixture is used by tests that need a temporary directory
    for container-related operations.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)
