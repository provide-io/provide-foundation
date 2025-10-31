#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import csv
from datetime import datetime
import io
from typing import Any

from provide.foundation.integrations.openobserve.models import SearchResponse
from provide.foundation.serialization import json_dumps

"""Output formatting utilities for OpenObserve results."""


def format_json(response: SearchResponse | dict[str, Any], pretty: bool = True) -> str:
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


def format_log_line(entry: dict[str, Any]) -> str:
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


def _determine_columns(hits: list[dict[str, Any]]) -> list[str]:
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


def _filter_internal_columns(columns: list[str]) -> list[str]:
    """Filter out internal columns if not explicitly requested."""
    if "_p" in columns:
        return [c for c in columns if not c.startswith("_") or c == "_timestamp"]
    return columns


def _format_cell_value(col: str, value: Any, max_length: int = 50) -> str:
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


def _format_with_tabulate(hits: list[dict[str, Any]], columns: list[str]) -> str:
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


def _format_simple_table(hits: list[dict[str, Any]], columns: list[str]) -> str:
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


def format_table(response: SearchResponse, columns: list[str] | None = None) -> str:
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


def format_csv(response: SearchResponse, columns: list[str] | None = None) -> str:
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


def format_summary(response: SearchResponse) -> str:
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


def _format_as_log(response: SearchResponse | dict[str, Any]) -> str:
    """Format response as log lines."""
    if isinstance(response, dict):
        return format_log_line(response)
    return "\n".join(format_log_line(hit) for hit in response.hits)


def _format_as_table(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
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


def _format_as_csv(response: SearchResponse | dict[str, Any], **kwargs: Any) -> str:
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


def _format_as_summary(response: SearchResponse | dict[str, Any]) -> str:
    """Format response as summary."""
    if isinstance(response, SearchResponse):
        return format_summary(response)
    return "Single log entry (use 'log' or 'json' format for details)"


def format_output(
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


# 🧱🏗️🔚
