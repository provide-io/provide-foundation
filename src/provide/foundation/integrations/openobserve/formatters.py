"""
Output formatting utilities for OpenObserve results.
"""

import csv
from datetime import datetime
import io
import json
from typing import Any

from provide.foundation.integrations.openobserve.models import SearchResponse


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
        return json.dumps(data, indent=2, sort_keys=False)
    else:
        return json.dumps(data)


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

    # Determine columns
    if columns is None:
        # Get all unique keys from hits
        all_keys = set()
        for hit in response.hits:
            all_keys.update(hit.keys())
        # Sort columns, putting common ones first
        priority_cols = ["_timestamp", "level", "service", "message"]
        columns = []
        for col in priority_cols:
            if col in all_keys:
                columns.append(col)
                all_keys.remove(col)
        columns.extend(sorted(all_keys))

    # Filter out internal columns if not explicitly requested
    if "_p" in columns and "_p" not in (columns or []):
        columns = [c for c in columns if not c.startswith("_") or c == "_timestamp"]

    # Try to use tabulate if available
    try:
        from tabulate import tabulate

        # Prepare data
        headers = columns
        rows = []
        for hit in response.hits:
            row = []
            for col in columns:
                value = hit.get(col, "")
                # Format timestamp
                if col == "_timestamp" and value:
                    dt = datetime.fromtimestamp(value / 1_000_000)
                    value = dt.strftime("%Y-%m-%d %H:%M:%S")
                # Truncate long values
                value_str = str(value)
                if len(value_str) > 50:
                    value_str = value_str[:47] + "..."
                row.append(value_str)
            rows.append(row)

        return tabulate(rows, headers=headers, tablefmt="grid")

    except ImportError:
        # Fallback to simple formatting
        lines = []

        # Header
        lines.append(" | ".join(columns))
        lines.append("-" * (len(columns) * 15))

        # Rows
        for hit in response.hits:
            row_values = []
            for col in columns:
                value = hit.get(col, "")
                if col == "_timestamp" and value:
                    dt = datetime.fromtimestamp(value / 1_000_000)
                    value = dt.strftime("%H:%M:%S")
                value_str = str(value)[:12]
                row_values.append(value_str)
            lines.append(" | ".join(row_values))

        return "\n".join(lines)


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
        all_keys = set()
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
    level_counts = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        level_counts[level] = level_counts.get(level, 0) + 1

    if level_counts:
        lines.append("\nLevel distribution:")
        for level, count in sorted(level_counts.items()):
            lines.append(f"  {level}: {count}")

    return "\n".join(lines)


def format_output(
    response: SearchResponse | dict[str, Any],
    format_type: str = "log",
    **kwargs,
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
            if isinstance(response, dict):
                return format_log_line(response)
            else:
                return "\n".join(format_log_line(hit) for hit in response.hits)
        case "table":
            if isinstance(response, SearchResponse):
                return format_table(response, **kwargs)
            else:
                # Single entry as table
                single_response = SearchResponse(
                    hits=[response],
                    total=1,
                    took=0,
                    scan_size=0,
                )
                return format_table(single_response, **kwargs)
        case "csv":
            if isinstance(response, SearchResponse):
                return format_csv(response, **kwargs)
            else:
                single_response = SearchResponse(
                    hits=[response],
                    total=1,
                    took=0,
                    scan_size=0,
                )
                return format_csv(single_response, **kwargs)
        case "summary":
            if isinstance(response, SearchResponse):
                return format_summary(response)
            else:
                return "Single log entry (use 'log' or 'json' format for details)"
        case _:
            # Default to log format
            if isinstance(response, dict):
                return format_log_line(response)
            else:
                return "\n".join(format_log_line(hit) for hit in response.hits)
