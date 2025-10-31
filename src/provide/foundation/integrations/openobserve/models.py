#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from attrs import define, field

"""Data models for OpenObserve API requests and responses."""


@define(slots=True)
class SearchQuery:
    """Search query parameters for OpenObserve."""

    sql: str
    start_time: int  # Microseconds since epoch
    end_time: int  # Microseconds since epoch
    from_offset: int = 0
    size: int = 100

    def to_dict(self) -> dict[str, Any]:
        """Convert to API request format."""
        return {
            "query": {
                "sql": self.sql,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "from": self.from_offset,
                "size": self.size,
            },
        }


@define(slots=True)
class SearchResponse:
    """Response from OpenObserve search API."""

    hits: list[dict[str, Any]]
    total: int
    took: int  # Milliseconds
    scan_size: int
    trace_id: str | None = None
    from_offset: int = 0
    size: int = 0
    is_partial: bool = False
    function_error: list[str] = field(factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SearchResponse:
        """Create from API response."""
        return cls(
            hits=data.get("hits", []),
            total=data.get("total", 0),
            took=data.get("took", 0),
            scan_size=data.get("scan_size", 0),
            trace_id=data.get("trace_id"),
            from_offset=data.get("from", 0),
            size=data.get("size", 0),
            is_partial=data.get("is_partial", False),
            function_error=data.get("function_error", []),
        )


@define(slots=True)
class StreamInfo:
    """Information about an OpenObserve stream."""

    name: str
    storage_type: str
    stream_type: str
    doc_count: int = 0
    compressed_size: int = 0
    original_size: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StreamInfo:
        """Create from API response."""
        return cls(
            name=data.get("name", ""),
            storage_type=data.get("storage_type", ""),
            stream_type=data.get("stream_type", ""),
            doc_count=data.get("stats", {}).get("doc_count", 0),
            compressed_size=data.get("stats", {}).get("compressed_size", 0),
            original_size=data.get("stats", {}).get("original_size", 0),
        )


def parse_relative_time(time_str: str, now: datetime | None = None) -> int:
    """Parse relative time strings like '-1h', '-30m' to microseconds since epoch.

    Args:
        time_str: Time string (e.g., '-1h', '-30m', 'now')
        now: Current time (for testing), defaults to datetime.now()

    Returns:
        Microseconds since epoch

    """
    from datetime import timedelta

    if now is None:
        now = datetime.now()

    if time_str == "now":
        return int(now.timestamp() * 1_000_000)

    if time_str.startswith("-"):
        # Parse relative time
        value = time_str[1:]
        if value.endswith("h"):
            delta = timedelta(hours=int(value[:-1]))
        elif value.endswith("m"):
            delta = timedelta(minutes=int(value[:-1]))
        elif value.endswith("s"):
            delta = timedelta(seconds=int(value[:-1]))
        elif value.endswith("d"):
            delta = timedelta(days=int(value[:-1]))
        else:
            # Assume seconds if no unit
            delta = timedelta(seconds=int(value))

        target_time = now - delta
        return int(target_time.timestamp() * 1_000_000)

    # Try to parse as timestamp
    try:
        timestamp = int(time_str)
        # If it's already in microseconds (large number), return as-is
        if timestamp > 1_000_000_000_000:
            return timestamp
        # Otherwise assume seconds and convert
        return timestamp * 1_000_000
    except ValueError:
        # Try to parse as ISO datetime
        dt = datetime.fromisoformat(time_str)
        return int(dt.timestamp() * 1_000_000)


# 🧱🏗️🔚
