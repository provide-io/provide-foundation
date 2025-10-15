# provide/foundation/observability/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Any

"""Observability module for Foundation.

Provides integration with observability platforms like OpenObserve.
Only available when OpenTelemetry dependencies are installed.
"""

if TYPE_CHECKING:
    pass  # OpenTelemetry imports are handled at runtime

# OpenTelemetry feature detection - Pattern 1: _HAS_* flag
_otel_trace_module: Any = None
try:
    from opentelemetry import trace as _otel_trace_module

    _HAS_OTEL = True
except ImportError:
    _otel_trace_module = None
    _HAS_OTEL = False

# Use consistent name throughout
otel_trace = _otel_trace_module

# Pattern 2: Import real implementation or create stubs
if _HAS_OTEL:
    try:
        from provide.foundation.integrations.openobserve import (
            OpenObserveClient,
            search_logs,
            stream_logs,
        )

        # Commands will auto-register if click is available
        with suppress(ImportError):
            from provide.foundation.integrations.openobserve.commands import (  # noqa: F401
                openobserve_group,
            )
    except ImportError:
        # OpenObserve module not available - create stubs
        from provide.foundation.utils.stubs import create_dependency_stub, create_function_stub

        OpenObserveClient = create_dependency_stub("opentelemetry", "observability")  # type: ignore[misc,assignment]
        search_logs = create_function_stub("opentelemetry", "observability")
        stream_logs = create_function_stub("opentelemetry", "observability")
else:
    # OpenTelemetry not available - create stubs
    from provide.foundation.utils.stubs import create_dependency_stub, create_function_stub

    OpenObserveClient = create_dependency_stub("opentelemetry", "observability")  # type: ignore[misc,assignment]
    search_logs = create_function_stub("opentelemetry", "observability")
    stream_logs = create_function_stub("opentelemetry", "observability")


# Static __all__ export (always the same, regardless of dependencies)
__all__ = [
    "_HAS_OTEL",
    "OpenObserveClient",
    "is_openobserve_available",
    "otel_trace",
    "search_logs",
    "stream_logs",
]


def is_openobserve_available() -> bool:
    """Check if OpenObserve integration is available.

    Returns:
        True if OpenTelemetry and OpenObserve are available

    """
    return _HAS_OTEL and "OpenObserveClient" in globals()


# <3 🧱🤝🔭🪄
