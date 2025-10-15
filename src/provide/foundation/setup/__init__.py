# provide/foundation/setup/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# __init__.py
#
from provide.foundation.concurrency.locks import get_lock_manager
from provide.foundation.logger.setup import internal_setup
from provide.foundation.metrics.otel import shutdown_opentelemetry_metrics
from provide.foundation.streams.file import flush_log_streams
from provide.foundation.tracer.otel import shutdown_opentelemetry

"""Foundation Setup Module.

This module provides the main setup API for Foundation,
orchestrating logging, tracing, and other subsystems.
"""

_EXPLICIT_SETUP_DONE = False


async def shutdown_foundation(timeout_millis: int = 5000) -> None:
    """Gracefully shutdown all Foundation subsystems.

    Args:
        timeout_millis: Timeout for shutdown (currently unused)

    """
    with get_lock_manager().acquire("foundation.logger.setup"):
        # Shutdown OpenTelemetry tracing and metrics
        shutdown_opentelemetry()
        shutdown_opentelemetry_metrics()

        # Flush logging streams
        flush_log_streams()


__all__ = [
    "internal_setup",
    "shutdown_foundation",
]


# <3 🧱🤝🛠️🪄
