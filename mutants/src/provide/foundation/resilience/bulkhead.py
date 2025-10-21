# provide/foundation/resilience/bulkhead.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Awaitable, Callable
import threading
import time
from typing import Any, TypeVar

from attrs import define, field

from provide.foundation.resilience.bulkhead_async import AsyncResourcePool
from provide.foundation.resilience.bulkhead_sync import SyncResourcePool

"""Bulkhead pattern for resource isolation and limiting.

The bulkhead pattern isolates resources to prevent failures in one part of
the system from cascading to other parts. It limits concurrent access to
resources and provides isolation boundaries.
"""

T = TypeVar("T")
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


@define(kw_only=True, slots=True)
class Bulkhead:
    """Bulkhead isolation pattern for protecting resources.

    Can use either SyncResourcePool or AsyncResourcePool depending on use case.
    """

    name: str
    pool: SyncResourcePool | AsyncResourcePool = field(factory=SyncResourcePool)

    def execute(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute function with bulkhead protection (sync).

        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            RuntimeError: If resource cannot be acquired
            Exception: Any exception from the protected function
        """
        # Must use SyncResourcePool for sync execution
        if not isinstance(self.pool, SyncResourcePool):
            raise TypeError("Sync execution requires SyncResourcePool")

        if not self.pool.acquire():
            raise RuntimeError(f"Bulkhead '{self.name}' is at capacity")

        try:
            # Emit acquisition event
            self._emit_event("acquired")
            start_time = time.time()

            result = func(*args, **kwargs)

            # Emit success event
            execution_time = time.time() - start_time
            self._emit_event("completed", execution_time=execution_time)

            return result
        except Exception as e:
            # Emit failure event
            execution_time = time.time() - start_time
            self._emit_event("failed", error=str(e), execution_time=execution_time)
            raise
        finally:
            self.pool.release()
            self._emit_event("released")

    async def execute_async(self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute async function with bulkhead protection.

        Args:
            func: Async function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            RuntimeError: If resource cannot be acquired
            Exception: Any exception from the protected function
        """
        # Must use AsyncResourcePool for async execution
        if not isinstance(self.pool, AsyncResourcePool):
            raise TypeError("Async execution requires AsyncResourcePool")

        if not await self.pool.acquire():
            raise RuntimeError(f"Bulkhead '{self.name}' is at capacity")

        try:
            # Emit acquisition event
            await self._emit_event_async("acquired")
            start_time = time.time()

            result = await func(*args, **kwargs)

            # Emit success event
            execution_time = time.time() - start_time
            await self._emit_event_async("completed", execution_time=execution_time)

            return result
        except Exception as e:
            # Emit failure event
            execution_time = time.time() - start_time
            await self._emit_event_async("failed", error=str(e), execution_time=execution_time)
            raise
        finally:
            await self.pool.release()
            await self._emit_event_async("released")

    def _emit_event(self, operation: str, **data: Any) -> None:
        """Emit bulkhead event (sync)."""
        try:
            from provide.foundation.hub.events import Event, get_event_bus

            # Get pool stats synchronously
            pool_stats = self.pool.get_stats() if isinstance(self.pool, SyncResourcePool) else {}

            get_event_bus().emit(
                Event(
                    name=f"bulkhead.{operation}",
                    data={
                        "bulkhead_name": self.name,
                        "pool_stats": pool_stats,
                        **data,
                    },
                    source="bulkhead",
                )
            )
        except ImportError:
            # Events not available, continue without logging
            pass

    async def _emit_event_async(self, operation: str, **data: Any) -> None:
        """Emit bulkhead event (async)."""
        try:
            from provide.foundation.hub.events import Event, get_event_bus

            # Get pool stats asynchronously
            pool_stats = await self.pool.get_stats() if isinstance(self.pool, AsyncResourcePool) else {}

            get_event_bus().emit(
                Event(
                    name=f"bulkhead.{operation}",
                    data={
                        "bulkhead_name": self.name,
                        "pool_stats": pool_stats,
                        **data,
                    },
                    source="bulkhead",
                )
            )
        except ImportError:
            # Events not available, continue without logging
            pass

    def get_status(self) -> dict[str, Any]:
        """Get bulkhead status (sync only)."""
        if isinstance(self.pool, SyncResourcePool):
            return {
                "name": self.name,
                "pool": self.pool.get_stats(),
            }
        # Can't get async pool stats in sync context
        return {
            "name": self.name,
            "pool": {},
        }

    async def get_status_async(self) -> dict[str, Any]:
        """Get bulkhead status (async)."""
        if isinstance(self.pool, AsyncResourcePool):
            return {
                "name": self.name,
                "pool": await self.pool.get_stats(),
            }
        # Can get sync pool stats from async context via threading
        return {
            "name": self.name,
            "pool": self.pool.get_stats() if isinstance(self.pool, SyncResourcePool) else {},
        }


class BulkheadManager:
    """Manager for multiple bulkheads with different resource pools."""

    def xǁBulkheadManagerǁ__init____mutmut_orig(self) -> None:
        """Initialize bulkhead manager."""
        self._bulkheads: dict[str, Bulkhead] = {}
        self._lock = threading.RLock()

    def xǁBulkheadManagerǁ__init____mutmut_1(self) -> None:
        """Initialize bulkhead manager."""
        self._bulkheads: dict[str, Bulkhead] = None
        self._lock = threading.RLock()

    def xǁBulkheadManagerǁ__init____mutmut_2(self) -> None:
        """Initialize bulkhead manager."""
        self._bulkheads: dict[str, Bulkhead] = {}
        self._lock = None
    
    xǁBulkheadManagerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBulkheadManagerǁ__init____mutmut_1': xǁBulkheadManagerǁ__init____mutmut_1, 
        'xǁBulkheadManagerǁ__init____mutmut_2': xǁBulkheadManagerǁ__init____mutmut_2
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBulkheadManagerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁBulkheadManagerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁBulkheadManagerǁ__init____mutmut_orig)
    xǁBulkheadManagerǁ__init____mutmut_orig.__name__ = 'xǁBulkheadManagerǁ__init__'

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_orig(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_1(
        self,
        name: str,
        max_concurrent: int = 11,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_2(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 101,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_3(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 31.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_4(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = True,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_5(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_6(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = None
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_7(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=None,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_8(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=None,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_9(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=None,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_10(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_11(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_12(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_13(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = None
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_14(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=None,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_15(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=None,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_16(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=None,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_17(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_18(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_19(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        )
                self._bulkheads[name] = Bulkhead(name=name, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_20(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = None

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_21(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=None, pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_22(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, pool=None)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_23(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(pool=pool)

            return self._bulkheads[name]

    def xǁBulkheadManagerǁcreate_bulkhead__mutmut_24(
        self,
        name: str,
        max_concurrent: int = 10,
        max_queue_size: int = 100,
        timeout: float = 30.0,
        use_async_pool: bool = False,
    ) -> Bulkhead:
        """Create or get a bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent operations
            max_queue_size: Maximum queue size
            timeout: Operation timeout
            use_async_pool: If True, create AsyncResourcePool; otherwise SyncResourcePool

        Returns:
            Bulkhead instance
        """
        with self._lock:
            if name not in self._bulkheads:
                pool: SyncResourcePool | AsyncResourcePool
                if use_async_pool:
                    pool = AsyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                else:
                    pool = SyncResourcePool(
                        max_concurrent=max_concurrent,
                        max_queue_size=max_queue_size,
                        timeout=timeout,
                    )
                self._bulkheads[name] = Bulkhead(name=name, )

            return self._bulkheads[name]
    
    xǁBulkheadManagerǁcreate_bulkhead__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBulkheadManagerǁcreate_bulkhead__mutmut_1': xǁBulkheadManagerǁcreate_bulkhead__mutmut_1, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_2': xǁBulkheadManagerǁcreate_bulkhead__mutmut_2, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_3': xǁBulkheadManagerǁcreate_bulkhead__mutmut_3, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_4': xǁBulkheadManagerǁcreate_bulkhead__mutmut_4, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_5': xǁBulkheadManagerǁcreate_bulkhead__mutmut_5, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_6': xǁBulkheadManagerǁcreate_bulkhead__mutmut_6, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_7': xǁBulkheadManagerǁcreate_bulkhead__mutmut_7, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_8': xǁBulkheadManagerǁcreate_bulkhead__mutmut_8, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_9': xǁBulkheadManagerǁcreate_bulkhead__mutmut_9, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_10': xǁBulkheadManagerǁcreate_bulkhead__mutmut_10, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_11': xǁBulkheadManagerǁcreate_bulkhead__mutmut_11, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_12': xǁBulkheadManagerǁcreate_bulkhead__mutmut_12, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_13': xǁBulkheadManagerǁcreate_bulkhead__mutmut_13, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_14': xǁBulkheadManagerǁcreate_bulkhead__mutmut_14, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_15': xǁBulkheadManagerǁcreate_bulkhead__mutmut_15, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_16': xǁBulkheadManagerǁcreate_bulkhead__mutmut_16, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_17': xǁBulkheadManagerǁcreate_bulkhead__mutmut_17, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_18': xǁBulkheadManagerǁcreate_bulkhead__mutmut_18, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_19': xǁBulkheadManagerǁcreate_bulkhead__mutmut_19, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_20': xǁBulkheadManagerǁcreate_bulkhead__mutmut_20, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_21': xǁBulkheadManagerǁcreate_bulkhead__mutmut_21, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_22': xǁBulkheadManagerǁcreate_bulkhead__mutmut_22, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_23': xǁBulkheadManagerǁcreate_bulkhead__mutmut_23, 
        'xǁBulkheadManagerǁcreate_bulkhead__mutmut_24': xǁBulkheadManagerǁcreate_bulkhead__mutmut_24
    }
    
    def create_bulkhead(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBulkheadManagerǁcreate_bulkhead__mutmut_orig"), object.__getattribute__(self, "xǁBulkheadManagerǁcreate_bulkhead__mutmut_mutants"), args, kwargs, self)
        return result 
    
    create_bulkhead.__signature__ = _mutmut_signature(xǁBulkheadManagerǁcreate_bulkhead__mutmut_orig)
    xǁBulkheadManagerǁcreate_bulkhead__mutmut_orig.__name__ = 'xǁBulkheadManagerǁcreate_bulkhead'

    def xǁBulkheadManagerǁget_bulkhead__mutmut_orig(self, name: str) -> Bulkhead | None:
        """Get a bulkhead by name."""
        with self._lock:
            return self._bulkheads.get(name)

    def xǁBulkheadManagerǁget_bulkhead__mutmut_1(self, name: str) -> Bulkhead | None:
        """Get a bulkhead by name."""
        with self._lock:
            return self._bulkheads.get(None)
    
    xǁBulkheadManagerǁget_bulkhead__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBulkheadManagerǁget_bulkhead__mutmut_1': xǁBulkheadManagerǁget_bulkhead__mutmut_1
    }
    
    def get_bulkhead(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBulkheadManagerǁget_bulkhead__mutmut_orig"), object.__getattribute__(self, "xǁBulkheadManagerǁget_bulkhead__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_bulkhead.__signature__ = _mutmut_signature(xǁBulkheadManagerǁget_bulkhead__mutmut_orig)
    xǁBulkheadManagerǁget_bulkhead__mutmut_orig.__name__ = 'xǁBulkheadManagerǁget_bulkhead'

    def xǁBulkheadManagerǁlist_bulkheads__mutmut_orig(self) -> list[str]:
        """List all bulkhead names."""
        with self._lock:
            return list(self._bulkheads.keys())

    def xǁBulkheadManagerǁlist_bulkheads__mutmut_1(self) -> list[str]:
        """List all bulkhead names."""
        with self._lock:
            return list(None)
    
    xǁBulkheadManagerǁlist_bulkheads__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBulkheadManagerǁlist_bulkheads__mutmut_1': xǁBulkheadManagerǁlist_bulkheads__mutmut_1
    }
    
    def list_bulkheads(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBulkheadManagerǁlist_bulkheads__mutmut_orig"), object.__getattribute__(self, "xǁBulkheadManagerǁlist_bulkheads__mutmut_mutants"), args, kwargs, self)
        return result 
    
    list_bulkheads.__signature__ = _mutmut_signature(xǁBulkheadManagerǁlist_bulkheads__mutmut_orig)
    xǁBulkheadManagerǁlist_bulkheads__mutmut_orig.__name__ = 'xǁBulkheadManagerǁlist_bulkheads'

    def get_all_status(self) -> dict[str, dict[str, Any]]:
        """Get status of all bulkheads."""
        with self._lock:
            return {name: bulkhead.get_status() for name, bulkhead in self._bulkheads.items()}

    def xǁBulkheadManagerǁremove_bulkhead__mutmut_orig(self, name: str) -> bool:
        """Remove a bulkhead.

        Args:
            name: Bulkhead name

        Returns:
            True if removed, False if not found
        """
        with self._lock:
            if name in self._bulkheads:
                del self._bulkheads[name]
                return True
            return False

    def xǁBulkheadManagerǁremove_bulkhead__mutmut_1(self, name: str) -> bool:
        """Remove a bulkhead.

        Args:
            name: Bulkhead name

        Returns:
            True if removed, False if not found
        """
        with self._lock:
            if name not in self._bulkheads:
                del self._bulkheads[name]
                return True
            return False

    def xǁBulkheadManagerǁremove_bulkhead__mutmut_2(self, name: str) -> bool:
        """Remove a bulkhead.

        Args:
            name: Bulkhead name

        Returns:
            True if removed, False if not found
        """
        with self._lock:
            if name in self._bulkheads:
                del self._bulkheads[name]
                return False
            return False

    def xǁBulkheadManagerǁremove_bulkhead__mutmut_3(self, name: str) -> bool:
        """Remove a bulkhead.

        Args:
            name: Bulkhead name

        Returns:
            True if removed, False if not found
        """
        with self._lock:
            if name in self._bulkheads:
                del self._bulkheads[name]
                return True
            return True
    
    xǁBulkheadManagerǁremove_bulkhead__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBulkheadManagerǁremove_bulkhead__mutmut_1': xǁBulkheadManagerǁremove_bulkhead__mutmut_1, 
        'xǁBulkheadManagerǁremove_bulkhead__mutmut_2': xǁBulkheadManagerǁremove_bulkhead__mutmut_2, 
        'xǁBulkheadManagerǁremove_bulkhead__mutmut_3': xǁBulkheadManagerǁremove_bulkhead__mutmut_3
    }
    
    def remove_bulkhead(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBulkheadManagerǁremove_bulkhead__mutmut_orig"), object.__getattribute__(self, "xǁBulkheadManagerǁremove_bulkhead__mutmut_mutants"), args, kwargs, self)
        return result 
    
    remove_bulkhead.__signature__ = _mutmut_signature(xǁBulkheadManagerǁremove_bulkhead__mutmut_orig)
    xǁBulkheadManagerǁremove_bulkhead__mutmut_orig.__name__ = 'xǁBulkheadManagerǁremove_bulkhead'


# Global bulkhead manager
_bulkhead_manager = BulkheadManager()


def get_bulkhead_manager() -> BulkheadManager:
    """Get the global bulkhead manager."""
    return _bulkhead_manager


__all__ = [
    "AsyncResourcePool",
    "Bulkhead",
    "BulkheadManager",
    "SyncResourcePool",
    "get_bulkhead_manager",
]


# <3 🧱🤝💪🪄
