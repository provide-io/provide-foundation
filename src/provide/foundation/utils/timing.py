#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
import contextvars
import time
from typing import TYPE_CHECKING, Any

"""Timing and performance utilities.

Provides context managers and utilities for timing operations and logging performance.
"""

if TYPE_CHECKING:
    from provide.foundation.logger.base import FoundationLogger


# Context variable for trace_id (applications can set this for request tracing)
_PROVIDE_CONTEXT_TRACE_ID = contextvars.ContextVar("foundation_context_trace_id", default=None)


@contextmanager
def timed_block(
    logger_instance: FoundationLogger,
    event_name: str,
    layer_keys: dict[str, Any] | None = None,
    initial_kvs: dict[str, Any] | None = None,
    **extra_kvs: Any,
) -> Generator[dict[str, Any], None, None]:
    """Context manager that logs the duration of a code block.

    Logs at DEBUG when entering, INFO on success, ERROR on exception.

    Args:
        logger_instance: Logger to use for output
        event_name: Name of the operation being timed
        layer_keys: Semantic layer keys (e.g., llm-specific keys)
        initial_kvs: Initial key-value pairs to include in logs
        **extra_kvs: Additional key-value pairs

    Yields:
        A mutable dict that can be updated with additional context

    Example:
        >>> with timed_block(logger, "database_query") as ctx:
        >>>     ctx["query"] = "SELECT * FROM users"
        >>>     result = db.query("SELECT * FROM users")
        >>>     ctx["rows"] = len(result)

    """
    # Combine all key-value pairs
    all_kvs = {}
    if layer_keys:
        all_kvs.update(layer_keys)
    if initial_kvs:
        all_kvs.update(initial_kvs)
    all_kvs.update(extra_kvs)

    # Try to get trace_id from context
    trace_id = _PROVIDE_CONTEXT_TRACE_ID.get()
    if trace_id and "trace_id" not in all_kvs:
        all_kvs["trace_id"] = trace_id

    # Create context dict that can be modified
    context: dict[str, Any] = {}

    # Log start
    logger_instance.debug(f"{event_name} started", **all_kvs)

    start_time = time.perf_counter()
    try:
        yield context

        # Success - calculate duration and log
        duration = time.perf_counter() - start_time
        all_kvs.update(context)
        all_kvs["duration_seconds"] = round(duration, 3)
        all_kvs["outcome"] = "success"

        logger_instance.info(f"{event_name} completed", **all_kvs)

    except Exception as e:
        # Error - calculate duration and log with exception
        duration = time.perf_counter() - start_time
        all_kvs.update(context)
        all_kvs["duration_seconds"] = round(duration, 3)
        all_kvs["outcome"] = "error"
        all_kvs["error.message"] = str(e)
        all_kvs["error.type"] = type(e).__name__

        logger_instance.error(f"{event_name} failed", exc_info=True, **all_kvs)
        raise


# 🧱🏗️🔚
