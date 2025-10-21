# provide/foundation/integrations/openobserve/formatters.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import csv
from datetime import datetime
import io
from typing import Any

from provide.foundation.integrations.openobserve.models import SearchResponse
from provide.foundation.serialization import json_dumps

"""Output formatting utilities for OpenObserve results."""
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


def x_format_json__mutmut_orig(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_1(response: SearchResponse | dict[str, Any], pretty: bool = False) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_2(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = None
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_3(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "XXhitsXX": response.hits,
            "total": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_4(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "HITS": response.hits,
            "total": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_5(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "XXtotalXX": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_6(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "TOTAL": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_7(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "XXtookXX": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_8(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "TOOK": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_9(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "took": response.took,
            "XXscan_sizeXX": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_10(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "took": response.took,
            "SCAN_SIZE": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_11(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = None

    if pretty:
        return json_dumps(data, indent=2, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_12(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(None, indent=2, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_13(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=None, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_14(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, sort_keys=None)
    return json_dumps(data)


def x_format_json__mutmut_15(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(indent=2, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_16(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_17(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, )
    return json_dumps(data)


def x_format_json__mutmut_18(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=3, sort_keys=False)
    return json_dumps(data)


def x_format_json__mutmut_19(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, sort_keys=True)
    return json_dumps(data)


def x_format_json__mutmut_20(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
    """Format response as JSON.

    Args:
        response: Search response or log entry
        pretty: If True, use pretty printing

    Returns:
        JSON string

    """
    if isinstance(response, SearchResponse):
        data = {
            "hits": response.hits,
            "total": response.total,
            "took": response.took,
            "scan_size": response.scan_size,
        }
    else:
        data = response

    if pretty:
        return json_dumps(data, indent=2, sort_keys=False)
    return json_dumps(None)

x_format_json__mutmut_mutants : ClassVar[MutantDict] = {
'x_format_json__mutmut_1': x_format_json__mutmut_1, 
    'x_format_json__mutmut_2': x_format_json__mutmut_2, 
    'x_format_json__mutmut_3': x_format_json__mutmut_3, 
    'x_format_json__mutmut_4': x_format_json__mutmut_4, 
    'x_format_json__mutmut_5': x_format_json__mutmut_5, 
    'x_format_json__mutmut_6': x_format_json__mutmut_6, 
    'x_format_json__mutmut_7': x_format_json__mutmut_7, 
    'x_format_json__mutmut_8': x_format_json__mutmut_8, 
    'x_format_json__mutmut_9': x_format_json__mutmut_9, 
    'x_format_json__mutmut_10': x_format_json__mutmut_10, 
    'x_format_json__mutmut_11': x_format_json__mutmut_11, 
    'x_format_json__mutmut_12': x_format_json__mutmut_12, 
    'x_format_json__mutmut_13': x_format_json__mutmut_13, 
    'x_format_json__mutmut_14': x_format_json__mutmut_14, 
    'x_format_json__mutmut_15': x_format_json__mutmut_15, 
    'x_format_json__mutmut_16': x_format_json__mutmut_16, 
    'x_format_json__mutmut_17': x_format_json__mutmut_17, 
    'x_format_json__mutmut_18': x_format_json__mutmut_18, 
    'x_format_json__mutmut_19': x_format_json__mutmut_19, 
    'x_format_json__mutmut_20': x_format_json__mutmut_20
}

def format_json(*args, **kwargs):
    result = _mutmut_trampoline(x_format_json__mutmut_orig, x_format_json__mutmut_mutants, args, kwargs)
    return result 

format_json.__signature__ = _mutmut_signature(x_format_json__mutmut_orig)
x_format_json__mutmut_orig.__name__ = 'x_format_json'


def x_format_log_line__mutmut_orig(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_1(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = None
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_2(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get(None, 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_3(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", None)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_4(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get(0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_5(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", )
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_6(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("XX_timestampXX", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_7(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_TIMESTAMP", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_8(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 1)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_9(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = None
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_10(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get(None, "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_11(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", None)
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_12(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_13(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", )
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_14(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("XXlevelXX", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_15(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("LEVEL", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_16(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "XXINFOXX")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_17(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "info")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_18(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = None
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_19(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get(None, "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_20(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", None)
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_21(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_22(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", )
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_23(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("XXmessageXX", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_24(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("MESSAGE", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_25(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "XXXX")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_26(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = None

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_27(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get(None, "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_28(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", None)

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_29(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_30(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", )

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_31(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("XXserviceXX", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_32(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("SERVICE", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_33(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "XXXX")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_34(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = None
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_35(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(None)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_36(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp * 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_37(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1000001)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_38(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = None
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_39(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime(None)[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_40(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("XX%Y-%m-%d %H:%M:%S.%fXX")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_41(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%y-%m-%d %h:%m:%s.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_42(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%M-%D %H:%M:%S.%F")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_43(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:+3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_44(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_45(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = None

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_46(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "XXunknownXX"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_47(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "UNKNOWN"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_48(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = None

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_49(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(None)

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_50(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(None)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_51(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = None
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_52(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"XX_timestampXX", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_53(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_TIMESTAMP", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_54(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "XXlevelXX", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_55(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "LEVEL", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_56(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "XXmessageXX", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_57(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "MESSAGE", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_58(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "XXserviceXX", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_59(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "SERVICE", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_60(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "XX_pXX"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_61(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_P"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_62(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = None
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_63(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_64(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(None)

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_65(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(None)

    return " ".join(parts)


def x_format_log_line__mutmut_66(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(None)})")

    return " ".join(parts)


def x_format_log_line__mutmut_67(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({'XX, XX'.join(extra_fields)})")

    return " ".join(parts)


def x_format_log_line__mutmut_68(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return " ".join(None)


def x_format_log_line__mutmut_69(entry: dict[str, Any]) -> str:
    """Format a log entry as a traditional log line.

    Args:
        entry: Log entry dictionary

    Returns:
        Formatted log line

    """
    # Extract common fields
    timestamp = entry.get("_timestamp", 0)
    level = entry.get("level", "INFO")
    message = entry.get("message", "")
    service = entry.get("service", "")

    # Convert timestamp to readable format
    if timestamp:
        # Assuming microseconds
        dt = datetime.fromtimestamp(timestamp / 1_000_000)
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        time_str = "unknown"

    # Build log line
    parts = [time_str, f"[{level:5s}]"]

    if service:
        parts.append(f"[{service}]")

    parts.append(message)

    # Add additional fields as key=value
    exclude_fields = {"_timestamp", "level", "message", "service", "_p"}
    extra_fields = []
    for key, value in entry.items():
        if key not in exclude_fields:
            extra_fields.append(f"{key}={value}")

    if extra_fields:
        parts.append(f"({', '.join(extra_fields)})")

    return "XX XX".join(parts)

x_format_log_line__mutmut_mutants : ClassVar[MutantDict] = {
'x_format_log_line__mutmut_1': x_format_log_line__mutmut_1, 
    'x_format_log_line__mutmut_2': x_format_log_line__mutmut_2, 
    'x_format_log_line__mutmut_3': x_format_log_line__mutmut_3, 
    'x_format_log_line__mutmut_4': x_format_log_line__mutmut_4, 
    'x_format_log_line__mutmut_5': x_format_log_line__mutmut_5, 
    'x_format_log_line__mutmut_6': x_format_log_line__mutmut_6, 
    'x_format_log_line__mutmut_7': x_format_log_line__mutmut_7, 
    'x_format_log_line__mutmut_8': x_format_log_line__mutmut_8, 
    'x_format_log_line__mutmut_9': x_format_log_line__mutmut_9, 
    'x_format_log_line__mutmut_10': x_format_log_line__mutmut_10, 
    'x_format_log_line__mutmut_11': x_format_log_line__mutmut_11, 
    'x_format_log_line__mutmut_12': x_format_log_line__mutmut_12, 
    'x_format_log_line__mutmut_13': x_format_log_line__mutmut_13, 
    'x_format_log_line__mutmut_14': x_format_log_line__mutmut_14, 
    'x_format_log_line__mutmut_15': x_format_log_line__mutmut_15, 
    'x_format_log_line__mutmut_16': x_format_log_line__mutmut_16, 
    'x_format_log_line__mutmut_17': x_format_log_line__mutmut_17, 
    'x_format_log_line__mutmut_18': x_format_log_line__mutmut_18, 
    'x_format_log_line__mutmut_19': x_format_log_line__mutmut_19, 
    'x_format_log_line__mutmut_20': x_format_log_line__mutmut_20, 
    'x_format_log_line__mutmut_21': x_format_log_line__mutmut_21, 
    'x_format_log_line__mutmut_22': x_format_log_line__mutmut_22, 
    'x_format_log_line__mutmut_23': x_format_log_line__mutmut_23, 
    'x_format_log_line__mutmut_24': x_format_log_line__mutmut_24, 
    'x_format_log_line__mutmut_25': x_format_log_line__mutmut_25, 
    'x_format_log_line__mutmut_26': x_format_log_line__mutmut_26, 
    'x_format_log_line__mutmut_27': x_format_log_line__mutmut_27, 
    'x_format_log_line__mutmut_28': x_format_log_line__mutmut_28, 
    'x_format_log_line__mutmut_29': x_format_log_line__mutmut_29, 
    'x_format_log_line__mutmut_30': x_format_log_line__mutmut_30, 
    'x_format_log_line__mutmut_31': x_format_log_line__mutmut_31, 
    'x_format_log_line__mutmut_32': x_format_log_line__mutmut_32, 
    'x_format_log_line__mutmut_33': x_format_log_line__mutmut_33, 
    'x_format_log_line__mutmut_34': x_format_log_line__mutmut_34, 
    'x_format_log_line__mutmut_35': x_format_log_line__mutmut_35, 
    'x_format_log_line__mutmut_36': x_format_log_line__mutmut_36, 
    'x_format_log_line__mutmut_37': x_format_log_line__mutmut_37, 
    'x_format_log_line__mutmut_38': x_format_log_line__mutmut_38, 
    'x_format_log_line__mutmut_39': x_format_log_line__mutmut_39, 
    'x_format_log_line__mutmut_40': x_format_log_line__mutmut_40, 
    'x_format_log_line__mutmut_41': x_format_log_line__mutmut_41, 
    'x_format_log_line__mutmut_42': x_format_log_line__mutmut_42, 
    'x_format_log_line__mutmut_43': x_format_log_line__mutmut_43, 
    'x_format_log_line__mutmut_44': x_format_log_line__mutmut_44, 
    'x_format_log_line__mutmut_45': x_format_log_line__mutmut_45, 
    'x_format_log_line__mutmut_46': x_format_log_line__mutmut_46, 
    'x_format_log_line__mutmut_47': x_format_log_line__mutmut_47, 
    'x_format_log_line__mutmut_48': x_format_log_line__mutmut_48, 
    'x_format_log_line__mutmut_49': x_format_log_line__mutmut_49, 
    'x_format_log_line__mutmut_50': x_format_log_line__mutmut_50, 
    'x_format_log_line__mutmut_51': x_format_log_line__mutmut_51, 
    'x_format_log_line__mutmut_52': x_format_log_line__mutmut_52, 
    'x_format_log_line__mutmut_53': x_format_log_line__mutmut_53, 
    'x_format_log_line__mutmut_54': x_format_log_line__mutmut_54, 
    'x_format_log_line__mutmut_55': x_format_log_line__mutmut_55, 
    'x_format_log_line__mutmut_56': x_format_log_line__mutmut_56, 
    'x_format_log_line__mutmut_57': x_format_log_line__mutmut_57, 
    'x_format_log_line__mutmut_58': x_format_log_line__mutmut_58, 
    'x_format_log_line__mutmut_59': x_format_log_line__mutmut_59, 
    'x_format_log_line__mutmut_60': x_format_log_line__mutmut_60, 
    'x_format_log_line__mutmut_61': x_format_log_line__mutmut_61, 
    'x_format_log_line__mutmut_62': x_format_log_line__mutmut_62, 
    'x_format_log_line__mutmut_63': x_format_log_line__mutmut_63, 
    'x_format_log_line__mutmut_64': x_format_log_line__mutmut_64, 
    'x_format_log_line__mutmut_65': x_format_log_line__mutmut_65, 
    'x_format_log_line__mutmut_66': x_format_log_line__mutmut_66, 
    'x_format_log_line__mutmut_67': x_format_log_line__mutmut_67, 
    'x_format_log_line__mutmut_68': x_format_log_line__mutmut_68, 
    'x_format_log_line__mutmut_69': x_format_log_line__mutmut_69
}

def format_log_line(*args, **kwargs):
    result = _mutmut_trampoline(x_format_log_line__mutmut_orig, x_format_log_line__mutmut_mutants, args, kwargs)
    return result 

format_log_line.__signature__ = _mutmut_signature(x_format_log_line__mutmut_orig)
x_format_log_line__mutmut_orig.__name__ = 'x_format_log_line'


def x__determine_columns__mutmut_orig(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "level", "service", "message"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_1(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = None
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "level", "service", "message"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_2(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(None)

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "level", "service", "message"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_3(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = None
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_4(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["XX_timestampXX", "level", "service", "message"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_5(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_TIMESTAMP", "level", "service", "message"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_6(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "XXlevelXX", "service", "message"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_7(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "LEVEL", "service", "message"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_8(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "level", "XXserviceXX", "message"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_9(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "level", "SERVICE", "message"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_10(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "level", "service", "XXmessageXX"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_11(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "level", "service", "MESSAGE"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_12(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "level", "service", "message"]
    columns = None
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_13(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "level", "service", "message"]
    columns = []
    for col in priority_cols:
        if col not in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_14(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "level", "service", "message"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(None)
            all_keys.remove(col)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_15(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "level", "service", "message"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(None)
    columns.extend(sorted(all_keys))
    return columns


def x__determine_columns__mutmut_16(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "level", "service", "message"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(None)
    return columns


def x__determine_columns__mutmut_17(hits: list[dict[str, Any]]) -> list[str]:
    """Determine columns to display from hits."""
    # Get all unique keys from hits
    all_keys: set[str] = set()
    for hit in hits:
        all_keys.update(hit.keys())

    # Sort columns, putting common ones first
    priority_cols = ["_timestamp", "level", "service", "message"]
    columns = []
    for col in priority_cols:
        if col in all_keys:
            columns.append(col)
            all_keys.remove(col)
    columns.extend(sorted(None))
    return columns

x__determine_columns__mutmut_mutants : ClassVar[MutantDict] = {
'x__determine_columns__mutmut_1': x__determine_columns__mutmut_1, 
    'x__determine_columns__mutmut_2': x__determine_columns__mutmut_2, 
    'x__determine_columns__mutmut_3': x__determine_columns__mutmut_3, 
    'x__determine_columns__mutmut_4': x__determine_columns__mutmut_4, 
    'x__determine_columns__mutmut_5': x__determine_columns__mutmut_5, 
    'x__determine_columns__mutmut_6': x__determine_columns__mutmut_6, 
    'x__determine_columns__mutmut_7': x__determine_columns__mutmut_7, 
    'x__determine_columns__mutmut_8': x__determine_columns__mutmut_8, 
    'x__determine_columns__mutmut_9': x__determine_columns__mutmut_9, 
    'x__determine_columns__mutmut_10': x__determine_columns__mutmut_10, 
    'x__determine_columns__mutmut_11': x__determine_columns__mutmut_11, 
    'x__determine_columns__mutmut_12': x__determine_columns__mutmut_12, 
    'x__determine_columns__mutmut_13': x__determine_columns__mutmut_13, 
    'x__determine_columns__mutmut_14': x__determine_columns__mutmut_14, 
    'x__determine_columns__mutmut_15': x__determine_columns__mutmut_15, 
    'x__determine_columns__mutmut_16': x__determine_columns__mutmut_16, 
    'x__determine_columns__mutmut_17': x__determine_columns__mutmut_17
}

def _determine_columns(*args, **kwargs):
    result = _mutmut_trampoline(x__determine_columns__mutmut_orig, x__determine_columns__mutmut_mutants, args, kwargs)
    return result 

_determine_columns.__signature__ = _mutmut_signature(x__determine_columns__mutmut_orig)
x__determine_columns__mutmut_orig.__name__ = 'x__determine_columns'


def x__filter_internal_columns__mutmut_orig(columns: list[str]) -> list[str]:
    """Filter out internal columns if not explicitly requested."""
    if "_p" in columns:
        return [c for c in columns if not c.startswith("_") or c == "_timestamp"]
    return columns


def x__filter_internal_columns__mutmut_1(columns: list[str]) -> list[str]:
    """Filter out internal columns if not explicitly requested."""
    if "XX_pXX" in columns:
        return [c for c in columns if not c.startswith("_") or c == "_timestamp"]
    return columns


def x__filter_internal_columns__mutmut_2(columns: list[str]) -> list[str]:
    """Filter out internal columns if not explicitly requested."""
    if "_P" in columns:
        return [c for c in columns if not c.startswith("_") or c == "_timestamp"]
    return columns


def x__filter_internal_columns__mutmut_3(columns: list[str]) -> list[str]:
    """Filter out internal columns if not explicitly requested."""
    if "_p" not in columns:
        return [c for c in columns if not c.startswith("_") or c == "_timestamp"]
    return columns


def x__filter_internal_columns__mutmut_4(columns: list[str]) -> list[str]:
    """Filter out internal columns if not explicitly requested."""
    if "_p" in columns:
        return [c for c in columns if not c.startswith("_") and c == "_timestamp"]
    return columns


def x__filter_internal_columns__mutmut_5(columns: list[str]) -> list[str]:
    """Filter out internal columns if not explicitly requested."""
    if "_p" in columns:
        return [c for c in columns if c.startswith("_") or c == "_timestamp"]
    return columns


def x__filter_internal_columns__mutmut_6(columns: list[str]) -> list[str]:
    """Filter out internal columns if not explicitly requested."""
    if "_p" in columns:
        return [c for c in columns if not c.startswith(None) or c == "_timestamp"]
    return columns


def x__filter_internal_columns__mutmut_7(columns: list[str]) -> list[str]:
    """Filter out internal columns if not explicitly requested."""
    if "_p" in columns:
        return [c for c in columns if not c.startswith("XX_XX") or c == "_timestamp"]
    return columns


def x__filter_internal_columns__mutmut_8(columns: list[str]) -> list[str]:
    """Filter out internal columns if not explicitly requested."""
    if "_p" in columns:
        return [c for c in columns if not c.startswith("_") or c != "_timestamp"]
    return columns


def x__filter_internal_columns__mutmut_9(columns: list[str]) -> list[str]:
    """Filter out internal columns if not explicitly requested."""
    if "_p" in columns:
        return [c for c in columns if not c.startswith("_") or c == "XX_timestampXX"]
    return columns


def x__filter_internal_columns__mutmut_10(columns: list[str]) -> list[str]:
    """Filter out internal columns if not explicitly requested."""
    if "_p" in columns:
        return [c for c in columns if not c.startswith("_") or c == "_TIMESTAMP"]
    return columns

x__filter_internal_columns__mutmut_mutants : ClassVar[MutantDict] = {
'x__filter_internal_columns__mutmut_1': x__filter_internal_columns__mutmut_1, 
    'x__filter_internal_columns__mutmut_2': x__filter_internal_columns__mutmut_2, 
    'x__filter_internal_columns__mutmut_3': x__filter_internal_columns__mutmut_3, 
    'x__filter_internal_columns__mutmut_4': x__filter_internal_columns__mutmut_4, 
    'x__filter_internal_columns__mutmut_5': x__filter_internal_columns__mutmut_5, 
    'x__filter_internal_columns__mutmut_6': x__filter_internal_columns__mutmut_6, 
    'x__filter_internal_columns__mutmut_7': x__filter_internal_columns__mutmut_7, 
    'x__filter_internal_columns__mutmut_8': x__filter_internal_columns__mutmut_8, 
    'x__filter_internal_columns__mutmut_9': x__filter_internal_columns__mutmut_9, 
    'x__filter_internal_columns__mutmut_10': x__filter_internal_columns__mutmut_10
}

def _filter_internal_columns(*args, **kwargs):
    result = _mutmut_trampoline(x__filter_internal_columns__mutmut_orig, x__filter_internal_columns__mutmut_mutants, args, kwargs)
    return result 

_filter_internal_columns.__signature__ = _mutmut_signature(x__filter_internal_columns__mutmut_orig)
x__filter_internal_columns__mutmut_orig.__name__ = 'x__filter_internal_columns'


def x__format_cell_value__mutmut_orig(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_1(col: str, value: Any, max_length: int = 51) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_2(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" or value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_3(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col != "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_4(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "XX_timestampXX" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_5(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_TIMESTAMP" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_6(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = None
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_7(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(None)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_8(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value * 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_9(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1000001)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_10(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length >= 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_11(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 21:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_12(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime(None)
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_13(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("XX%Y-%m-%d %H:%M:%SXX")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_14(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%y-%m-%d %h:%m:%s")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_15(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%M-%D %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_16(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime(None)

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_17(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("XX%H:%M:%SXX")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_18(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%h:%m:%s")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_19(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = None
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_20(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(None)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_21(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) >= max_length:
        return value_str[: max_length - 3] + "..."
    return value_str


def x__format_cell_value__mutmut_22(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] - "..."
    return value_str


def x__format_cell_value__mutmut_23(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length + 3] + "..."
    return value_str


def x__format_cell_value__mutmut_24(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 4] + "..."
    return value_str


def x__format_cell_value__mutmut_25(col: str, value: Any, max_length: int = 50) -> str:
    """Format a cell value for display."""
    if col == "_timestamp" and value:
        dt = datetime.fromtimestamp(value / 1_000_000)
        if max_length > 20:  # Full format for wide tables
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:  # Short format for narrow tables
            return dt.strftime("%H:%M:%S")

    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[: max_length - 3] + "XX...XX"
    return value_str

x__format_cell_value__mutmut_mutants : ClassVar[MutantDict] = {
'x__format_cell_value__mutmut_1': x__format_cell_value__mutmut_1, 
    'x__format_cell_value__mutmut_2': x__format_cell_value__mutmut_2, 
    'x__format_cell_value__mutmut_3': x__format_cell_value__mutmut_3, 
    'x__format_cell_value__mutmut_4': x__format_cell_value__mutmut_4, 
    'x__format_cell_value__mutmut_5': x__format_cell_value__mutmut_5, 
    'x__format_cell_value__mutmut_6': x__format_cell_value__mutmut_6, 
    'x__format_cell_value__mutmut_7': x__format_cell_value__mutmut_7, 
    'x__format_cell_value__mutmut_8': x__format_cell_value__mutmut_8, 
    'x__format_cell_value__mutmut_9': x__format_cell_value__mutmut_9, 
    'x__format_cell_value__mutmut_10': x__format_cell_value__mutmut_10, 
    'x__format_cell_value__mutmut_11': x__format_cell_value__mutmut_11, 
    'x__format_cell_value__mutmut_12': x__format_cell_value__mutmut_12, 
    'x__format_cell_value__mutmut_13': x__format_cell_value__mutmut_13, 
    'x__format_cell_value__mutmut_14': x__format_cell_value__mutmut_14, 
    'x__format_cell_value__mutmut_15': x__format_cell_value__mutmut_15, 
    'x__format_cell_value__mutmut_16': x__format_cell_value__mutmut_16, 
    'x__format_cell_value__mutmut_17': x__format_cell_value__mutmut_17, 
    'x__format_cell_value__mutmut_18': x__format_cell_value__mutmut_18, 
    'x__format_cell_value__mutmut_19': x__format_cell_value__mutmut_19, 
    'x__format_cell_value__mutmut_20': x__format_cell_value__mutmut_20, 
    'x__format_cell_value__mutmut_21': x__format_cell_value__mutmut_21, 
    'x__format_cell_value__mutmut_22': x__format_cell_value__mutmut_22, 
    'x__format_cell_value__mutmut_23': x__format_cell_value__mutmut_23, 
    'x__format_cell_value__mutmut_24': x__format_cell_value__mutmut_24, 
    'x__format_cell_value__mutmut_25': x__format_cell_value__mutmut_25
}

def _format_cell_value(*args, **kwargs):
    result = _mutmut_trampoline(x__format_cell_value__mutmut_orig, x__format_cell_value__mutmut_mutants, args, kwargs)
    return result 

_format_cell_value.__signature__ = _mutmut_signature(x__format_cell_value__mutmut_orig)
x__format_cell_value__mutmut_orig.__name__ = 'x__format_cell_value'


def x__format_with_tabulate__mutmut_orig(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_1(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = None
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_2(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = None
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_3(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = None
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_4(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(None, "")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_5(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, None)
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_6(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get("")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_7(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, )
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_8(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "XXXX")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_9(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = None
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_10(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(None, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_11(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, None, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_12(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=None)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_13(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_14(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_15(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, )
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_16(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=51)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_17(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(None)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_18(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(None)

    return tabulate(rows, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_19(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(None, headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_20(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=None, tablefmt="grid")


def x__format_with_tabulate__mutmut_21(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt=None)


def x__format_with_tabulate__mutmut_22(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(headers=columns, tablefmt="grid")


def x__format_with_tabulate__mutmut_23(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, tablefmt="grid")


def x__format_with_tabulate__mutmut_24(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, )


def x__format_with_tabulate__mutmut_25(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="XXgridXX")


def x__format_with_tabulate__mutmut_26(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using tabulate library."""
    from tabulate import tabulate  # type: ignore[import-untyped]

    rows = []
    for hit in hits:
        row = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=50)
            row.append(formatted_value)
        rows.append(row)

    return tabulate(rows, headers=columns, tablefmt="GRID")

x__format_with_tabulate__mutmut_mutants : ClassVar[MutantDict] = {
'x__format_with_tabulate__mutmut_1': x__format_with_tabulate__mutmut_1, 
    'x__format_with_tabulate__mutmut_2': x__format_with_tabulate__mutmut_2, 
    'x__format_with_tabulate__mutmut_3': x__format_with_tabulate__mutmut_3, 
    'x__format_with_tabulate__mutmut_4': x__format_with_tabulate__mutmut_4, 
    'x__format_with_tabulate__mutmut_5': x__format_with_tabulate__mutmut_5, 
    'x__format_with_tabulate__mutmut_6': x__format_with_tabulate__mutmut_6, 
    'x__format_with_tabulate__mutmut_7': x__format_with_tabulate__mutmut_7, 
    'x__format_with_tabulate__mutmut_8': x__format_with_tabulate__mutmut_8, 
    'x__format_with_tabulate__mutmut_9': x__format_with_tabulate__mutmut_9, 
    'x__format_with_tabulate__mutmut_10': x__format_with_tabulate__mutmut_10, 
    'x__format_with_tabulate__mutmut_11': x__format_with_tabulate__mutmut_11, 
    'x__format_with_tabulate__mutmut_12': x__format_with_tabulate__mutmut_12, 
    'x__format_with_tabulate__mutmut_13': x__format_with_tabulate__mutmut_13, 
    'x__format_with_tabulate__mutmut_14': x__format_with_tabulate__mutmut_14, 
    'x__format_with_tabulate__mutmut_15': x__format_with_tabulate__mutmut_15, 
    'x__format_with_tabulate__mutmut_16': x__format_with_tabulate__mutmut_16, 
    'x__format_with_tabulate__mutmut_17': x__format_with_tabulate__mutmut_17, 
    'x__format_with_tabulate__mutmut_18': x__format_with_tabulate__mutmut_18, 
    'x__format_with_tabulate__mutmut_19': x__format_with_tabulate__mutmut_19, 
    'x__format_with_tabulate__mutmut_20': x__format_with_tabulate__mutmut_20, 
    'x__format_with_tabulate__mutmut_21': x__format_with_tabulate__mutmut_21, 
    'x__format_with_tabulate__mutmut_22': x__format_with_tabulate__mutmut_22, 
    'x__format_with_tabulate__mutmut_23': x__format_with_tabulate__mutmut_23, 
    'x__format_with_tabulate__mutmut_24': x__format_with_tabulate__mutmut_24, 
    'x__format_with_tabulate__mutmut_25': x__format_with_tabulate__mutmut_25, 
    'x__format_with_tabulate__mutmut_26': x__format_with_tabulate__mutmut_26
}

def _format_with_tabulate(*args, **kwargs):
    result = _mutmut_trampoline(x__format_with_tabulate__mutmut_orig, x__format_with_tabulate__mutmut_mutants, args, kwargs)
    return result 

_format_with_tabulate.__signature__ = _mutmut_signature(x__format_with_tabulate__mutmut_orig)
x__format_with_tabulate__mutmut_orig.__name__ = 'x__format_with_tabulate'


def x__format_simple_table__mutmut_orig(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_1(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = None

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_2(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(None)
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_3(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(None))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_4(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append("XX | XX".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_5(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append(None)

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_6(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" / (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_7(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("XX-XX" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_8(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) / 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_9(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 16))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_10(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = None
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_11(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = None
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_12(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(None, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_13(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, None)
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_14(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get("")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_15(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, )
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_16(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "XXXX")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_17(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = None
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_18(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(None, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_19(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, None, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_20(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=None)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_21(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_22(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_23(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, )
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_24(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=13)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_25(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(None)
        lines.append(" | ".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_26(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(None)

    return "\n".join(lines)


def x__format_simple_table__mutmut_27(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(None))

    return "\n".join(lines)


def x__format_simple_table__mutmut_28(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append("XX | XX".join(row_values))

    return "\n".join(lines)


def x__format_simple_table__mutmut_29(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "\n".join(None)


def x__format_simple_table__mutmut_30(hits: list[dict[str, Any]], columns: list[str]) -> str:
    """Format using simple text formatting."""
    lines = []

    # Header
    lines.append(" | ".join(columns))
    lines.append("-" * (len(columns) * 15))

    # Rows
    for hit in hits:
        row_values = []
        for col in columns:
            value = hit.get(col, "")
            formatted_value = _format_cell_value(col, value, max_length=12)
            row_values.append(formatted_value)
        lines.append(" | ".join(row_values))

    return "XX\nXX".join(lines)

x__format_simple_table__mutmut_mutants : ClassVar[MutantDict] = {
'x__format_simple_table__mutmut_1': x__format_simple_table__mutmut_1, 
    'x__format_simple_table__mutmut_2': x__format_simple_table__mutmut_2, 
    'x__format_simple_table__mutmut_3': x__format_simple_table__mutmut_3, 
    'x__format_simple_table__mutmut_4': x__format_simple_table__mutmut_4, 
    'x__format_simple_table__mutmut_5': x__format_simple_table__mutmut_5, 
    'x__format_simple_table__mutmut_6': x__format_simple_table__mutmut_6, 
    'x__format_simple_table__mutmut_7': x__format_simple_table__mutmut_7, 
    'x__format_simple_table__mutmut_8': x__format_simple_table__mutmut_8, 
    'x__format_simple_table__mutmut_9': x__format_simple_table__mutmut_9, 
    'x__format_simple_table__mutmut_10': x__format_simple_table__mutmut_10, 
    'x__format_simple_table__mutmut_11': x__format_simple_table__mutmut_11, 
    'x__format_simple_table__mutmut_12': x__format_simple_table__mutmut_12, 
    'x__format_simple_table__mutmut_13': x__format_simple_table__mutmut_13, 
    'x__format_simple_table__mutmut_14': x__format_simple_table__mutmut_14, 
    'x__format_simple_table__mutmut_15': x__format_simple_table__mutmut_15, 
    'x__format_simple_table__mutmut_16': x__format_simple_table__mutmut_16, 
    'x__format_simple_table__mutmut_17': x__format_simple_table__mutmut_17, 
    'x__format_simple_table__mutmut_18': x__format_simple_table__mutmut_18, 
    'x__format_simple_table__mutmut_19': x__format_simple_table__mutmut_19, 
    'x__format_simple_table__mutmut_20': x__format_simple_table__mutmut_20, 
    'x__format_simple_table__mutmut_21': x__format_simple_table__mutmut_21, 
    'x__format_simple_table__mutmut_22': x__format_simple_table__mutmut_22, 
    'x__format_simple_table__mutmut_23': x__format_simple_table__mutmut_23, 
    'x__format_simple_table__mutmut_24': x__format_simple_table__mutmut_24, 
    'x__format_simple_table__mutmut_25': x__format_simple_table__mutmut_25, 
    'x__format_simple_table__mutmut_26': x__format_simple_table__mutmut_26, 
    'x__format_simple_table__mutmut_27': x__format_simple_table__mutmut_27, 
    'x__format_simple_table__mutmut_28': x__format_simple_table__mutmut_28, 
    'x__format_simple_table__mutmut_29': x__format_simple_table__mutmut_29, 
    'x__format_simple_table__mutmut_30': x__format_simple_table__mutmut_30
}

def _format_simple_table(*args, **kwargs):
    result = _mutmut_trampoline(x__format_simple_table__mutmut_orig, x__format_simple_table__mutmut_mutants, args, kwargs)
    return result 

_format_simple_table.__signature__ = _mutmut_signature(x__format_simple_table__mutmut_orig)
x__format_simple_table__mutmut_orig.__name__ = 'x__format_simple_table'


def x_format_table__mutmut_orig(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, columns)
    except ImportError:
        return _format_simple_table(response.hits, columns)


def x_format_table__mutmut_1(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, columns)
    except ImportError:
        return _format_simple_table(response.hits, columns)


def x_format_table__mutmut_2(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "XXNo results foundXX"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, columns)
    except ImportError:
        return _format_simple_table(response.hits, columns)


def x_format_table__mutmut_3(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "no results found"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, columns)
    except ImportError:
        return _format_simple_table(response.hits, columns)


def x_format_table__mutmut_4(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "NO RESULTS FOUND"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, columns)
    except ImportError:
        return _format_simple_table(response.hits, columns)


def x_format_table__mutmut_5(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is not None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, columns)
    except ImportError:
        return _format_simple_table(response.hits, columns)


def x_format_table__mutmut_6(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is None:
        columns = None
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, columns)
    except ImportError:
        return _format_simple_table(response.hits, columns)


def x_format_table__mutmut_7(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(None)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, columns)
    except ImportError:
        return _format_simple_table(response.hits, columns)


def x_format_table__mutmut_8(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = None

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, columns)
    except ImportError:
        return _format_simple_table(response.hits, columns)


def x_format_table__mutmut_9(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(None)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, columns)
    except ImportError:
        return _format_simple_table(response.hits, columns)


def x_format_table__mutmut_10(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(None, columns)
    except ImportError:
        return _format_simple_table(response.hits, columns)


def x_format_table__mutmut_11(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, None)
    except ImportError:
        return _format_simple_table(response.hits, columns)


def x_format_table__mutmut_12(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(columns)
    except ImportError:
        return _format_simple_table(response.hits, columns)


def x_format_table__mutmut_13(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, )
    except ImportError:
        return _format_simple_table(response.hits, columns)


def x_format_table__mutmut_14(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, columns)
    except ImportError:
        return _format_simple_table(None, columns)


def x_format_table__mutmut_15(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, columns)
    except ImportError:
        return _format_simple_table(response.hits, None)


def x_format_table__mutmut_16(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, columns)
    except ImportError:
        return _format_simple_table(columns)


def x_format_table__mutmut_17(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as a table.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        Table string

    """
    if not response.hits:
        return "No results found"

    # Determine columns if not provided
    if columns is None:
        columns = _determine_columns(response.hits)
        columns = _filter_internal_columns(columns)

    # Try to use tabulate if available
    try:
        return _format_with_tabulate(response.hits, columns)
    except ImportError:
        return _format_simple_table(response.hits, )

x_format_table__mutmut_mutants : ClassVar[MutantDict] = {
'x_format_table__mutmut_1': x_format_table__mutmut_1, 
    'x_format_table__mutmut_2': x_format_table__mutmut_2, 
    'x_format_table__mutmut_3': x_format_table__mutmut_3, 
    'x_format_table__mutmut_4': x_format_table__mutmut_4, 
    'x_format_table__mutmut_5': x_format_table__mutmut_5, 
    'x_format_table__mutmut_6': x_format_table__mutmut_6, 
    'x_format_table__mutmut_7': x_format_table__mutmut_7, 
    'x_format_table__mutmut_8': x_format_table__mutmut_8, 
    'x_format_table__mutmut_9': x_format_table__mutmut_9, 
    'x_format_table__mutmut_10': x_format_table__mutmut_10, 
    'x_format_table__mutmut_11': x_format_table__mutmut_11, 
    'x_format_table__mutmut_12': x_format_table__mutmut_12, 
    'x_format_table__mutmut_13': x_format_table__mutmut_13, 
    'x_format_table__mutmut_14': x_format_table__mutmut_14, 
    'x_format_table__mutmut_15': x_format_table__mutmut_15, 
    'x_format_table__mutmut_16': x_format_table__mutmut_16, 
    'x_format_table__mutmut_17': x_format_table__mutmut_17
}

def format_table(*args, **kwargs):
    result = _mutmut_trampoline(x_format_table__mutmut_orig, x_format_table__mutmut_mutants, args, kwargs)
    return result 

format_table.__signature__ = _mutmut_signature(x_format_table__mutmut_orig)
x_format_table__mutmut_orig.__name__ = 'x_format_table'


def x_format_csv__mutmut_orig(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_1(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_2(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return "XXXX"

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_3(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is not None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_4(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = None
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_5(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(None)
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_6(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = None

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_7(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(None)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_8(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = None
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_9(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = None

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_10(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(None, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_11(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=None, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_12(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction=None)

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_13(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_14(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_15(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, )

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_16(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="XXignoreXX")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_17(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="IGNORE")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_18(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "XX_timestampXX" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_19(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_TIMESTAMP" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_20(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" not in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_21(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = None
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_22(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = None
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_23(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["XX_timestampXX"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_24(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_TIMESTAMP"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_25(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = None
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_26(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(None)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_27(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp * 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_28(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1000001)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_29(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = None
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_30(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["XX_timestampXX"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_31(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_TIMESTAMP"] = dt.isoformat()
        writer.writerow(hit)

    return output.getvalue()


def x_format_csv__mutmut_32(response: SearchResponse, columns: list[str] | None = None) -> str:
    """Format response as CSV.

    Args:
        response: Search response
        columns: Specific columns to include (None for all)

    Returns:
        CSV string

    """
    if not response.hits:
        return ""

    # Determine columns
    if columns is None:
        all_keys: set[str] = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        columns = sorted(all_keys)

    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")

    writer.writeheader()
    for hit in response.hits:
        # Format timestamp for readability
        if "_timestamp" in hit:
            hit = hit.copy()
            timestamp = hit["_timestamp"]
            if timestamp:
                dt = datetime.fromtimestamp(timestamp / 1_000_000)
                hit["_timestamp"] = dt.isoformat()
        writer.writerow(None)

    return output.getvalue()

x_format_csv__mutmut_mutants : ClassVar[MutantDict] = {
'x_format_csv__mutmut_1': x_format_csv__mutmut_1, 
    'x_format_csv__mutmut_2': x_format_csv__mutmut_2, 
    'x_format_csv__mutmut_3': x_format_csv__mutmut_3, 
    'x_format_csv__mutmut_4': x_format_csv__mutmut_4, 
    'x_format_csv__mutmut_5': x_format_csv__mutmut_5, 
    'x_format_csv__mutmut_6': x_format_csv__mutmut_6, 
    'x_format_csv__mutmut_7': x_format_csv__mutmut_7, 
    'x_format_csv__mutmut_8': x_format_csv__mutmut_8, 
    'x_format_csv__mutmut_9': x_format_csv__mutmut_9, 
    'x_format_csv__mutmut_10': x_format_csv__mutmut_10, 
    'x_format_csv__mutmut_11': x_format_csv__mutmut_11, 
    'x_format_csv__mutmut_12': x_format_csv__mutmut_12, 
    'x_format_csv__mutmut_13': x_format_csv__mutmut_13, 
    'x_format_csv__mutmut_14': x_format_csv__mutmut_14, 
    'x_format_csv__mutmut_15': x_format_csv__mutmut_15, 
    'x_format_csv__mutmut_16': x_format_csv__mutmut_16, 
    'x_format_csv__mutmut_17': x_format_csv__mutmut_17, 
    'x_format_csv__mutmut_18': x_format_csv__mutmut_18, 
    'x_format_csv__mutmut_19': x_format_csv__mutmut_19, 
    'x_format_csv__mutmut_20': x_format_csv__mutmut_20, 
    'x_format_csv__mutmut_21': x_format_csv__mutmut_21, 
    'x_format_csv__mutmut_22': x_format_csv__mutmut_22, 
    'x_format_csv__mutmut_23': x_format_csv__mutmut_23, 
    'x_format_csv__mutmut_24': x_format_csv__mutmut_24, 
    'x_format_csv__mutmut_25': x_format_csv__mutmut_25, 
    'x_format_csv__mutmut_26': x_format_csv__mutmut_26, 
    'x_format_csv__mutmut_27': x_format_csv__mutmut_27, 
    'x_format_csv__mutmut_28': x_format_csv__mutmut_28, 
    'x_format_csv__mutmut_29': x_format_csv__mutmut_29, 
    'x_format_csv__mutmut_30': x_format_csv__mutmut_30, 
    'x_format_csv__mutmut_31': x_format_csv__mutmut_31, 
    'x_format_csv__mutmut_32': x_format_csv__mutmut_32
}

def format_csv(*args, **kwargs):
    result = _mutmut_trampoline(x_format_csv__mutmut_orig, x_format_csv__mutmut_mutants, args, kwargs)
    return result 

format_csv.__signature__ = _mutmut_signature(x_format_csv__mutmut_orig)
x_format_csv__mutmut_orig.__name__ = 'x_format_csv'


def x_format_summary__mutmut_orig(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_1(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = None

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_2(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(None)

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_3(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append(None)

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_4(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("XX⚠️  Results are partialXX")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_5(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_6(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  RESULTS ARE PARTIAL")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_7(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append(None)
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_8(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("XXErrors:XX")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_9(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_10(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("ERRORS:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_11(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(None)

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_12(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = None
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_13(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = None
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_14(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get(None, "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_15(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", None)
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_16(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_17(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", )
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_18(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("XXlevelXX", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_19(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("LEVEL", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_20(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "XXUNKNOWNXX")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_21(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "unknown")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_22(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = None

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_23(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) - 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_24(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(None, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_25(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, None) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_26(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_27(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, ) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_28(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 1) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_29(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 2

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_30(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append(None)
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_31(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("XX\nLevel distribution:XX")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_32(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nlevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_33(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLEVEL DISTRIBUTION:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_34(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(None):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def x_format_summary__mutmut_35(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(None)

    return "\n".join(lines)


def x_format_summary__mutmut_36(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(None)


def x_format_summary__mutmut_37(response: SearchResponse) -> str:
    """Format a summary of the search response.

    Args:
        response: Search response

    Returns:
        Summary string

    """
    lines = [
        f"Total hits: {response.total}",
        f"Returned: {len(response.hits)}",
        f"Query time: {response.took}ms",
        f"Scan size: {response.scan_size:,} bytes",
    ]

    if response.trace_id:
        lines.append(f"Trace ID: {response.trace_id}")

    if response.is_partial:
        lines.append("⚠️  Results are partial")

    if response.function_error:
        lines.append("Errors:")
        for error in response.function_error:
            lines.append(f"  - {error}")

    # Add level distribution if available
    level_counts: dict[str, int] = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "XX\nXX".join(lines)

x_format_summary__mutmut_mutants : ClassVar[MutantDict] = {
'x_format_summary__mutmut_1': x_format_summary__mutmut_1, 
    'x_format_summary__mutmut_2': x_format_summary__mutmut_2, 
    'x_format_summary__mutmut_3': x_format_summary__mutmut_3, 
    'x_format_summary__mutmut_4': x_format_summary__mutmut_4, 
    'x_format_summary__mutmut_5': x_format_summary__mutmut_5, 
    'x_format_summary__mutmut_6': x_format_summary__mutmut_6, 
    'x_format_summary__mutmut_7': x_format_summary__mutmut_7, 
    'x_format_summary__mutmut_8': x_format_summary__mutmut_8, 
    'x_format_summary__mutmut_9': x_format_summary__mutmut_9, 
    'x_format_summary__mutmut_10': x_format_summary__mutmut_10, 
    'x_format_summary__mutmut_11': x_format_summary__mutmut_11, 
    'x_format_summary__mutmut_12': x_format_summary__mutmut_12, 
    'x_format_summary__mutmut_13': x_format_summary__mutmut_13, 
    'x_format_summary__mutmut_14': x_format_summary__mutmut_14, 
    'x_format_summary__mutmut_15': x_format_summary__mutmut_15, 
    'x_format_summary__mutmut_16': x_format_summary__mutmut_16, 
    'x_format_summary__mutmut_17': x_format_summary__mutmut_17, 
    'x_format_summary__mutmut_18': x_format_summary__mutmut_18, 
    'x_format_summary__mutmut_19': x_format_summary__mutmut_19, 
    'x_format_summary__mutmut_20': x_format_summary__mutmut_20, 
    'x_format_summary__mutmut_21': x_format_summary__mutmut_21, 
    'x_format_summary__mutmut_22': x_format_summary__mutmut_22, 
    'x_format_summary__mutmut_23': x_format_summary__mutmut_23, 
    'x_format_summary__mutmut_24': x_format_summary__mutmut_24, 
    'x_format_summary__mutmut_25': x_format_summary__mutmut_25, 
    'x_format_summary__mutmut_26': x_format_summary__mutmut_26, 
    'x_format_summary__mutmut_27': x_format_summary__mutmut_27, 
    'x_format_summary__mutmut_28': x_format_summary__mutmut_28, 
    'x_format_summary__mutmut_29': x_format_summary__mutmut_29, 
    'x_format_summary__mutmut_30': x_format_summary__mutmut_30, 
    'x_format_summary__mutmut_31': x_format_summary__mutmut_31, 
    'x_format_summary__mutmut_32': x_format_summary__mutmut_32, 
    'x_format_summary__mutmut_33': x_format_summary__mutmut_33, 
    'x_format_summary__mutmut_34': x_format_summary__mutmut_34, 
    'x_format_summary__mutmut_35': x_format_summary__mutmut_35, 
    'x_format_summary__mutmut_36': x_format_summary__mutmut_36, 
    'x_format_summary__mutmut_37': x_format_summary__mutmut_37
}

def format_summary(*args, **kwargs):
    result = _mutmut_trampoline(x_format_summary__mutmut_orig, x_format_summary__mutmut_mutants, args, kwargs)
    return result 

format_summary.__signature__ = _mutmut_signature(x_format_summary__mutmut_orig)
x_format_summary__mutmut_orig.__name__ = 'x_format_summary'


def x__format_as_log__mutmut_orig(response: SearchResponse | dict[str, Any]) -> str:
    """Format response as log lines."""
    if isinstance(response, dict):
        return format_log_line(response)
    return "\n".join(format_log_line(hit) for hit in response.hits)


def x__format_as_log__mutmut_1(response: SearchResponse | dict[str, Any]) -> str:
    """Format response as log lines."""
    if isinstance(response, dict):
        return format_log_line(None)
    return "\n".join(format_log_line(hit) for hit in response.hits)


def x__format_as_log__mutmut_2(response: SearchResponse | dict[str, Any]) -> str:
    """Format response as log lines."""
    if isinstance(response, dict):
        return format_log_line(response)
    return "\n".join(None)


def x__format_as_log__mutmut_3(response: SearchResponse | dict[str, Any]) -> str:
    """Format response as log lines."""
    if isinstance(response, dict):
        return format_log_line(response)
    return "XX\nXX".join(format_log_line(hit) for hit in response.hits)


def x__format_as_log__mutmut_4(response: SearchResponse | dict[str, Any]) -> str:
    """Format response as log lines."""
    if isinstance(response, dict):
        return format_log_line(response)
    return "\n".join(format_log_line(None) for hit in response.hits)

x__format_as_log__mutmut_mutants : ClassVar[MutantDict] = {
'x__format_as_log__mutmut_1': x__format_as_log__mutmut_1, 
    'x__format_as_log__mutmut_2': x__format_as_log__mutmut_2, 
    'x__format_as_log__mutmut_3': x__format_as_log__mutmut_3, 
    'x__format_as_log__mutmut_4': x__format_as_log__mutmut_4
}

def _format_as_log(*args, **kwargs):
    result = _mutmut_trampoline(x__format_as_log__mutmut_orig, x__format_as_log__mutmut_mutants, args, kwargs)
    return result 

_format_as_log.__signature__ = _mutmut_signature(x__format_as_log__mutmut_orig)
x__format_as_log__mutmut_orig.__name__ = 'x__format_as_log'


def x__format_as_table__mutmut_orig(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=0,
    )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_1(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(None, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=0,
    )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_2(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(**kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=0,
    )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_3(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, )
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=0,
    )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_4(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = None
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_5(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=None,
        total=1,
        took=0,
        scan_size=0,
    )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_6(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=None,
        took=0,
        scan_size=0,
    )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_7(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=None,
        scan_size=0,
    )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_8(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=None,
    )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_9(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        total=1,
        took=0,
        scan_size=0,
    )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_10(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        took=0,
        scan_size=0,
    )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_11(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=1,
        scan_size=0,
    )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_12(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_13(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=2,
        took=0,
        scan_size=0,
    )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_14(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=1,
        scan_size=0,
    )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_15(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=1,
    )
    return format_table(single_response, **kwargs)


def x__format_as_table__mutmut_16(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=0,
    )
    return format_table(None, **kwargs)


def x__format_as_table__mutmut_17(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=0,
    )
    return format_table(**kwargs)


def x__format_as_table__mutmut_18(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as table."""
    if isinstance(response, SearchResponse):
        return format_table(response, **kwargs)
    # Single entry as table
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=0,
    )
    return format_table(single_response, )

x__format_as_table__mutmut_mutants : ClassVar[MutantDict] = {
'x__format_as_table__mutmut_1': x__format_as_table__mutmut_1, 
    'x__format_as_table__mutmut_2': x__format_as_table__mutmut_2, 
    'x__format_as_table__mutmut_3': x__format_as_table__mutmut_3, 
    'x__format_as_table__mutmut_4': x__format_as_table__mutmut_4, 
    'x__format_as_table__mutmut_5': x__format_as_table__mutmut_5, 
    'x__format_as_table__mutmut_6': x__format_as_table__mutmut_6, 
    'x__format_as_table__mutmut_7': x__format_as_table__mutmut_7, 
    'x__format_as_table__mutmut_8': x__format_as_table__mutmut_8, 
    'x__format_as_table__mutmut_9': x__format_as_table__mutmut_9, 
    'x__format_as_table__mutmut_10': x__format_as_table__mutmut_10, 
    'x__format_as_table__mutmut_11': x__format_as_table__mutmut_11, 
    'x__format_as_table__mutmut_12': x__format_as_table__mutmut_12, 
    'x__format_as_table__mutmut_13': x__format_as_table__mutmut_13, 
    'x__format_as_table__mutmut_14': x__format_as_table__mutmut_14, 
    'x__format_as_table__mutmut_15': x__format_as_table__mutmut_15, 
    'x__format_as_table__mutmut_16': x__format_as_table__mutmut_16, 
    'x__format_as_table__mutmut_17': x__format_as_table__mutmut_17, 
    'x__format_as_table__mutmut_18': x__format_as_table__mutmut_18
}

def _format_as_table(*args, **kwargs):
    result = _mutmut_trampoline(x__format_as_table__mutmut_orig, x__format_as_table__mutmut_mutants, args, kwargs)
    return result 

_format_as_table.__signature__ = _mutmut_signature(x__format_as_table__mutmut_orig)
x__format_as_table__mutmut_orig.__name__ = 'x__format_as_table'


def x__format_as_csv__mutmut_orig(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=0,
    )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_1(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(None, **kwargs)
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=0,
    )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_2(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(**kwargs)
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=0,
    )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_3(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, )
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=0,
    )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_4(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = None
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_5(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        hits=None,
        total=1,
        took=0,
        scan_size=0,
    )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_6(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        hits=[response],
        total=None,
        took=0,
        scan_size=0,
    )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_7(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=None,
        scan_size=0,
    )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_8(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=None,
    )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_9(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        total=1,
        took=0,
        scan_size=0,
    )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_10(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        hits=[response],
        took=0,
        scan_size=0,
    )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_11(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        hits=[response],
        total=1,
        scan_size=0,
    )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_12(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_13(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        hits=[response],
        total=2,
        took=0,
        scan_size=0,
    )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_14(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=1,
        scan_size=0,
    )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_15(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=1,
    )
    return format_csv(single_response, **kwargs)


def x__format_as_csv__mutmut_16(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=0,
    )
    return format_csv(None, **kwargs)


def x__format_as_csv__mutmut_17(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=0,
    )
    return format_csv(**kwargs)


def x__format_as_csv__mutmut_18(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
    """Format response as CSV."""
    if isinstance(response, SearchResponse):
        return format_csv(response, **kwargs)
    single_response = SearchResponse(
        hits=[response],
        total=1,
        took=0,
        scan_size=0,
    )
    return format_csv(single_response, )

x__format_as_csv__mutmut_mutants : ClassVar[MutantDict] = {
'x__format_as_csv__mutmut_1': x__format_as_csv__mutmut_1, 
    'x__format_as_csv__mutmut_2': x__format_as_csv__mutmut_2, 
    'x__format_as_csv__mutmut_3': x__format_as_csv__mutmut_3, 
    'x__format_as_csv__mutmut_4': x__format_as_csv__mutmut_4, 
    'x__format_as_csv__mutmut_5': x__format_as_csv__mutmut_5, 
    'x__format_as_csv__mutmut_6': x__format_as_csv__mutmut_6, 
    'x__format_as_csv__mutmut_7': x__format_as_csv__mutmut_7, 
    'x__format_as_csv__mutmut_8': x__format_as_csv__mutmut_8, 
    'x__format_as_csv__mutmut_9': x__format_as_csv__mutmut_9, 
    'x__format_as_csv__mutmut_10': x__format_as_csv__mutmut_10, 
    'x__format_as_csv__mutmut_11': x__format_as_csv__mutmut_11, 
    'x__format_as_csv__mutmut_12': x__format_as_csv__mutmut_12, 
    'x__format_as_csv__mutmut_13': x__format_as_csv__mutmut_13, 
    'x__format_as_csv__mutmut_14': x__format_as_csv__mutmut_14, 
    'x__format_as_csv__mutmut_15': x__format_as_csv__mutmut_15, 
    'x__format_as_csv__mutmut_16': x__format_as_csv__mutmut_16, 
    'x__format_as_csv__mutmut_17': x__format_as_csv__mutmut_17, 
    'x__format_as_csv__mutmut_18': x__format_as_csv__mutmut_18
}

def _format_as_csv(*args, **kwargs):
    result = _mutmut_trampoline(x__format_as_csv__mutmut_orig, x__format_as_csv__mutmut_mutants, args, kwargs)
    return result 

_format_as_csv.__signature__ = _mutmut_signature(x__format_as_csv__mutmut_orig)
x__format_as_csv__mutmut_orig.__name__ = 'x__format_as_csv'


def x__format_as_summary__mutmut_orig(response: SearchResponse | dict[str, Any]) -> str:
    """Format response as summary."""
    if isinstance(response, SearchResponse):
        return format_summary(response)
    return "Single log entry (use 'log' or 'json' format for details)"


def x__format_as_summary__mutmut_1(response: SearchResponse | dict[str, Any]) -> str:
    """Format response as summary."""
    if isinstance(response, SearchResponse):
        return format_summary(None)
    return "Single log entry (use 'log' or 'json' format for details)"


def x__format_as_summary__mutmut_2(response: SearchResponse | dict[str, Any]) -> str:
    """Format response as summary."""
    if isinstance(response, SearchResponse):
        return format_summary(response)
    return "XXSingle log entry (use 'log' or 'json' format for details)XX"


def x__format_as_summary__mutmut_3(response: SearchResponse | dict[str, Any]) -> str:
    """Format response as summary."""
    if isinstance(response, SearchResponse):
        return format_summary(response)
    return "single log entry (use 'log' or 'json' format for details)"


def x__format_as_summary__mutmut_4(response: SearchResponse | dict[str, Any]) -> str:
    """Format response as summary."""
    if isinstance(response, SearchResponse):
        return format_summary(response)
    return "SINGLE LOG ENTRY (USE 'LOG' OR 'JSON' FORMAT FOR DETAILS)"

x__format_as_summary__mutmut_mutants : ClassVar[MutantDict] = {
'x__format_as_summary__mutmut_1': x__format_as_summary__mutmut_1, 
    'x__format_as_summary__mutmut_2': x__format_as_summary__mutmut_2, 
    'x__format_as_summary__mutmut_3': x__format_as_summary__mutmut_3, 
    'x__format_as_summary__mutmut_4': x__format_as_summary__mutmut_4
}

def _format_as_summary(*args, **kwargs):
    result = _mutmut_trampoline(x__format_as_summary__mutmut_orig, x__format_as_summary__mutmut_mutants, args, kwargs)
    return result 

_format_as_summary.__signature__ = _mutmut_signature(x__format_as_summary__mutmut_orig)
x__format_as_summary__mutmut_orig.__name__ = 'x__format_as_summary'


def x_format_output__mutmut_orig(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_1(
    response: SearchResponse | dict[str, Any],
    format_type: str = "XXlogXX",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_2(
    response: SearchResponse | dict[str, Any],
    format_type: str = "LOG",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_3(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_4(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_5(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_6(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_7(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_8(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)


def x_format_output__mutmut_9(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.upper():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_10(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "XXjsonXX":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_11(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "JSON":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_12(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(None, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_13(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(**kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_14(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, )
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_15(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "XXlogXX":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_16(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "LOG":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_17(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(None)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_18(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "XXtableXX":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_19(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "TABLE":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_20(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(None, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_21(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(**kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_22(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, )
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_23(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "XXcsvXX":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_24(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "CSV":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_25(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(None, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_26(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(**kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_27(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, )
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_28(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "XXsummaryXX":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_29(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "SUMMARY":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_30(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(None)
        case _:
            # Default to log format
            return _format_as_log(response)


def x_format_output__mutmut_31(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs: Any,
) -> str:
    """Format output based on specified type.

    Args:
        response: Search response or log entry
        format_type: Output format (json, log, table, csv, summary)
        **kwargs: Additional format-specific options

    Returns:
        Formatted string

    """
    match format_type.lower():
        case "json":
            return format_json(response, **kwargs)
        case "log":
            return _format_as_log(response)
        case "table":
            return _format_as_table(response, **kwargs)
        case "csv":
            return _format_as_csv(response, **kwargs)
        case "summary":
            return _format_as_summary(response)
        case _:
            # Default to log format
            return _format_as_log(None)

x_format_output__mutmut_mutants : ClassVar[MutantDict] = {
'x_format_output__mutmut_1': x_format_output__mutmut_1, 
    'x_format_output__mutmut_2': x_format_output__mutmut_2, 
    'x_format_output__mutmut_3': x_format_output__mutmut_3, 
    'x_format_output__mutmut_4': x_format_output__mutmut_4, 
    'x_format_output__mutmut_5': x_format_output__mutmut_5, 
    'x_format_output__mutmut_6': x_format_output__mutmut_6, 
    'x_format_output__mutmut_7': x_format_output__mutmut_7, 
    'x_format_output__mutmut_8': x_format_output__mutmut_8, 
    'x_format_output__mutmut_9': x_format_output__mutmut_9, 
    'x_format_output__mutmut_10': x_format_output__mutmut_10, 
    'x_format_output__mutmut_11': x_format_output__mutmut_11, 
    'x_format_output__mutmut_12': x_format_output__mutmut_12, 
    'x_format_output__mutmut_13': x_format_output__mutmut_13, 
    'x_format_output__mutmut_14': x_format_output__mutmut_14, 
    'x_format_output__mutmut_15': x_format_output__mutmut_15, 
    'x_format_output__mutmut_16': x_format_output__mutmut_16, 
    'x_format_output__mutmut_17': x_format_output__mutmut_17, 
    'x_format_output__mutmut_18': x_format_output__mutmut_18, 
    'x_format_output__mutmut_19': x_format_output__mutmut_19, 
    'x_format_output__mutmut_20': x_format_output__mutmut_20, 
    'x_format_output__mutmut_21': x_format_output__mutmut_21, 
    'x_format_output__mutmut_22': x_format_output__mutmut_22, 
    'x_format_output__mutmut_23': x_format_output__mutmut_23, 
    'x_format_output__mutmut_24': x_format_output__mutmut_24, 
    'x_format_output__mutmut_25': x_format_output__mutmut_25, 
    'x_format_output__mutmut_26': x_format_output__mutmut_26, 
    'x_format_output__mutmut_27': x_format_output__mutmut_27, 
    'x_format_output__mutmut_28': x_format_output__mutmut_28, 
    'x_format_output__mutmut_29': x_format_output__mutmut_29, 
    'x_format_output__mutmut_30': x_format_output__mutmut_30, 
    'x_format_output__mutmut_31': x_format_output__mutmut_31
}

def format_output(*args, **kwargs):
    result = _mutmut_trampoline(x_format_output__mutmut_orig, x_format_output__mutmut_mutants, args, kwargs)
    return result 

format_output.__signature__ = _mutmut_signature(x_format_output__mutmut_orig)
x_format_output__mutmut_orig.__name__ = 'x_format_output'


# <3 🧱🤝🔌🪄
