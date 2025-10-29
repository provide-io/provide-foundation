# provide/foundation/integrations/openobserve/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveAuthenticationError,
    OpenObserveConfigError,
    OpenObserveConnectionError,
    OpenObserveError,
    OpenObserveQueryError,
    OpenObserveStreamingError,
)
from provide.foundation.integrations.openobserve.formatters import (
    format_csv,
    format_json,
    format_log_line,
    format_output,
    format_summary,
    format_table,
)
from provide.foundation.integrations.openobserve.models import (
    SearchQuery,
    SearchResponse,
    StreamInfo,
    parse_relative_time,
)
from provide.foundation.integrations.openobserve.search import (
    aggregate_by_level,
    get_current_trace_logs,
    search_by_level,
    search_by_service,
    search_by_trace_id,
    search_errors,
    search_logs,
)
from provide.foundation.integrations.openobserve.streaming import (
    stream_logs,
    stream_search_http2,
    tail_logs,
)

"""OpenObserve integration for Foundation.

Provides log querying and streaming capabilities as an optional integration.
"""

__all__ = [
    "OpenObserveAuthenticationError",
    # Client
    "OpenObserveClient",
    # Configuration
    "OpenObserveConfig",
    "OpenObserveConfigError",
    "OpenObserveConnectionError",
    # Exceptions
    "OpenObserveError",
    "OpenObserveQueryError",
    "OpenObserveStreamingError",
    # Models
    "SearchQuery",
    "SearchResponse",
    "StreamInfo",
    "aggregate_by_level",
    "format_csv",
    # Formatters
    "format_json",
    "format_log_line",
    "format_output",
    "format_summary",
    "format_table",
    "get_current_trace_logs",
    "parse_relative_time",
    "search_by_level",
    "search_by_service",
    "search_by_trace_id",
    "search_errors",
    # Search functions
    "search_logs",
    # Streaming functions
    "stream_logs",
    "stream_search_http2",
    "tail_logs",
]
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


# <3 🧱🤝🔌🪄
