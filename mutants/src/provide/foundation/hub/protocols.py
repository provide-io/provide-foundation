# provide/foundation/hub/protocols.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Any, Protocol, runtime_checkable

"""Resource management protocols for proper component lifecycle."""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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

    def xǁAsyncContextResourceǁ__init____mutmut_orig(self, resource_factory: Any) -> None:
        """Initialize with a resource factory."""
        self._resource_factory = resource_factory
        self._resource: Any = None

    def xǁAsyncContextResourceǁ__init____mutmut_1(self, resource_factory: Any) -> None:
        """Initialize with a resource factory."""
        self._resource_factory = None
        self._resource: Any = None

    def xǁAsyncContextResourceǁ__init____mutmut_2(self, resource_factory: Any) -> None:
        """Initialize with a resource factory."""
        self._resource_factory = resource_factory
        self._resource: Any = ""

    xǁAsyncContextResourceǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAsyncContextResourceǁ__init____mutmut_1": xǁAsyncContextResourceǁ__init____mutmut_1,
        "xǁAsyncContextResourceǁ__init____mutmut_2": xǁAsyncContextResourceǁ__init____mutmut_2,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAsyncContextResourceǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁAsyncContextResourceǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁAsyncContextResourceǁ__init____mutmut_orig)
    xǁAsyncContextResourceǁ__init____mutmut_orig.__name__ = "xǁAsyncContextResourceǁ__init__"

    async def xǁAsyncContextResourceǁ__aenter____mutmut_orig(self) -> Any:
        """Enter async context and acquire resource."""
        self._resource = await self._resource_factory()
        return self._resource

    async def xǁAsyncContextResourceǁ__aenter____mutmut_1(self) -> Any:
        """Enter async context and acquire resource."""
        self._resource = None
        return self._resource

    xǁAsyncContextResourceǁ__aenter____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAsyncContextResourceǁ__aenter____mutmut_1": xǁAsyncContextResourceǁ__aenter____mutmut_1
    }

    def __aenter__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAsyncContextResourceǁ__aenter____mutmut_orig"),
            object.__getattribute__(self, "xǁAsyncContextResourceǁ__aenter____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __aenter__.__signature__ = _mutmut_signature(xǁAsyncContextResourceǁ__aenter____mutmut_orig)
    xǁAsyncContextResourceǁ__aenter____mutmut_orig.__name__ = "xǁAsyncContextResourceǁ__aenter__"

    async def xǁAsyncContextResourceǁ__aexit____mutmut_orig(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr(self._resource, "dispose_async"):
            await self._resource.dispose_async()
        elif self._resource and hasattr(self._resource, "dispose"):
            self._resource.dispose()

    async def xǁAsyncContextResourceǁ__aexit____mutmut_1(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource or hasattr(self._resource, "dispose_async"):
            await self._resource.dispose_async()
        elif self._resource and hasattr(self._resource, "dispose"):
            self._resource.dispose()

    async def xǁAsyncContextResourceǁ__aexit____mutmut_2(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr(None, "dispose_async"):
            await self._resource.dispose_async()
        elif self._resource and hasattr(self._resource, "dispose"):
            self._resource.dispose()

    async def xǁAsyncContextResourceǁ__aexit____mutmut_3(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr(self._resource, None):
            await self._resource.dispose_async()
        elif self._resource and hasattr(self._resource, "dispose"):
            self._resource.dispose()

    async def xǁAsyncContextResourceǁ__aexit____mutmut_4(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr("dispose_async"):
            await self._resource.dispose_async()
        elif self._resource and hasattr(self._resource, "dispose"):
            self._resource.dispose()

    async def xǁAsyncContextResourceǁ__aexit____mutmut_5(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr(
            self._resource,
        ):
            await self._resource.dispose_async()
        elif self._resource and hasattr(self._resource, "dispose"):
            self._resource.dispose()

    async def xǁAsyncContextResourceǁ__aexit____mutmut_6(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr(self._resource, "XXdispose_asyncXX"):
            await self._resource.dispose_async()
        elif self._resource and hasattr(self._resource, "dispose"):
            self._resource.dispose()

    async def xǁAsyncContextResourceǁ__aexit____mutmut_7(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr(self._resource, "DISPOSE_ASYNC"):
            await self._resource.dispose_async()
        elif self._resource and hasattr(self._resource, "dispose"):
            self._resource.dispose()

    async def xǁAsyncContextResourceǁ__aexit____mutmut_8(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr(self._resource, "dispose_async"):
            await self._resource.dispose_async()
        elif self._resource or hasattr(self._resource, "dispose"):
            self._resource.dispose()

    async def xǁAsyncContextResourceǁ__aexit____mutmut_9(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr(self._resource, "dispose_async"):
            await self._resource.dispose_async()
        elif self._resource and hasattr(None, "dispose"):
            self._resource.dispose()

    async def xǁAsyncContextResourceǁ__aexit____mutmut_10(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr(self._resource, "dispose_async"):
            await self._resource.dispose_async()
        elif self._resource and hasattr(self._resource, None):
            self._resource.dispose()

    async def xǁAsyncContextResourceǁ__aexit____mutmut_11(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr(self._resource, "dispose_async"):
            await self._resource.dispose_async()
        elif self._resource and hasattr("dispose"):
            self._resource.dispose()

    async def xǁAsyncContextResourceǁ__aexit____mutmut_12(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr(self._resource, "dispose_async"):
            await self._resource.dispose_async()
        elif self._resource and hasattr(
            self._resource,
        ):
            self._resource.dispose()

    async def xǁAsyncContextResourceǁ__aexit____mutmut_13(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr(self._resource, "dispose_async"):
            await self._resource.dispose_async()
        elif self._resource and hasattr(self._resource, "XXdisposeXX"):
            self._resource.dispose()

    async def xǁAsyncContextResourceǁ__aexit____mutmut_14(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        """Exit async context and cleanup resource."""
        if self._resource and hasattr(self._resource, "dispose_async"):
            await self._resource.dispose_async()
        elif self._resource and hasattr(self._resource, "DISPOSE"):
            self._resource.dispose()

    xǁAsyncContextResourceǁ__aexit____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAsyncContextResourceǁ__aexit____mutmut_1": xǁAsyncContextResourceǁ__aexit____mutmut_1,
        "xǁAsyncContextResourceǁ__aexit____mutmut_2": xǁAsyncContextResourceǁ__aexit____mutmut_2,
        "xǁAsyncContextResourceǁ__aexit____mutmut_3": xǁAsyncContextResourceǁ__aexit____mutmut_3,
        "xǁAsyncContextResourceǁ__aexit____mutmut_4": xǁAsyncContextResourceǁ__aexit____mutmut_4,
        "xǁAsyncContextResourceǁ__aexit____mutmut_5": xǁAsyncContextResourceǁ__aexit____mutmut_5,
        "xǁAsyncContextResourceǁ__aexit____mutmut_6": xǁAsyncContextResourceǁ__aexit____mutmut_6,
        "xǁAsyncContextResourceǁ__aexit____mutmut_7": xǁAsyncContextResourceǁ__aexit____mutmut_7,
        "xǁAsyncContextResourceǁ__aexit____mutmut_8": xǁAsyncContextResourceǁ__aexit____mutmut_8,
        "xǁAsyncContextResourceǁ__aexit____mutmut_9": xǁAsyncContextResourceǁ__aexit____mutmut_9,
        "xǁAsyncContextResourceǁ__aexit____mutmut_10": xǁAsyncContextResourceǁ__aexit____mutmut_10,
        "xǁAsyncContextResourceǁ__aexit____mutmut_11": xǁAsyncContextResourceǁ__aexit____mutmut_11,
        "xǁAsyncContextResourceǁ__aexit____mutmut_12": xǁAsyncContextResourceǁ__aexit____mutmut_12,
        "xǁAsyncContextResourceǁ__aexit____mutmut_13": xǁAsyncContextResourceǁ__aexit____mutmut_13,
        "xǁAsyncContextResourceǁ__aexit____mutmut_14": xǁAsyncContextResourceǁ__aexit____mutmut_14,
    }

    def __aexit__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAsyncContextResourceǁ__aexit____mutmut_orig"),
            object.__getattribute__(self, "xǁAsyncContextResourceǁ__aexit____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __aexit__.__signature__ = _mutmut_signature(xǁAsyncContextResourceǁ__aexit____mutmut_orig)
    xǁAsyncContextResourceǁ__aexit____mutmut_orig.__name__ = "xǁAsyncContextResourceǁ__aexit__"


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


# <3 🧱🤝🌐🪄
