#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Any, Protocol, runtime_checkable

"""Resource management protocols for proper component lifecycle."""


@runtime_checkable
class Disposable(Protocol):
    """Protocol for components that require cleanup."""

    def dispose(self) -> None:
        """Dispose of the component and clean up resources."""
        ...


@runtime_checkable
class AsyncDisposable(Protocol):
    """Protocol for components that require async cleanup."""

    async def dispose_async(self) -> None:
        """Dispose of the component and clean up resources asynchronously."""
        ...


@runtime_checkable
class Initializable(Protocol):
    """Protocol for components that support lazy initialization."""

    def initialize(self) -> Any:
        """Initialize the component."""
        ...


@runtime_checkable
class AsyncInitializable(Protocol):
    """Protocol for components that support async lazy initialization."""

    async def initialize_async(self) -> Any:
        """Initialize the component asynchronously."""
        ...


@runtime_checkable
class HealthCheckable(Protocol):
    """Protocol for components that support health checks."""

    def health_check(self) -> dict[str, Any]:
        """Check component health status."""
        ...


class ResourceManager(ABC):
    """Abstract base class for resource managers."""

    @abstractmethod
    def acquire_resource(self, resource_id: str) -> Any:
        """Acquire a resource by ID."""
        pass

    @abstractmethod
    def release_resource(self, resource_id: str) -> None:
        """Release a resource by ID."""
        pass

    @abstractmethod
    def cleanup_all(self) -> None:
        """Clean up all managed resources."""
        pass


class AsyncResourceManager(ABC):
    """Abstract base class for async resource managers."""

    @abstractmethod
    async def acquire_resource_async(self, resource_id: str) -> Any:
        """Acquire a resource by ID asynchronously."""
        pass

    @abstractmethod
    async def release_resource_async(self, resource_id: str) -> None:
        """Release a resource by ID asynchronously."""
        pass

    @abstractmethod
    async def cleanup_all_async(self) -> None:
        """Clean up all managed resources asynchronously."""
        pass


class AsyncContextResource(AbstractAsyncContextManager[Any]):
    """Base class for async context-managed resources."""

    def __init__(self, resource_factory: Any) -> None:
        """Initialize with a resource factory."""
        self._resource_factory = resource_factory
        self._resource: Any = None

    async def __aenter__(self) -> Any:
        """Enter async context and acquire resource."""
        self._resource = await self._resource_factory()
        return self._resource

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr(self._resource, "dispose_async"):
            await self._resource.dispose_async()
        elif self._resource and hasattr(self._resource, "dispose"):
            self._resource.dispose()


__all__ = [
    "AsyncContextResource",
    "AsyncDisposable",
    "AsyncInitializable",
    "AsyncResourceManager",
    "Disposable",
    "HealthCheckable",
    "Initializable",
    "ResourceManager",
]

# 🧱🏗️🔚
