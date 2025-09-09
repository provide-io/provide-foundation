"""
Mocking Fixtures and Utilities.

Standardized mocking patterns and fixtures for the provide-io ecosystem.
Reduces boilerplate and ensures consistent mocking across all tests.
"""

from unittest.mock import Mock, MagicMock, AsyncMock, PropertyMock, patch, call, ANY
from typing import Any, Callable
from collections.abc import Generator
import sys

import pytest


@pytest.fixture
def mock_factory():
    """
    Factory for creating configured mock objects.
    
    Returns:
        Function that creates mock objects with common configurations.
    """
    def _create_mock(name: str = None, **kwargs) -> Mock:
        """
        Create a mock with standard configuration.
        
        Args:
            name: Optional name for the mock
            **kwargs: Additional mock configuration
            
        Returns:
            Configured Mock object
        """
        defaults = {
            "spec_set": True if "spec" in kwargs else False,
        }
        defaults.update(kwargs)
        
        mock = Mock(name=name, **defaults)
        return mock
    
    return _create_mock


@pytest.fixture
def magic_mock_factory():
    """
    Factory for creating MagicMock objects.
    
    Returns:
        Function that creates MagicMock objects with common configurations.
    """
    def _create_magic_mock(name: str = None, **kwargs) -> MagicMock:
        """
        Create a MagicMock with standard configuration.
        
        Args:
            name: Optional name for the mock
            **kwargs: Additional mock configuration
            
        Returns:
            Configured MagicMock object
        """
        return MagicMock(name=name, **kwargs)
    
    return _create_magic_mock


@pytest.fixture
def async_mock_factory():
    """
    Factory for creating AsyncMock objects.
    
    Returns:
        Function that creates AsyncMock objects with common configurations.
    """
    def _create_async_mock(name: str = None, return_value=None, side_effect=None, **kwargs) -> AsyncMock:
        """
        Create an AsyncMock with standard configuration.
        
        Args:
            name: Optional name for the mock
            return_value: Return value for the async mock
            side_effect: Side effect for the async mock
            **kwargs: Additional mock configuration
            
        Returns:
            Configured AsyncMock object
        """
        mock = AsyncMock(name=name, **kwargs)
        if return_value is not None:
            mock.return_value = return_value
        if side_effect is not None:
            mock.side_effect = side_effect
        return mock
    
    return _create_async_mock


@pytest.fixture
def property_mock_factory():
    """
    Factory for creating PropertyMock objects.
    
    Returns:
        Function that creates PropertyMock objects.
    """
    def _create_property_mock(return_value=None, side_effect=None, **kwargs) -> PropertyMock:
        """
        Create a PropertyMock.
        
        Args:
            return_value: Return value for the property
            side_effect: Side effect for the property
            **kwargs: Additional mock configuration
            
        Returns:
            Configured PropertyMock object
        """
        return PropertyMock(return_value=return_value, side_effect=side_effect, **kwargs)
    
    return _create_property_mock


@pytest.fixture
def patch_fixture():
    """
    Fixture for patching objects with automatic cleanup.
    
    Returns:
        Function that patches objects and returns the mock.
    """
    patches = []
    
    def _patch(target: str, **kwargs) -> Mock:
        """
        Patch a target with automatic cleanup.
        
        Args:
            target: The target to patch (module.Class.attribute)
            **kwargs: Additional patch configuration
            
        Returns:
            The mock object
        """
        patcher = patch(target, **kwargs)
        mock = patcher.start()
        patches.append(patcher)
        return mock
    
    yield _patch
    
    # Cleanup all patches
    for patcher in patches:
        patcher.stop()


@pytest.fixture
def patch_multiple_fixture():
    """
    Fixture for patching multiple objects at once.
    
    Returns:
        Function that patches multiple targets.
    """
    patches = []
    
    def _patch_multiple(target_module: str, **kwargs) -> dict[str, Mock]:
        """
        Patch multiple attributes in a module.
        
        Args:
            target_module: The module to patch in
            **kwargs: Mapping of attribute names to mock objects or DEFAULT
            
        Returns:
            Dict mapping attribute names to mock objects
        """
        from unittest.mock import patch as mock_patch
        patcher = mock_patch.multiple(target_module, **kwargs)
        mocks = patcher.start()
        patches.append(patcher)
        return mocks
    
    yield _patch_multiple
    
    # Cleanup all patches
    for patcher in patches:
        patcher.stop()


@pytest.fixture
def auto_patch():
    """
    Context manager for automatic patching with cleanup.
    
    Returns:
        Patch context manager class.
    """
    class AutoPatch:
        def __init__(self):
            self.patches = []
        
        def object(self, target: Any, attribute: str, **kwargs) -> Mock:
            """Patch an object's attribute."""
            patcher = patch.object(target, attribute, **kwargs)
            mock = patcher.start()
            self.patches.append(patcher)
            return mock
        
        def dict(self, target: dict, values: dict, **kwargs) -> None:
            """Patch a dictionary."""
            patcher = patch.dict(target, values, **kwargs)
            patcher.start()
            self.patches.append(patcher)
        
        def env(self, **env_vars) -> None:
            """Patch environment variables."""
            import os
            patcher = patch.dict(os.environ, env_vars)
            patcher.start()
            self.patches.append(patcher)
        
        def cleanup(self):
            """Stop all patches."""
            for patcher in self.patches:
                patcher.stop()
    
    patcher = AutoPatch()
    yield patcher
    patcher.cleanup()


@pytest.fixture
def mock_open_fixture():
    """
    Fixture for mocking file operations.
    
    Returns:
        Function that creates a mock for open().
    """
    from unittest.mock import mock_open
    
    def _mock_open(read_data: str = None) -> Mock:
        """
        Create a mock for the open() builtin.
        
        Args:
            read_data: Optional data to return when reading
            
        Returns:
            Mock object for open()
        """
        return mock_open(read_data=read_data)
    
    return _mock_open


@pytest.fixture
def spy_fixture():
    """
    Create a spy (mock that calls through to the original).
    
    Returns:
        Function that creates spy objects.
    """
    def _create_spy(obj: Any, method_name: str) -> Mock:
        """
        Create a spy on a method.
        
        Args:
            obj: The object to spy on
            method_name: The method name to spy on
            
        Returns:
            Mock that wraps the original method
        """
        original = getattr(obj, method_name)
        mock = Mock(wraps=original)
        setattr(obj, method_name, mock)
        return mock
    
    return _create_spy


@pytest.fixture
def assert_mock_calls():
    """
    Helper for asserting mock calls with better error messages.
    
    Returns:
        Function for asserting mock calls.
    """
    def _assert_calls(mock: Mock, expected_calls: list, any_order: bool = False):
        """
        Assert that a mock was called with expected calls.
        
        Args:
            mock: The mock to check
            expected_calls: List of expected call objects
            any_order: Whether calls can be in any order
        """
        if any_order:
            mock.assert_has_calls(expected_calls, any_order=True)
        else:
            mock.assert_has_calls(expected_calls)
    
    return _assert_calls


# Re-export commonly used mock utilities
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