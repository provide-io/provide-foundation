# provide/foundation/logger/ratelimit/queue_limiter.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# queue_limiter.py
#
from collections import deque
import sys
import threading
import time
from typing import Any, Literal

"""Queue-based rate limiter with overflow protection for Foundation's logging system."""
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


class QueuedRateLimiter:
    """Rate limiter with a queue for buffering logs.
    Drops oldest messages when queue is full (FIFO overflow).

    Lifecycle Management:
        The QueuedRateLimiter requires explicit lifecycle management:
        1. Create instance: `limiter = QueuedRateLimiter(...)`
        2. Start processing: `limiter.start()`
        3. Use normally: `limiter.enqueue(item)`
        4. Shutdown cleanly: `limiter.stop()`

    Examples:
        >>> limiter = QueuedRateLimiter(capacity=100.0, refill_rate=10.0)
        >>> limiter.start()  # Start background processing
        >>> try:
        ...     limiter.enqueue(log_item)
        ... finally:
        ...     limiter.stop()  # Clean shutdown

        >>> # Or use as a context manager
        >>> with QueuedRateLimiter(100.0, 10.0) as limiter:
        ...     limiter.enqueue(log_item)  # Automatically starts and stops

    Note on Threading:
        This implementation uses threading.Thread for background processing.
        Foundation's preferred concurrency model is asyncio (see utils/rate_limiting.py
        for the async TokenBucketRateLimiter). This threading approach is maintained
        for backward compatibility with synchronous logging contexts.
    """

    def xǁQueuedRateLimiterǁ__init____mutmut_orig(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_1(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1001,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_2(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "XXdrop_oldestXX",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_3(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "DROP_OLDEST",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_4(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity < 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_5(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 1:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_6(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError(None)
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_7(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("XXCapacity must be positiveXX")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_8(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_9(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("CAPACITY MUST BE POSITIVE")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_10(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate < 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_11(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 1:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_12(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError(None)
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_13(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("XXRefill rate must be positiveXX")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_14(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_15(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("REFILL RATE MUST BE POSITIVE")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_16(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size < 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_17(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 1:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_18(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError(None)

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_19(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("XXMax queue size must be positiveXX")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_20(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_21(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("MAX QUEUE SIZE MUST BE POSITIVE")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_22(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = None
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_23(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(None)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_24(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = None
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_25(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(None)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_26(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = None
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_27(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(None)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_28(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = None

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_29(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = None
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_30(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_31(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(None) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_32(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 / 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_33(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb / 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_34(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1025 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_35(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1025) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_36(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = None

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_37(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = None
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_38(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_39(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy != "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_40(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "XXdrop_oldestXX" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_41(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "DROP_OLDEST" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_42(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = None

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_43(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = None
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_44(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 1
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_45(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = None
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_46(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 1
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_47(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = None
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_48(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 1
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_49(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = None

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_50(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 1

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_51(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = None
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_52(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = True
        self.worker_thread: threading.Thread | None = None

    def xǁQueuedRateLimiterǁ__init____mutmut_53(
        self,
        capacity: float,
        refill_rate: float,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: Literal["drop_oldest", "drop_newest", "block"] = "drop_oldest",
    ) -> None:
        """Initialize the queued rate limiter.

        Note:
            This does NOT start the worker thread automatically. Call start()
            to begin processing the queue. This allows applications to control
            the lifecycle and thread management.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            max_queue_size: Maximum number of items in queue
            max_memory_mb: Maximum memory usage in MB (estimated)
            overflow_policy: What to do when queue is full

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        if max_queue_size <= 0:
            raise ValueError("Max queue size must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

        # Queue management
        self.max_queue_size = max_queue_size
        self.max_memory_bytes = int(max_memory_mb * 1024 * 1024) if max_memory_mb else None
        self.overflow_policy = overflow_policy

        # Use deque for efficient FIFO operations
        self.pending_queue: deque[Any] = deque(
            maxlen=max_queue_size if overflow_policy == "drop_oldest" else None
        )
        self.queue_lock = threading.Lock()

        # Track statistics
        self.total_queued = 0
        self.total_dropped = 0
        self.total_processed = 0
        self.estimated_memory = 0

        # Worker thread for processing queue (not started automatically)
        self.running = False
        self.worker_thread: threading.Thread | None = ""
    
    xǁQueuedRateLimiterǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁQueuedRateLimiterǁ__init____mutmut_1': xǁQueuedRateLimiterǁ__init____mutmut_1, 
        'xǁQueuedRateLimiterǁ__init____mutmut_2': xǁQueuedRateLimiterǁ__init____mutmut_2, 
        'xǁQueuedRateLimiterǁ__init____mutmut_3': xǁQueuedRateLimiterǁ__init____mutmut_3, 
        'xǁQueuedRateLimiterǁ__init____mutmut_4': xǁQueuedRateLimiterǁ__init____mutmut_4, 
        'xǁQueuedRateLimiterǁ__init____mutmut_5': xǁQueuedRateLimiterǁ__init____mutmut_5, 
        'xǁQueuedRateLimiterǁ__init____mutmut_6': xǁQueuedRateLimiterǁ__init____mutmut_6, 
        'xǁQueuedRateLimiterǁ__init____mutmut_7': xǁQueuedRateLimiterǁ__init____mutmut_7, 
        'xǁQueuedRateLimiterǁ__init____mutmut_8': xǁQueuedRateLimiterǁ__init____mutmut_8, 
        'xǁQueuedRateLimiterǁ__init____mutmut_9': xǁQueuedRateLimiterǁ__init____mutmut_9, 
        'xǁQueuedRateLimiterǁ__init____mutmut_10': xǁQueuedRateLimiterǁ__init____mutmut_10, 
        'xǁQueuedRateLimiterǁ__init____mutmut_11': xǁQueuedRateLimiterǁ__init____mutmut_11, 
        'xǁQueuedRateLimiterǁ__init____mutmut_12': xǁQueuedRateLimiterǁ__init____mutmut_12, 
        'xǁQueuedRateLimiterǁ__init____mutmut_13': xǁQueuedRateLimiterǁ__init____mutmut_13, 
        'xǁQueuedRateLimiterǁ__init____mutmut_14': xǁQueuedRateLimiterǁ__init____mutmut_14, 
        'xǁQueuedRateLimiterǁ__init____mutmut_15': xǁQueuedRateLimiterǁ__init____mutmut_15, 
        'xǁQueuedRateLimiterǁ__init____mutmut_16': xǁQueuedRateLimiterǁ__init____mutmut_16, 
        'xǁQueuedRateLimiterǁ__init____mutmut_17': xǁQueuedRateLimiterǁ__init____mutmut_17, 
        'xǁQueuedRateLimiterǁ__init____mutmut_18': xǁQueuedRateLimiterǁ__init____mutmut_18, 
        'xǁQueuedRateLimiterǁ__init____mutmut_19': xǁQueuedRateLimiterǁ__init____mutmut_19, 
        'xǁQueuedRateLimiterǁ__init____mutmut_20': xǁQueuedRateLimiterǁ__init____mutmut_20, 
        'xǁQueuedRateLimiterǁ__init____mutmut_21': xǁQueuedRateLimiterǁ__init____mutmut_21, 
        'xǁQueuedRateLimiterǁ__init____mutmut_22': xǁQueuedRateLimiterǁ__init____mutmut_22, 
        'xǁQueuedRateLimiterǁ__init____mutmut_23': xǁQueuedRateLimiterǁ__init____mutmut_23, 
        'xǁQueuedRateLimiterǁ__init____mutmut_24': xǁQueuedRateLimiterǁ__init____mutmut_24, 
        'xǁQueuedRateLimiterǁ__init____mutmut_25': xǁQueuedRateLimiterǁ__init____mutmut_25, 
        'xǁQueuedRateLimiterǁ__init____mutmut_26': xǁQueuedRateLimiterǁ__init____mutmut_26, 
        'xǁQueuedRateLimiterǁ__init____mutmut_27': xǁQueuedRateLimiterǁ__init____mutmut_27, 
        'xǁQueuedRateLimiterǁ__init____mutmut_28': xǁQueuedRateLimiterǁ__init____mutmut_28, 
        'xǁQueuedRateLimiterǁ__init____mutmut_29': xǁQueuedRateLimiterǁ__init____mutmut_29, 
        'xǁQueuedRateLimiterǁ__init____mutmut_30': xǁQueuedRateLimiterǁ__init____mutmut_30, 
        'xǁQueuedRateLimiterǁ__init____mutmut_31': xǁQueuedRateLimiterǁ__init____mutmut_31, 
        'xǁQueuedRateLimiterǁ__init____mutmut_32': xǁQueuedRateLimiterǁ__init____mutmut_32, 
        'xǁQueuedRateLimiterǁ__init____mutmut_33': xǁQueuedRateLimiterǁ__init____mutmut_33, 
        'xǁQueuedRateLimiterǁ__init____mutmut_34': xǁQueuedRateLimiterǁ__init____mutmut_34, 
        'xǁQueuedRateLimiterǁ__init____mutmut_35': xǁQueuedRateLimiterǁ__init____mutmut_35, 
        'xǁQueuedRateLimiterǁ__init____mutmut_36': xǁQueuedRateLimiterǁ__init____mutmut_36, 
        'xǁQueuedRateLimiterǁ__init____mutmut_37': xǁQueuedRateLimiterǁ__init____mutmut_37, 
        'xǁQueuedRateLimiterǁ__init____mutmut_38': xǁQueuedRateLimiterǁ__init____mutmut_38, 
        'xǁQueuedRateLimiterǁ__init____mutmut_39': xǁQueuedRateLimiterǁ__init____mutmut_39, 
        'xǁQueuedRateLimiterǁ__init____mutmut_40': xǁQueuedRateLimiterǁ__init____mutmut_40, 
        'xǁQueuedRateLimiterǁ__init____mutmut_41': xǁQueuedRateLimiterǁ__init____mutmut_41, 
        'xǁQueuedRateLimiterǁ__init____mutmut_42': xǁQueuedRateLimiterǁ__init____mutmut_42, 
        'xǁQueuedRateLimiterǁ__init____mutmut_43': xǁQueuedRateLimiterǁ__init____mutmut_43, 
        'xǁQueuedRateLimiterǁ__init____mutmut_44': xǁQueuedRateLimiterǁ__init____mutmut_44, 
        'xǁQueuedRateLimiterǁ__init____mutmut_45': xǁQueuedRateLimiterǁ__init____mutmut_45, 
        'xǁQueuedRateLimiterǁ__init____mutmut_46': xǁQueuedRateLimiterǁ__init____mutmut_46, 
        'xǁQueuedRateLimiterǁ__init____mutmut_47': xǁQueuedRateLimiterǁ__init____mutmut_47, 
        'xǁQueuedRateLimiterǁ__init____mutmut_48': xǁQueuedRateLimiterǁ__init____mutmut_48, 
        'xǁQueuedRateLimiterǁ__init____mutmut_49': xǁQueuedRateLimiterǁ__init____mutmut_49, 
        'xǁQueuedRateLimiterǁ__init____mutmut_50': xǁQueuedRateLimiterǁ__init____mutmut_50, 
        'xǁQueuedRateLimiterǁ__init____mutmut_51': xǁQueuedRateLimiterǁ__init____mutmut_51, 
        'xǁQueuedRateLimiterǁ__init____mutmut_52': xǁQueuedRateLimiterǁ__init____mutmut_52, 
        'xǁQueuedRateLimiterǁ__init____mutmut_53': xǁQueuedRateLimiterǁ__init____mutmut_53
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁQueuedRateLimiterǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁQueuedRateLimiterǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁQueuedRateLimiterǁ__init____mutmut_orig)
    xǁQueuedRateLimiterǁ__init____mutmut_orig.__name__ = 'xǁQueuedRateLimiterǁ__init__'

    def xǁQueuedRateLimiterǁstart__mutmut_orig(self) -> None:
        """Start the worker thread for processing queued items.

        This should be called after initialization and before enqueuing items.
        Can be called multiple times (subsequent calls are no-ops if already running).

        Raises:
            RuntimeError: If start() is called after stop() on the same instance
        """
        if self.running:
            # Already running, no-op
            return

        if self.worker_thread is not None and self.worker_thread.is_alive():
            # Thread exists and is alive, no-op
            return

        # Start new worker thread
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def xǁQueuedRateLimiterǁstart__mutmut_1(self) -> None:
        """Start the worker thread for processing queued items.

        This should be called after initialization and before enqueuing items.
        Can be called multiple times (subsequent calls are no-ops if already running).

        Raises:
            RuntimeError: If start() is called after stop() on the same instance
        """
        if self.running:
            # Already running, no-op
            return

        if self.worker_thread is not None or self.worker_thread.is_alive():
            # Thread exists and is alive, no-op
            return

        # Start new worker thread
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def xǁQueuedRateLimiterǁstart__mutmut_2(self) -> None:
        """Start the worker thread for processing queued items.

        This should be called after initialization and before enqueuing items.
        Can be called multiple times (subsequent calls are no-ops if already running).

        Raises:
            RuntimeError: If start() is called after stop() on the same instance
        """
        if self.running:
            # Already running, no-op
            return

        if self.worker_thread is None and self.worker_thread.is_alive():
            # Thread exists and is alive, no-op
            return

        # Start new worker thread
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def xǁQueuedRateLimiterǁstart__mutmut_3(self) -> None:
        """Start the worker thread for processing queued items.

        This should be called after initialization and before enqueuing items.
        Can be called multiple times (subsequent calls are no-ops if already running).

        Raises:
            RuntimeError: If start() is called after stop() on the same instance
        """
        if self.running:
            # Already running, no-op
            return

        if self.worker_thread is not None and self.worker_thread.is_alive():
            # Thread exists and is alive, no-op
            return

        # Start new worker thread
        self.running = None
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def xǁQueuedRateLimiterǁstart__mutmut_4(self) -> None:
        """Start the worker thread for processing queued items.

        This should be called after initialization and before enqueuing items.
        Can be called multiple times (subsequent calls are no-ops if already running).

        Raises:
            RuntimeError: If start() is called after stop() on the same instance
        """
        if self.running:
            # Already running, no-op
            return

        if self.worker_thread is not None and self.worker_thread.is_alive():
            # Thread exists and is alive, no-op
            return

        # Start new worker thread
        self.running = False
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def xǁQueuedRateLimiterǁstart__mutmut_5(self) -> None:
        """Start the worker thread for processing queued items.

        This should be called after initialization and before enqueuing items.
        Can be called multiple times (subsequent calls are no-ops if already running).

        Raises:
            RuntimeError: If start() is called after stop() on the same instance
        """
        if self.running:
            # Already running, no-op
            return

        if self.worker_thread is not None and self.worker_thread.is_alive():
            # Thread exists and is alive, no-op
            return

        # Start new worker thread
        self.running = True
        self.worker_thread = None
        self.worker_thread.start()

    def xǁQueuedRateLimiterǁstart__mutmut_6(self) -> None:
        """Start the worker thread for processing queued items.

        This should be called after initialization and before enqueuing items.
        Can be called multiple times (subsequent calls are no-ops if already running).

        Raises:
            RuntimeError: If start() is called after stop() on the same instance
        """
        if self.running:
            # Already running, no-op
            return

        if self.worker_thread is not None and self.worker_thread.is_alive():
            # Thread exists and is alive, no-op
            return

        # Start new worker thread
        self.running = True
        self.worker_thread = threading.Thread(target=None, daemon=True)
        self.worker_thread.start()

    def xǁQueuedRateLimiterǁstart__mutmut_7(self) -> None:
        """Start the worker thread for processing queued items.

        This should be called after initialization and before enqueuing items.
        Can be called multiple times (subsequent calls are no-ops if already running).

        Raises:
            RuntimeError: If start() is called after stop() on the same instance
        """
        if self.running:
            # Already running, no-op
            return

        if self.worker_thread is not None and self.worker_thread.is_alive():
            # Thread exists and is alive, no-op
            return

        # Start new worker thread
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=None)
        self.worker_thread.start()

    def xǁQueuedRateLimiterǁstart__mutmut_8(self) -> None:
        """Start the worker thread for processing queued items.

        This should be called after initialization and before enqueuing items.
        Can be called multiple times (subsequent calls are no-ops if already running).

        Raises:
            RuntimeError: If start() is called after stop() on the same instance
        """
        if self.running:
            # Already running, no-op
            return

        if self.worker_thread is not None and self.worker_thread.is_alive():
            # Thread exists and is alive, no-op
            return

        # Start new worker thread
        self.running = True
        self.worker_thread = threading.Thread(daemon=True)
        self.worker_thread.start()

    def xǁQueuedRateLimiterǁstart__mutmut_9(self) -> None:
        """Start the worker thread for processing queued items.

        This should be called after initialization and before enqueuing items.
        Can be called multiple times (subsequent calls are no-ops if already running).

        Raises:
            RuntimeError: If start() is called after stop() on the same instance
        """
        if self.running:
            # Already running, no-op
            return

        if self.worker_thread is not None and self.worker_thread.is_alive():
            # Thread exists and is alive, no-op
            return

        # Start new worker thread
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_queue, )
        self.worker_thread.start()

    def xǁQueuedRateLimiterǁstart__mutmut_10(self) -> None:
        """Start the worker thread for processing queued items.

        This should be called after initialization and before enqueuing items.
        Can be called multiple times (subsequent calls are no-ops if already running).

        Raises:
            RuntimeError: If start() is called after stop() on the same instance
        """
        if self.running:
            # Already running, no-op
            return

        if self.worker_thread is not None and self.worker_thread.is_alive():
            # Thread exists and is alive, no-op
            return

        # Start new worker thread
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=False)
        self.worker_thread.start()
    
    xǁQueuedRateLimiterǁstart__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁQueuedRateLimiterǁstart__mutmut_1': xǁQueuedRateLimiterǁstart__mutmut_1, 
        'xǁQueuedRateLimiterǁstart__mutmut_2': xǁQueuedRateLimiterǁstart__mutmut_2, 
        'xǁQueuedRateLimiterǁstart__mutmut_3': xǁQueuedRateLimiterǁstart__mutmut_3, 
        'xǁQueuedRateLimiterǁstart__mutmut_4': xǁQueuedRateLimiterǁstart__mutmut_4, 
        'xǁQueuedRateLimiterǁstart__mutmut_5': xǁQueuedRateLimiterǁstart__mutmut_5, 
        'xǁQueuedRateLimiterǁstart__mutmut_6': xǁQueuedRateLimiterǁstart__mutmut_6, 
        'xǁQueuedRateLimiterǁstart__mutmut_7': xǁQueuedRateLimiterǁstart__mutmut_7, 
        'xǁQueuedRateLimiterǁstart__mutmut_8': xǁQueuedRateLimiterǁstart__mutmut_8, 
        'xǁQueuedRateLimiterǁstart__mutmut_9': xǁQueuedRateLimiterǁstart__mutmut_9, 
        'xǁQueuedRateLimiterǁstart__mutmut_10': xǁQueuedRateLimiterǁstart__mutmut_10
    }
    
    def start(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁQueuedRateLimiterǁstart__mutmut_orig"), object.__getattribute__(self, "xǁQueuedRateLimiterǁstart__mutmut_mutants"), args, kwargs, self)
        return result 
    
    start.__signature__ = _mutmut_signature(xǁQueuedRateLimiterǁstart__mutmut_orig)
    xǁQueuedRateLimiterǁstart__mutmut_orig.__name__ = 'xǁQueuedRateLimiterǁstart'

    def xǁQueuedRateLimiterǁstop__mutmut_orig(self, timeout: float = 1.0) -> None:
        """Stop the worker thread and wait for it to finish.

        This provides a clean shutdown, allowing the worker to finish processing
        the current item before terminating.

        Args:
            timeout: Maximum seconds to wait for thread to finish (default: 1.0)

        Example:
            >>> limiter.stop(timeout=2.0)  # Wait up to 2 seconds for clean shutdown
        """
        self.running = False
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=timeout)

    def xǁQueuedRateLimiterǁstop__mutmut_1(self, timeout: float = 2.0) -> None:
        """Stop the worker thread and wait for it to finish.

        This provides a clean shutdown, allowing the worker to finish processing
        the current item before terminating.

        Args:
            timeout: Maximum seconds to wait for thread to finish (default: 1.0)

        Example:
            >>> limiter.stop(timeout=2.0)  # Wait up to 2 seconds for clean shutdown
        """
        self.running = False
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=timeout)

    def xǁQueuedRateLimiterǁstop__mutmut_2(self, timeout: float = 1.0) -> None:
        """Stop the worker thread and wait for it to finish.

        This provides a clean shutdown, allowing the worker to finish processing
        the current item before terminating.

        Args:
            timeout: Maximum seconds to wait for thread to finish (default: 1.0)

        Example:
            >>> limiter.stop(timeout=2.0)  # Wait up to 2 seconds for clean shutdown
        """
        self.running = None
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=timeout)

    def xǁQueuedRateLimiterǁstop__mutmut_3(self, timeout: float = 1.0) -> None:
        """Stop the worker thread and wait for it to finish.

        This provides a clean shutdown, allowing the worker to finish processing
        the current item before terminating.

        Args:
            timeout: Maximum seconds to wait for thread to finish (default: 1.0)

        Example:
            >>> limiter.stop(timeout=2.0)  # Wait up to 2 seconds for clean shutdown
        """
        self.running = True
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=timeout)

    def xǁQueuedRateLimiterǁstop__mutmut_4(self, timeout: float = 1.0) -> None:
        """Stop the worker thread and wait for it to finish.

        This provides a clean shutdown, allowing the worker to finish processing
        the current item before terminating.

        Args:
            timeout: Maximum seconds to wait for thread to finish (default: 1.0)

        Example:
            >>> limiter.stop(timeout=2.0)  # Wait up to 2 seconds for clean shutdown
        """
        self.running = False
        if self.worker_thread or self.worker_thread.is_alive():
            self.worker_thread.join(timeout=timeout)

    def xǁQueuedRateLimiterǁstop__mutmut_5(self, timeout: float = 1.0) -> None:
        """Stop the worker thread and wait for it to finish.

        This provides a clean shutdown, allowing the worker to finish processing
        the current item before terminating.

        Args:
            timeout: Maximum seconds to wait for thread to finish (default: 1.0)

        Example:
            >>> limiter.stop(timeout=2.0)  # Wait up to 2 seconds for clean shutdown
        """
        self.running = False
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=None)
    
    xǁQueuedRateLimiterǁstop__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁQueuedRateLimiterǁstop__mutmut_1': xǁQueuedRateLimiterǁstop__mutmut_1, 
        'xǁQueuedRateLimiterǁstop__mutmut_2': xǁQueuedRateLimiterǁstop__mutmut_2, 
        'xǁQueuedRateLimiterǁstop__mutmut_3': xǁQueuedRateLimiterǁstop__mutmut_3, 
        'xǁQueuedRateLimiterǁstop__mutmut_4': xǁQueuedRateLimiterǁstop__mutmut_4, 
        'xǁQueuedRateLimiterǁstop__mutmut_5': xǁQueuedRateLimiterǁstop__mutmut_5
    }
    
    def stop(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁQueuedRateLimiterǁstop__mutmut_orig"), object.__getattribute__(self, "xǁQueuedRateLimiterǁstop__mutmut_mutants"), args, kwargs, self)
        return result 
    
    stop.__signature__ = _mutmut_signature(xǁQueuedRateLimiterǁstop__mutmut_orig)
    xǁQueuedRateLimiterǁstop__mutmut_orig.__name__ = 'xǁQueuedRateLimiterǁstop'

    def __enter__(self) -> QueuedRateLimiter:
        """Enter context manager, automatically starting the worker thread.

        Returns:
            Self for use in with statement

        Example:
            >>> with QueuedRateLimiter(100.0, 10.0) as limiter:
            ...     limiter.enqueue(item)
        """
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager, automatically stopping the worker thread.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        self.stop()

    def xǁQueuedRateLimiterǁ_estimate_size__mutmut_orig(self, item: Any) -> int:
        """Estimate memory size of an item."""
        # Simple estimation - can be made more sophisticated
        return sys.getsizeof(item)

    def xǁQueuedRateLimiterǁ_estimate_size__mutmut_1(self, item: Any) -> int:
        """Estimate memory size of an item."""
        # Simple estimation - can be made more sophisticated
        return sys.getsizeof(None)
    
    xǁQueuedRateLimiterǁ_estimate_size__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁQueuedRateLimiterǁ_estimate_size__mutmut_1': xǁQueuedRateLimiterǁ_estimate_size__mutmut_1
    }
    
    def _estimate_size(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁQueuedRateLimiterǁ_estimate_size__mutmut_orig"), object.__getattribute__(self, "xǁQueuedRateLimiterǁ_estimate_size__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _estimate_size.__signature__ = _mutmut_signature(xǁQueuedRateLimiterǁ_estimate_size__mutmut_orig)
    xǁQueuedRateLimiterǁ_estimate_size__mutmut_orig.__name__ = 'xǁQueuedRateLimiterǁ_estimate_size'

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_orig(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill

        if elapsed > 0:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = now

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_1(self) -> None:
        """Refill tokens based on elapsed time."""
        now = None
        elapsed = now - self.last_refill

        if elapsed > 0:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = now

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_2(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = None

        if elapsed > 0:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = now

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_3(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now + self.last_refill

        if elapsed > 0:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = now

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_4(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill

        if elapsed >= 0:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = now

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_5(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill

        if elapsed > 1:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = now

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_6(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill

        if elapsed > 0:
            tokens_to_add = None
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = now

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_7(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill

        if elapsed > 0:
            tokens_to_add = elapsed / self.refill_rate
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = now

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_8(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill

        if elapsed > 0:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = None
            self.last_refill = now

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_9(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill

        if elapsed > 0:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(None, self.tokens + tokens_to_add)
            self.last_refill = now

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_10(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill

        if elapsed > 0:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, None)
            self.last_refill = now

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_11(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill

        if elapsed > 0:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.tokens + tokens_to_add)
            self.last_refill = now

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_12(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill

        if elapsed > 0:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, )
            self.last_refill = now

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_13(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill

        if elapsed > 0:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens - tokens_to_add)
            self.last_refill = now

    def xǁQueuedRateLimiterǁ_refill_tokens__mutmut_14(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill

        if elapsed > 0:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = None
    
    xǁQueuedRateLimiterǁ_refill_tokens__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁQueuedRateLimiterǁ_refill_tokens__mutmut_1': xǁQueuedRateLimiterǁ_refill_tokens__mutmut_1, 
        'xǁQueuedRateLimiterǁ_refill_tokens__mutmut_2': xǁQueuedRateLimiterǁ_refill_tokens__mutmut_2, 
        'xǁQueuedRateLimiterǁ_refill_tokens__mutmut_3': xǁQueuedRateLimiterǁ_refill_tokens__mutmut_3, 
        'xǁQueuedRateLimiterǁ_refill_tokens__mutmut_4': xǁQueuedRateLimiterǁ_refill_tokens__mutmut_4, 
        'xǁQueuedRateLimiterǁ_refill_tokens__mutmut_5': xǁQueuedRateLimiterǁ_refill_tokens__mutmut_5, 
        'xǁQueuedRateLimiterǁ_refill_tokens__mutmut_6': xǁQueuedRateLimiterǁ_refill_tokens__mutmut_6, 
        'xǁQueuedRateLimiterǁ_refill_tokens__mutmut_7': xǁQueuedRateLimiterǁ_refill_tokens__mutmut_7, 
        'xǁQueuedRateLimiterǁ_refill_tokens__mutmut_8': xǁQueuedRateLimiterǁ_refill_tokens__mutmut_8, 
        'xǁQueuedRateLimiterǁ_refill_tokens__mutmut_9': xǁQueuedRateLimiterǁ_refill_tokens__mutmut_9, 
        'xǁQueuedRateLimiterǁ_refill_tokens__mutmut_10': xǁQueuedRateLimiterǁ_refill_tokens__mutmut_10, 
        'xǁQueuedRateLimiterǁ_refill_tokens__mutmut_11': xǁQueuedRateLimiterǁ_refill_tokens__mutmut_11, 
        'xǁQueuedRateLimiterǁ_refill_tokens__mutmut_12': xǁQueuedRateLimiterǁ_refill_tokens__mutmut_12, 
        'xǁQueuedRateLimiterǁ_refill_tokens__mutmut_13': xǁQueuedRateLimiterǁ_refill_tokens__mutmut_13, 
        'xǁQueuedRateLimiterǁ_refill_tokens__mutmut_14': xǁQueuedRateLimiterǁ_refill_tokens__mutmut_14
    }
    
    def _refill_tokens(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁQueuedRateLimiterǁ_refill_tokens__mutmut_orig"), object.__getattribute__(self, "xǁQueuedRateLimiterǁ_refill_tokens__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _refill_tokens.__signature__ = _mutmut_signature(xǁQueuedRateLimiterǁ_refill_tokens__mutmut_orig)
    xǁQueuedRateLimiterǁ_refill_tokens__mutmut_orig.__name__ = 'xǁQueuedRateLimiterǁ_refill_tokens'

    def xǁQueuedRateLimiterǁenqueue__mutmut_orig(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_1(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = None
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_2(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(None)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_3(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory - item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_4(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size >= self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_5(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped = 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_6(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped -= 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_7(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 2
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_8(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        True,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_9(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 * 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_10(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory * 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_11(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1025 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_12(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1025:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_13(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) > self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_14(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy != "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_15(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "XXdrop_newestXX":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_16(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "DROP_NEWEST":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_17(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped = 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_18(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped -= 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_19(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 2
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_20(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return True, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_21(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy != "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_22(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "XXdrop_oldestXX":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_23(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "DROP_OLDEST":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_24(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) >= 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_25(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 1:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_26(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = None
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_27(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[1] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_28(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) != self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_29(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item or self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_30(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory = self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_31(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory += self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_32(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(None)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_33(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped = 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_34(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped -= 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_35(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 2
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_36(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy != "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_37(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "XXblockXX":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_38(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "BLOCK":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_39(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return True, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_40(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "XXQueue full (blocking not implemented)XX"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_41(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_42(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "QUEUE FULL (BLOCKING NOT IMPLEMENTED)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_43(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(None)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_44(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued = 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_45(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued -= 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_46(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 2

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_47(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory = self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_48(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory -= self._estimate_size(item)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_49(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(None)

            return True, None

    def xǁQueuedRateLimiterǁenqueue__mutmut_50(self, item: Any) -> tuple[bool, str | None]:
        """Add item to queue for rate-limited processing.

        Returns:
            Tuple of (accepted, reason) where reason is set if rejected

        """
        with self.queue_lock:
            # Check memory limit
            if self.max_memory_bytes:
                item_size = self._estimate_size(item)
                if self.estimated_memory + item_size > self.max_memory_bytes:
                    self.total_dropped += 1
                    return (
                        False,
                        f"Memory limit exceeded ({self.estimated_memory / 1024 / 1024:.1f}MB)",
                    )

            # Check queue size
            if len(self.pending_queue) >= self.max_queue_size:
                if self.overflow_policy == "drop_newest":
                    self.total_dropped += 1
                    return False, f"Queue full ({self.max_queue_size} items)"
                if self.overflow_policy == "drop_oldest":
                    # deque with maxlen automatically drops oldest
                    if len(self.pending_queue) > 0:
                        old_item = (
                            self.pending_queue[0] if len(self.pending_queue) == self.max_queue_size else None
                        )
                        if old_item and self.max_memory_bytes:
                            self.estimated_memory -= self._estimate_size(old_item)
                        self.total_dropped += 1
                elif self.overflow_policy == "block":
                    # In block mode, we would need to wait
                    # For now, just reject
                    return False, "Queue full (blocking not implemented)"

            # Add to queue
            self.pending_queue.append(item)
            self.total_queued += 1

            if self.max_memory_bytes:
                self.estimated_memory += self._estimate_size(item)

            return False, None
    
    xǁQueuedRateLimiterǁenqueue__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁQueuedRateLimiterǁenqueue__mutmut_1': xǁQueuedRateLimiterǁenqueue__mutmut_1, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_2': xǁQueuedRateLimiterǁenqueue__mutmut_2, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_3': xǁQueuedRateLimiterǁenqueue__mutmut_3, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_4': xǁQueuedRateLimiterǁenqueue__mutmut_4, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_5': xǁQueuedRateLimiterǁenqueue__mutmut_5, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_6': xǁQueuedRateLimiterǁenqueue__mutmut_6, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_7': xǁQueuedRateLimiterǁenqueue__mutmut_7, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_8': xǁQueuedRateLimiterǁenqueue__mutmut_8, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_9': xǁQueuedRateLimiterǁenqueue__mutmut_9, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_10': xǁQueuedRateLimiterǁenqueue__mutmut_10, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_11': xǁQueuedRateLimiterǁenqueue__mutmut_11, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_12': xǁQueuedRateLimiterǁenqueue__mutmut_12, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_13': xǁQueuedRateLimiterǁenqueue__mutmut_13, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_14': xǁQueuedRateLimiterǁenqueue__mutmut_14, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_15': xǁQueuedRateLimiterǁenqueue__mutmut_15, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_16': xǁQueuedRateLimiterǁenqueue__mutmut_16, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_17': xǁQueuedRateLimiterǁenqueue__mutmut_17, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_18': xǁQueuedRateLimiterǁenqueue__mutmut_18, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_19': xǁQueuedRateLimiterǁenqueue__mutmut_19, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_20': xǁQueuedRateLimiterǁenqueue__mutmut_20, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_21': xǁQueuedRateLimiterǁenqueue__mutmut_21, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_22': xǁQueuedRateLimiterǁenqueue__mutmut_22, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_23': xǁQueuedRateLimiterǁenqueue__mutmut_23, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_24': xǁQueuedRateLimiterǁenqueue__mutmut_24, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_25': xǁQueuedRateLimiterǁenqueue__mutmut_25, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_26': xǁQueuedRateLimiterǁenqueue__mutmut_26, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_27': xǁQueuedRateLimiterǁenqueue__mutmut_27, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_28': xǁQueuedRateLimiterǁenqueue__mutmut_28, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_29': xǁQueuedRateLimiterǁenqueue__mutmut_29, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_30': xǁQueuedRateLimiterǁenqueue__mutmut_30, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_31': xǁQueuedRateLimiterǁenqueue__mutmut_31, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_32': xǁQueuedRateLimiterǁenqueue__mutmut_32, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_33': xǁQueuedRateLimiterǁenqueue__mutmut_33, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_34': xǁQueuedRateLimiterǁenqueue__mutmut_34, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_35': xǁQueuedRateLimiterǁenqueue__mutmut_35, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_36': xǁQueuedRateLimiterǁenqueue__mutmut_36, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_37': xǁQueuedRateLimiterǁenqueue__mutmut_37, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_38': xǁQueuedRateLimiterǁenqueue__mutmut_38, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_39': xǁQueuedRateLimiterǁenqueue__mutmut_39, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_40': xǁQueuedRateLimiterǁenqueue__mutmut_40, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_41': xǁQueuedRateLimiterǁenqueue__mutmut_41, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_42': xǁQueuedRateLimiterǁenqueue__mutmut_42, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_43': xǁQueuedRateLimiterǁenqueue__mutmut_43, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_44': xǁQueuedRateLimiterǁenqueue__mutmut_44, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_45': xǁQueuedRateLimiterǁenqueue__mutmut_45, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_46': xǁQueuedRateLimiterǁenqueue__mutmut_46, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_47': xǁQueuedRateLimiterǁenqueue__mutmut_47, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_48': xǁQueuedRateLimiterǁenqueue__mutmut_48, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_49': xǁQueuedRateLimiterǁenqueue__mutmut_49, 
        'xǁQueuedRateLimiterǁenqueue__mutmut_50': xǁQueuedRateLimiterǁenqueue__mutmut_50
    }
    
    def enqueue(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁQueuedRateLimiterǁenqueue__mutmut_orig"), object.__getattribute__(self, "xǁQueuedRateLimiterǁenqueue__mutmut_mutants"), args, kwargs, self)
        return result 
    
    enqueue.__signature__ = _mutmut_signature(xǁQueuedRateLimiterǁenqueue__mutmut_orig)
    xǁQueuedRateLimiterǁenqueue__mutmut_orig.__name__ = 'xǁQueuedRateLimiterǁenqueue'

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_orig(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens -= 1.0
                    self.total_processed += 1

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_1(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 or self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens -= 1.0
                    self.total_processed += 1

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_2(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens > 1.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens -= 1.0
                    self.total_processed += 1

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_3(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 2.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens -= 1.0
                    self.total_processed += 1

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_4(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 and self.pending_queue:
                    item = None
                    self.tokens -= 1.0
                    self.total_processed += 1

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_5(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens = 1.0
                    self.total_processed += 1

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_6(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens += 1.0
                    self.total_processed += 1

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_7(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens -= 2.0
                    self.total_processed += 1

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_8(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens -= 1.0
                    self.total_processed = 1

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_9(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens -= 1.0
                    self.total_processed -= 1

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_10(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens -= 1.0
                    self.total_processed += 2

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_11(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens -= 1.0
                    self.total_processed += 1

                    if self.max_memory_bytes:
                        self.estimated_memory = self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_12(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens -= 1.0
                    self.total_processed += 1

                    if self.max_memory_bytes:
                        self.estimated_memory += self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_13(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens -= 1.0
                    self.total_processed += 1

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(None)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_14(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens -= 1.0
                    self.total_processed += 1

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(None)

            # Sleep briefly to avoid busy waiting
            time.sleep(0.01)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_15(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens -= 1.0
                    self.total_processed += 1

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(None)

    def xǁQueuedRateLimiterǁ_process_queue__mutmut_16(self) -> None:
        """Worker thread that processes queued items."""
        while self.running:
            with self.queue_lock:
                self._refill_tokens()

                # Process items while we have tokens
                while self.tokens >= 1.0 and self.pending_queue:
                    item = self.pending_queue.popleft()
                    self.tokens -= 1.0
                    self.total_processed += 1

                    if self.max_memory_bytes:
                        self.estimated_memory -= self._estimate_size(item)

                    # Here we would actually process the item
                    # For logging, this would mean emitting the log
                    self._process_item(item)

            # Sleep briefly to avoid busy waiting
            time.sleep(1.01)
    
    xǁQueuedRateLimiterǁ_process_queue__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁQueuedRateLimiterǁ_process_queue__mutmut_1': xǁQueuedRateLimiterǁ_process_queue__mutmut_1, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_2': xǁQueuedRateLimiterǁ_process_queue__mutmut_2, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_3': xǁQueuedRateLimiterǁ_process_queue__mutmut_3, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_4': xǁQueuedRateLimiterǁ_process_queue__mutmut_4, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_5': xǁQueuedRateLimiterǁ_process_queue__mutmut_5, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_6': xǁQueuedRateLimiterǁ_process_queue__mutmut_6, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_7': xǁQueuedRateLimiterǁ_process_queue__mutmut_7, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_8': xǁQueuedRateLimiterǁ_process_queue__mutmut_8, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_9': xǁQueuedRateLimiterǁ_process_queue__mutmut_9, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_10': xǁQueuedRateLimiterǁ_process_queue__mutmut_10, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_11': xǁQueuedRateLimiterǁ_process_queue__mutmut_11, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_12': xǁQueuedRateLimiterǁ_process_queue__mutmut_12, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_13': xǁQueuedRateLimiterǁ_process_queue__mutmut_13, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_14': xǁQueuedRateLimiterǁ_process_queue__mutmut_14, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_15': xǁQueuedRateLimiterǁ_process_queue__mutmut_15, 
        'xǁQueuedRateLimiterǁ_process_queue__mutmut_16': xǁQueuedRateLimiterǁ_process_queue__mutmut_16
    }
    
    def _process_queue(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁQueuedRateLimiterǁ_process_queue__mutmut_orig"), object.__getattribute__(self, "xǁQueuedRateLimiterǁ_process_queue__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _process_queue.__signature__ = _mutmut_signature(xǁQueuedRateLimiterǁ_process_queue__mutmut_orig)
    xǁQueuedRateLimiterǁ_process_queue__mutmut_orig.__name__ = 'xǁQueuedRateLimiterǁ_process_queue'

    def _process_item(self, item: Any) -> None:
        """Process a single item from the queue."""
        # This would be overridden to actually emit the log

    def xǁQueuedRateLimiterǁget_stats__mutmut_orig(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_1(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "XXqueue_sizeXX": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_2(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "QUEUE_SIZE": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_3(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "XXmax_queue_sizeXX": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_4(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "MAX_QUEUE_SIZE": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_5(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "XXtokens_availableXX": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_6(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "TOKENS_AVAILABLE": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_7(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "XXcapacityXX": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_8(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "CAPACITY": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_9(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "XXrefill_rateXX": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_10(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "REFILL_RATE": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_11(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "XXtotal_queuedXX": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_12(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "TOTAL_QUEUED": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_13(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "XXtotal_droppedXX": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_14(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "TOTAL_DROPPED": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_15(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "XXtotal_processedXX": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_16(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "TOTAL_PROCESSED": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_17(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "XXestimated_memory_mbXX": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_18(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "ESTIMATED_MEMORY_MB": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_19(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 * 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_20(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory * 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_21(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1025 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_22(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1025 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_23(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "XXmax_memory_mbXX": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_24(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "MAX_MEMORY_MB": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_25(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 * 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_26(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes * 1024 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_27(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1025 / 1024 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_28(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1025 if self.max_memory_bytes else None,
                "overflow_policy": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_29(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "XXoverflow_policyXX": self.overflow_policy,
            }

    def xǁQueuedRateLimiterǁget_stats__mutmut_30(self) -> dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            return {
                "queue_size": len(self.pending_queue),
                "max_queue_size": self.max_queue_size,
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_queued": self.total_queued,
                "total_dropped": self.total_dropped,
                "total_processed": self.total_processed,
                "estimated_memory_mb": self.estimated_memory / 1024 / 1024 if self.max_memory_bytes else None,
                "max_memory_mb": self.max_memory_bytes / 1024 / 1024 if self.max_memory_bytes else None,
                "OVERFLOW_POLICY": self.overflow_policy,
            }
    
    xǁQueuedRateLimiterǁget_stats__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁQueuedRateLimiterǁget_stats__mutmut_1': xǁQueuedRateLimiterǁget_stats__mutmut_1, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_2': xǁQueuedRateLimiterǁget_stats__mutmut_2, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_3': xǁQueuedRateLimiterǁget_stats__mutmut_3, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_4': xǁQueuedRateLimiterǁget_stats__mutmut_4, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_5': xǁQueuedRateLimiterǁget_stats__mutmut_5, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_6': xǁQueuedRateLimiterǁget_stats__mutmut_6, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_7': xǁQueuedRateLimiterǁget_stats__mutmut_7, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_8': xǁQueuedRateLimiterǁget_stats__mutmut_8, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_9': xǁQueuedRateLimiterǁget_stats__mutmut_9, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_10': xǁQueuedRateLimiterǁget_stats__mutmut_10, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_11': xǁQueuedRateLimiterǁget_stats__mutmut_11, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_12': xǁQueuedRateLimiterǁget_stats__mutmut_12, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_13': xǁQueuedRateLimiterǁget_stats__mutmut_13, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_14': xǁQueuedRateLimiterǁget_stats__mutmut_14, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_15': xǁQueuedRateLimiterǁget_stats__mutmut_15, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_16': xǁQueuedRateLimiterǁget_stats__mutmut_16, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_17': xǁQueuedRateLimiterǁget_stats__mutmut_17, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_18': xǁQueuedRateLimiterǁget_stats__mutmut_18, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_19': xǁQueuedRateLimiterǁget_stats__mutmut_19, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_20': xǁQueuedRateLimiterǁget_stats__mutmut_20, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_21': xǁQueuedRateLimiterǁget_stats__mutmut_21, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_22': xǁQueuedRateLimiterǁget_stats__mutmut_22, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_23': xǁQueuedRateLimiterǁget_stats__mutmut_23, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_24': xǁQueuedRateLimiterǁget_stats__mutmut_24, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_25': xǁQueuedRateLimiterǁget_stats__mutmut_25, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_26': xǁQueuedRateLimiterǁget_stats__mutmut_26, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_27': xǁQueuedRateLimiterǁget_stats__mutmut_27, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_28': xǁQueuedRateLimiterǁget_stats__mutmut_28, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_29': xǁQueuedRateLimiterǁget_stats__mutmut_29, 
        'xǁQueuedRateLimiterǁget_stats__mutmut_30': xǁQueuedRateLimiterǁget_stats__mutmut_30
    }
    
    def get_stats(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁQueuedRateLimiterǁget_stats__mutmut_orig"), object.__getattribute__(self, "xǁQueuedRateLimiterǁget_stats__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_stats.__signature__ = _mutmut_signature(xǁQueuedRateLimiterǁget_stats__mutmut_orig)
    xǁQueuedRateLimiterǁget_stats__mutmut_orig.__name__ = 'xǁQueuedRateLimiterǁget_stats'


class BufferedRateLimiter:
    """Simple synchronous rate limiter with overflow buffer.
    Does not use a worker thread - processes inline.
    """

    def xǁBufferedRateLimiterǁ__init____mutmut_orig(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_1(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 101,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_2(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = False,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_3(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity < 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_4(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 1:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_5(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError(None)
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_6(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("XXCapacity must be positiveXX")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_7(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_8(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("CAPACITY MUST BE POSITIVE")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_9(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate < 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_10(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 1:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_11(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError(None)

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_12(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("XXRefill rate must be positiveXX")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_13(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_14(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("REFILL RATE MUST BE POSITIVE")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_15(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = None
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_16(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(None)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_17(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = None
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_18(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(None)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_19(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = None
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_20(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(None)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_21(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = None
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_22(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = None

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_23(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = None
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_24(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = None
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_25(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_26(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=None) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_27(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = None
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_28(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 1
        self.total_denied = 0
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_29(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = None
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_30(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 1
        self.total_bytes_dropped = 0

    def xǁBufferedRateLimiterǁ__init____mutmut_31(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = None

    def xǁBufferedRateLimiterǁ__init____mutmut_32(
        self,
        capacity: float,
        refill_rate: float,
        buffer_size: int = 100,
        track_dropped: bool = True,
    ) -> None:
        """Initialize buffered rate limiter.

        Args:
            capacity: Maximum tokens (burst capacity)
            refill_rate: Tokens per second
            buffer_size: Number of recently dropped items to track
            track_dropped: Whether to keep dropped items for debugging

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track dropped items
        self.buffer_size = buffer_size
        self.track_dropped = track_dropped
        self.dropped_buffer: deque[Any] | None = deque(maxlen=buffer_size) if track_dropped else None

        # Statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.total_bytes_dropped = 1
    
    xǁBufferedRateLimiterǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBufferedRateLimiterǁ__init____mutmut_1': xǁBufferedRateLimiterǁ__init____mutmut_1, 
        'xǁBufferedRateLimiterǁ__init____mutmut_2': xǁBufferedRateLimiterǁ__init____mutmut_2, 
        'xǁBufferedRateLimiterǁ__init____mutmut_3': xǁBufferedRateLimiterǁ__init____mutmut_3, 
        'xǁBufferedRateLimiterǁ__init____mutmut_4': xǁBufferedRateLimiterǁ__init____mutmut_4, 
        'xǁBufferedRateLimiterǁ__init____mutmut_5': xǁBufferedRateLimiterǁ__init____mutmut_5, 
        'xǁBufferedRateLimiterǁ__init____mutmut_6': xǁBufferedRateLimiterǁ__init____mutmut_6, 
        'xǁBufferedRateLimiterǁ__init____mutmut_7': xǁBufferedRateLimiterǁ__init____mutmut_7, 
        'xǁBufferedRateLimiterǁ__init____mutmut_8': xǁBufferedRateLimiterǁ__init____mutmut_8, 
        'xǁBufferedRateLimiterǁ__init____mutmut_9': xǁBufferedRateLimiterǁ__init____mutmut_9, 
        'xǁBufferedRateLimiterǁ__init____mutmut_10': xǁBufferedRateLimiterǁ__init____mutmut_10, 
        'xǁBufferedRateLimiterǁ__init____mutmut_11': xǁBufferedRateLimiterǁ__init____mutmut_11, 
        'xǁBufferedRateLimiterǁ__init____mutmut_12': xǁBufferedRateLimiterǁ__init____mutmut_12, 
        'xǁBufferedRateLimiterǁ__init____mutmut_13': xǁBufferedRateLimiterǁ__init____mutmut_13, 
        'xǁBufferedRateLimiterǁ__init____mutmut_14': xǁBufferedRateLimiterǁ__init____mutmut_14, 
        'xǁBufferedRateLimiterǁ__init____mutmut_15': xǁBufferedRateLimiterǁ__init____mutmut_15, 
        'xǁBufferedRateLimiterǁ__init____mutmut_16': xǁBufferedRateLimiterǁ__init____mutmut_16, 
        'xǁBufferedRateLimiterǁ__init____mutmut_17': xǁBufferedRateLimiterǁ__init____mutmut_17, 
        'xǁBufferedRateLimiterǁ__init____mutmut_18': xǁBufferedRateLimiterǁ__init____mutmut_18, 
        'xǁBufferedRateLimiterǁ__init____mutmut_19': xǁBufferedRateLimiterǁ__init____mutmut_19, 
        'xǁBufferedRateLimiterǁ__init____mutmut_20': xǁBufferedRateLimiterǁ__init____mutmut_20, 
        'xǁBufferedRateLimiterǁ__init____mutmut_21': xǁBufferedRateLimiterǁ__init____mutmut_21, 
        'xǁBufferedRateLimiterǁ__init____mutmut_22': xǁBufferedRateLimiterǁ__init____mutmut_22, 
        'xǁBufferedRateLimiterǁ__init____mutmut_23': xǁBufferedRateLimiterǁ__init____mutmut_23, 
        'xǁBufferedRateLimiterǁ__init____mutmut_24': xǁBufferedRateLimiterǁ__init____mutmut_24, 
        'xǁBufferedRateLimiterǁ__init____mutmut_25': xǁBufferedRateLimiterǁ__init____mutmut_25, 
        'xǁBufferedRateLimiterǁ__init____mutmut_26': xǁBufferedRateLimiterǁ__init____mutmut_26, 
        'xǁBufferedRateLimiterǁ__init____mutmut_27': xǁBufferedRateLimiterǁ__init____mutmut_27, 
        'xǁBufferedRateLimiterǁ__init____mutmut_28': xǁBufferedRateLimiterǁ__init____mutmut_28, 
        'xǁBufferedRateLimiterǁ__init____mutmut_29': xǁBufferedRateLimiterǁ__init____mutmut_29, 
        'xǁBufferedRateLimiterǁ__init____mutmut_30': xǁBufferedRateLimiterǁ__init____mutmut_30, 
        'xǁBufferedRateLimiterǁ__init____mutmut_31': xǁBufferedRateLimiterǁ__init____mutmut_31, 
        'xǁBufferedRateLimiterǁ__init____mutmut_32': xǁBufferedRateLimiterǁ__init____mutmut_32
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBufferedRateLimiterǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁBufferedRateLimiterǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁBufferedRateLimiterǁ__init____mutmut_orig)
    xǁBufferedRateLimiterǁ__init____mutmut_orig.__name__ = 'xǁBufferedRateLimiterǁ__init__'

    def xǁBufferedRateLimiterǁis_allowed__mutmut_orig(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_1(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = None
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_2(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = None

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_3(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now + self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_4(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed >= 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_5(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 1:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_6(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = None
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_7(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed / self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_8(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = None
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_9(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(None, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_10(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, None)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_11(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_12(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, )
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_13(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens - tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_14(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = None

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_15(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens > 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_16(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 2.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_17(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens = 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_18(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens += 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_19(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 2.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_20(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed = 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_21(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed -= 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_22(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 2
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_23(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return False, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_24(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied = 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_25(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied -= 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_26(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 2

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_27(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None or self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_28(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped or item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_29(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_30(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_31(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    None,
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_32(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "XXtimeXX": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_33(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "TIME": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_34(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "XXitemXX": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_35(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "ITEM": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_36(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "XXsizeXX": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_37(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "SIZE": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_38(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(None),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_39(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped = sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_40(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped -= sys.getsizeof(item)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_41(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(None)

            return False, f"Rate limit exceeded (tokens: {self.tokens:.1f})"

    def xǁBufferedRateLimiterǁis_allowed__mutmut_42(self, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if item is allowed based on rate limit.

        Args:
            item: Optional item to track if dropped

        Returns:
            Tuple of (allowed, reason)

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True, None
            self.total_denied += 1

            # Track dropped item
            if self.track_dropped and item is not None and self.dropped_buffer is not None:
                self.dropped_buffer.append(
                    {
                        "time": now,
                        "item": item,
                        "size": sys.getsizeof(item),
                    },
                )
                self.total_bytes_dropped += sys.getsizeof(item)

            return True, f"Rate limit exceeded (tokens: {self.tokens:.1f})"
    
    xǁBufferedRateLimiterǁis_allowed__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBufferedRateLimiterǁis_allowed__mutmut_1': xǁBufferedRateLimiterǁis_allowed__mutmut_1, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_2': xǁBufferedRateLimiterǁis_allowed__mutmut_2, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_3': xǁBufferedRateLimiterǁis_allowed__mutmut_3, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_4': xǁBufferedRateLimiterǁis_allowed__mutmut_4, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_5': xǁBufferedRateLimiterǁis_allowed__mutmut_5, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_6': xǁBufferedRateLimiterǁis_allowed__mutmut_6, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_7': xǁBufferedRateLimiterǁis_allowed__mutmut_7, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_8': xǁBufferedRateLimiterǁis_allowed__mutmut_8, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_9': xǁBufferedRateLimiterǁis_allowed__mutmut_9, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_10': xǁBufferedRateLimiterǁis_allowed__mutmut_10, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_11': xǁBufferedRateLimiterǁis_allowed__mutmut_11, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_12': xǁBufferedRateLimiterǁis_allowed__mutmut_12, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_13': xǁBufferedRateLimiterǁis_allowed__mutmut_13, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_14': xǁBufferedRateLimiterǁis_allowed__mutmut_14, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_15': xǁBufferedRateLimiterǁis_allowed__mutmut_15, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_16': xǁBufferedRateLimiterǁis_allowed__mutmut_16, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_17': xǁBufferedRateLimiterǁis_allowed__mutmut_17, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_18': xǁBufferedRateLimiterǁis_allowed__mutmut_18, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_19': xǁBufferedRateLimiterǁis_allowed__mutmut_19, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_20': xǁBufferedRateLimiterǁis_allowed__mutmut_20, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_21': xǁBufferedRateLimiterǁis_allowed__mutmut_21, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_22': xǁBufferedRateLimiterǁis_allowed__mutmut_22, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_23': xǁBufferedRateLimiterǁis_allowed__mutmut_23, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_24': xǁBufferedRateLimiterǁis_allowed__mutmut_24, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_25': xǁBufferedRateLimiterǁis_allowed__mutmut_25, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_26': xǁBufferedRateLimiterǁis_allowed__mutmut_26, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_27': xǁBufferedRateLimiterǁis_allowed__mutmut_27, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_28': xǁBufferedRateLimiterǁis_allowed__mutmut_28, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_29': xǁBufferedRateLimiterǁis_allowed__mutmut_29, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_30': xǁBufferedRateLimiterǁis_allowed__mutmut_30, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_31': xǁBufferedRateLimiterǁis_allowed__mutmut_31, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_32': xǁBufferedRateLimiterǁis_allowed__mutmut_32, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_33': xǁBufferedRateLimiterǁis_allowed__mutmut_33, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_34': xǁBufferedRateLimiterǁis_allowed__mutmut_34, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_35': xǁBufferedRateLimiterǁis_allowed__mutmut_35, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_36': xǁBufferedRateLimiterǁis_allowed__mutmut_36, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_37': xǁBufferedRateLimiterǁis_allowed__mutmut_37, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_38': xǁBufferedRateLimiterǁis_allowed__mutmut_38, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_39': xǁBufferedRateLimiterǁis_allowed__mutmut_39, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_40': xǁBufferedRateLimiterǁis_allowed__mutmut_40, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_41': xǁBufferedRateLimiterǁis_allowed__mutmut_41, 
        'xǁBufferedRateLimiterǁis_allowed__mutmut_42': xǁBufferedRateLimiterǁis_allowed__mutmut_42
    }
    
    def is_allowed(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBufferedRateLimiterǁis_allowed__mutmut_orig"), object.__getattribute__(self, "xǁBufferedRateLimiterǁis_allowed__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_allowed.__signature__ = _mutmut_signature(xǁBufferedRateLimiterǁis_allowed__mutmut_orig)
    xǁBufferedRateLimiterǁis_allowed__mutmut_orig.__name__ = 'xǁBufferedRateLimiterǁis_allowed'

    def xǁBufferedRateLimiterǁget_dropped_samples__mutmut_orig(self, count: int = 10) -> list[Any]:
        """Get recent dropped items for debugging."""
        if not self.track_dropped or not self.dropped_buffer:
            return []

        with self.lock:
            return list(self.dropped_buffer)[-count:]

    def xǁBufferedRateLimiterǁget_dropped_samples__mutmut_1(self, count: int = 11) -> list[Any]:
        """Get recent dropped items for debugging."""
        if not self.track_dropped or not self.dropped_buffer:
            return []

        with self.lock:
            return list(self.dropped_buffer)[-count:]

    def xǁBufferedRateLimiterǁget_dropped_samples__mutmut_2(self, count: int = 10) -> list[Any]:
        """Get recent dropped items for debugging."""
        if not self.track_dropped and not self.dropped_buffer:
            return []

        with self.lock:
            return list(self.dropped_buffer)[-count:]

    def xǁBufferedRateLimiterǁget_dropped_samples__mutmut_3(self, count: int = 10) -> list[Any]:
        """Get recent dropped items for debugging."""
        if self.track_dropped or not self.dropped_buffer:
            return []

        with self.lock:
            return list(self.dropped_buffer)[-count:]

    def xǁBufferedRateLimiterǁget_dropped_samples__mutmut_4(self, count: int = 10) -> list[Any]:
        """Get recent dropped items for debugging."""
        if not self.track_dropped or self.dropped_buffer:
            return []

        with self.lock:
            return list(self.dropped_buffer)[-count:]

    def xǁBufferedRateLimiterǁget_dropped_samples__mutmut_5(self, count: int = 10) -> list[Any]:
        """Get recent dropped items for debugging."""
        if not self.track_dropped or not self.dropped_buffer:
            return []

        with self.lock:
            return list(None)[-count:]

    def xǁBufferedRateLimiterǁget_dropped_samples__mutmut_6(self, count: int = 10) -> list[Any]:
        """Get recent dropped items for debugging."""
        if not self.track_dropped or not self.dropped_buffer:
            return []

        with self.lock:
            return list(self.dropped_buffer)[+count:]
    
    xǁBufferedRateLimiterǁget_dropped_samples__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBufferedRateLimiterǁget_dropped_samples__mutmut_1': xǁBufferedRateLimiterǁget_dropped_samples__mutmut_1, 
        'xǁBufferedRateLimiterǁget_dropped_samples__mutmut_2': xǁBufferedRateLimiterǁget_dropped_samples__mutmut_2, 
        'xǁBufferedRateLimiterǁget_dropped_samples__mutmut_3': xǁBufferedRateLimiterǁget_dropped_samples__mutmut_3, 
        'xǁBufferedRateLimiterǁget_dropped_samples__mutmut_4': xǁBufferedRateLimiterǁget_dropped_samples__mutmut_4, 
        'xǁBufferedRateLimiterǁget_dropped_samples__mutmut_5': xǁBufferedRateLimiterǁget_dropped_samples__mutmut_5, 
        'xǁBufferedRateLimiterǁget_dropped_samples__mutmut_6': xǁBufferedRateLimiterǁget_dropped_samples__mutmut_6
    }
    
    def get_dropped_samples(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBufferedRateLimiterǁget_dropped_samples__mutmut_orig"), object.__getattribute__(self, "xǁBufferedRateLimiterǁget_dropped_samples__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_dropped_samples.__signature__ = _mutmut_signature(xǁBufferedRateLimiterǁget_dropped_samples__mutmut_orig)
    xǁBufferedRateLimiterǁget_dropped_samples__mutmut_orig.__name__ = 'xǁBufferedRateLimiterǁget_dropped_samples'

    def xǁBufferedRateLimiterǁget_stats__mutmut_orig(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_1(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = None

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_2(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "XXtokens_availableXX": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_3(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "TOKENS_AVAILABLE": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_4(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "XXcapacityXX": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_5(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "CAPACITY": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_6(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "XXrefill_rateXX": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_7(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "REFILL_RATE": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_8(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "XXtotal_allowedXX": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_9(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "TOTAL_ALLOWED": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_10(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "XXtotal_deniedXX": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_11(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "TOTAL_DENIED": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_12(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "XXtotal_bytes_droppedXX": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_13(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "TOTAL_BYTES_DROPPED": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_14(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped or self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_15(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = None
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_16(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["XXdropped_buffer_sizeXX"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_17(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["DROPPED_BUFFER_SIZE"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_18(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = None

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_19(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["XXoldest_dropped_ageXX"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_20(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["OLDEST_DROPPED_AGE"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_21(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() + self.dropped_buffer[0]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_22(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[1]["time"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_23(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["XXtimeXX"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_24(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["TIME"] if self.dropped_buffer else 0
                )

            return stats

    def xǁBufferedRateLimiterǁget_stats__mutmut_25(self) -> dict[str, Any]:
        """Get statistics."""
        with self.lock:
            stats = {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "total_bytes_dropped": self.total_bytes_dropped,
            }

            if self.track_dropped and self.dropped_buffer:
                stats["dropped_buffer_size"] = len(self.dropped_buffer)
                stats["oldest_dropped_age"] = (
                    time.monotonic() - self.dropped_buffer[0]["time"] if self.dropped_buffer else 1
                )

            return stats
    
    xǁBufferedRateLimiterǁget_stats__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBufferedRateLimiterǁget_stats__mutmut_1': xǁBufferedRateLimiterǁget_stats__mutmut_1, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_2': xǁBufferedRateLimiterǁget_stats__mutmut_2, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_3': xǁBufferedRateLimiterǁget_stats__mutmut_3, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_4': xǁBufferedRateLimiterǁget_stats__mutmut_4, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_5': xǁBufferedRateLimiterǁget_stats__mutmut_5, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_6': xǁBufferedRateLimiterǁget_stats__mutmut_6, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_7': xǁBufferedRateLimiterǁget_stats__mutmut_7, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_8': xǁBufferedRateLimiterǁget_stats__mutmut_8, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_9': xǁBufferedRateLimiterǁget_stats__mutmut_9, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_10': xǁBufferedRateLimiterǁget_stats__mutmut_10, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_11': xǁBufferedRateLimiterǁget_stats__mutmut_11, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_12': xǁBufferedRateLimiterǁget_stats__mutmut_12, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_13': xǁBufferedRateLimiterǁget_stats__mutmut_13, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_14': xǁBufferedRateLimiterǁget_stats__mutmut_14, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_15': xǁBufferedRateLimiterǁget_stats__mutmut_15, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_16': xǁBufferedRateLimiterǁget_stats__mutmut_16, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_17': xǁBufferedRateLimiterǁget_stats__mutmut_17, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_18': xǁBufferedRateLimiterǁget_stats__mutmut_18, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_19': xǁBufferedRateLimiterǁget_stats__mutmut_19, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_20': xǁBufferedRateLimiterǁget_stats__mutmut_20, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_21': xǁBufferedRateLimiterǁget_stats__mutmut_21, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_22': xǁBufferedRateLimiterǁget_stats__mutmut_22, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_23': xǁBufferedRateLimiterǁget_stats__mutmut_23, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_24': xǁBufferedRateLimiterǁget_stats__mutmut_24, 
        'xǁBufferedRateLimiterǁget_stats__mutmut_25': xǁBufferedRateLimiterǁget_stats__mutmut_25
    }
    
    def get_stats(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBufferedRateLimiterǁget_stats__mutmut_orig"), object.__getattribute__(self, "xǁBufferedRateLimiterǁget_stats__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_stats.__signature__ = _mutmut_signature(xǁBufferedRateLimiterǁget_stats__mutmut_orig)
    xǁBufferedRateLimiterǁget_stats__mutmut_orig.__name__ = 'xǁBufferedRateLimiterǁget_stats'


# <3 🧱🤝📝🪄
