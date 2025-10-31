#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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

    def __init__(
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

    def start(self) -> None:
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

    def stop(self, timeout: float = 1.0) -> None:
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

    def _estimate_size(self, item: Any) -> int:
        """Estimate memory size of an item."""
        # Simple estimation - can be made more sophisticated
        return sys.getsizeof(item)

    def _refill_tokens(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill

        if elapsed > 0:
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill = now

    def enqueue(self, item: Any) -> tuple[bool, str | None]:
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

    def _process_queue(self) -> None:
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

    def _process_item(self, item: Any) -> None:
        """Process a single item from the queue."""
        # This would be overridden to actually emit the log

    def get_stats(self) -> dict[str, Any]:
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


class BufferedRateLimiter:
    """Simple synchronous rate limiter with overflow buffer.
    Does not use a worker thread - processes inline.
    """

    def __init__(
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

    def is_allowed(self, item: Any | None = None) -> tuple[bool, str | None]:
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

    def get_dropped_samples(self, count: int = 10) -> list[Any]:
        """Get recent dropped items for debugging."""
        if not self.track_dropped or not self.dropped_buffer:
            return []

        with self.lock:
            return list(self.dropped_buffer)[-count:]

    def get_stats(self) -> dict[str, Any]:
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


# 🧱🏗️🔚
