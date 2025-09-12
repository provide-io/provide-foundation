"""
Example conftest.py for flavorpack project.

This file should be placed at flavorpack/tests/conftest.py to provide
foundation testing fixtures to all flavorpack tests.
"""

import pytest

# Import foundation testing utilities
from provide.foundation.testing import (
    async_stream_reader,
    async_timeout,
    binary_file,
    # Foundation-specific
    captured_stderr_for_foundation,
    # Async testing helpers
    clean_event_loop,
    empty_directory,
    # Network testing
    free_port,
    httpx_mock_responses,
    mock_async_process,
    mock_cache,
    mock_file_system,
    # Mock objects
    mock_http_config,
    mock_logger,
    mock_server,
    mock_subprocess,
    mock_telemetry_config,
    mock_transport,
    nested_directory_structure,
    readonly_file,
    setup_foundation_telemetry_for_test,
    # File/directory fixtures
    temp_directory,
    temp_file,
    test_files_structure,
)

# Re-export for pytest discovery
__all__ = [
    # File fixtures
    "temp_directory",
    "test_files_structure",
    "temp_file",
    "binary_file",
    "nested_directory_structure",
    "empty_directory",
    "readonly_file",
    # Async fixtures
    "clean_event_loop",
    "async_timeout",
    "mock_async_process",
    "async_stream_reader",
    # Mock fixtures
    "mock_http_config",
    "mock_telemetry_config",
    "mock_logger",
    "mock_transport",
    "mock_cache",
    "mock_subprocess",
    "mock_file_system",
    # Network fixtures
    "free_port",
    "mock_server",
    "httpx_mock_responses",
    # Foundation fixtures
    "captured_stderr_for_foundation",
    "setup_foundation_telemetry_for_test",
]


# ============================================================================
# Flavorpack-specific fixtures
# ============================================================================

@pytest.fixture
def pspf_2025_config():
    """PSPF/2025 format configuration for testing."""
    return {
        "format": "PSPF/2025",
        "version": "1.0.0",
        "protocol": {
            "version": "2025.1",
            "features": ["operations", "metadata", "security"],
        },
    }


@pytest.fixture
def mock_uv_manager():
    """Mock UV package manager for testing."""
    from unittest.mock import Mock

    manager = Mock()
    manager.install = Mock(return_value=True)
    manager.sync = Mock(return_value=True)
    manager.add = Mock(return_value=True)
    manager.remove = Mock(return_value=True)
    manager.list_packages = Mock(return_value=[])
    manager.is_available = Mock(return_value=True)

    return manager


@pytest.fixture
def sample_wheel_metadata():
    """Sample wheel metadata for testing."""
    return {
        "Wheel-Version": "1.0",
        "Generator": "flavorpack",
        "Root-Is-Purelib": "true",
        "Tag": "py3-none-any",
    }


@pytest.fixture
def sample_package_structure(test_files_structure):
    """
    Create a sample Python package structure for testing.
    
    Extends the foundation test_files_structure fixture.
    """
    temp_path, source = test_files_structure

    # Add Python package structure
    package_dir = source / "mypackage"
    package_dir.mkdir()

    # Create package files
    (package_dir / "__init__.py").write_text('__version__ = "1.0.0"')
    (package_dir / "main.py").write_text('def main(): print("Hello")')
    (source / "setup.py").write_text('from setuptools import setup; setup()')
    (source / "pyproject.toml").write_text('[build-system]\nrequires = ["setuptools"]')

    return temp_path, source, package_dir


@pytest.fixture
def flavor_archive_path(temp_directory):
    """Path for flavor archive testing."""
    return temp_directory / "test_flavor.tar.gz"


@pytest.fixture
def mock_platform_info():
    """Mock platform information for testing."""
    return {
        "system": "Darwin",
        "machine": "arm64",
        "python_version": "3.11.0",
        "platform": "darwin_arm64",
    }


# ============================================================================
# Test markers and configuration
# ============================================================================

# Mark all async tests to use the clean_event_loop fixture automatically
def pytest_configure(config):
    """Configure pytest with flavorpack-specific settings."""
    config.addinivalue_line(
        "markers",
        "packaging: mark test as packaging-related"
    )
    config.addinivalue_line(
        "markers",
        "format_2025: mark test as PSPF/2025 format-related"
    )
    config.addinivalue_line(
        "markers",
        "requires_uv: mark test as requiring UV package manager"
    )
