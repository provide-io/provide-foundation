# provide/foundation/integrations/openobserve/streaming.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Streaming search operations for OpenObserve using Foundation transport."""

from __future__ import annotations

from collections.abc import AsyncGenerator, Generator
import re
import time
from typing import Any

from provide.foundation.console.output import perr
from provide.foundation.errors import ValidationError
from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveStreamingError,
)
from provide.foundation.integrations.openobserve.models import parse_relative_time
from provide.foundation.serialization import json_dumps, json_loads
from provide.foundation.utils.async_helpers import run_async
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


def x_stream_logs__mutmut_orig(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_1(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 6,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_2(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is not None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_3(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = None

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_4(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is not None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_5(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = None
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_6(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time(None)
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_7(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("XX-1mXX")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_8(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1M")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_9(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = None
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_10(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(None)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_11(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = None
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_12(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = None

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_13(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while False:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_14(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = None

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_15(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(None)

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_16(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=None,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_17(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=None,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_18(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time=None,
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_19(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=None,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_20(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_21(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_22(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_23(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_24(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="XXnowXX",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_25(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="NOW",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_26(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1001,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_27(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = None
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_28(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get(None, 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_29(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", None)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_30(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get(0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_31(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get(
                    "_timestamp",
                )
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_32(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("XX_timestampXX", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_33(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_TIMESTAMP", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_34(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 1)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_35(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = None

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_36(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(None)}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_37(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(None, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_38(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=None))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_39(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_40(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_41(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=False))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_42(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_43(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(None)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_44(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp >= last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_45(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = None  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_46(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp - 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_47(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 2  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_48(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = None
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_49(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time(None)
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_50(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("XX-1mXX")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_51(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1M")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_52(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = None

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_53(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(None) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_54(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(None)[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_55(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split("XX:XX")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_56(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[1]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_57(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) >= cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_58(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(None)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_59(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            return
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_60(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(None)
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def x_stream_logs__mutmut_61(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(None) from e


x_stream_logs__mutmut_mutants: ClassVar[MutantDict] = {
    "x_stream_logs__mutmut_1": x_stream_logs__mutmut_1,
    "x_stream_logs__mutmut_2": x_stream_logs__mutmut_2,
    "x_stream_logs__mutmut_3": x_stream_logs__mutmut_3,
    "x_stream_logs__mutmut_4": x_stream_logs__mutmut_4,
    "x_stream_logs__mutmut_5": x_stream_logs__mutmut_5,
    "x_stream_logs__mutmut_6": x_stream_logs__mutmut_6,
    "x_stream_logs__mutmut_7": x_stream_logs__mutmut_7,
    "x_stream_logs__mutmut_8": x_stream_logs__mutmut_8,
    "x_stream_logs__mutmut_9": x_stream_logs__mutmut_9,
    "x_stream_logs__mutmut_10": x_stream_logs__mutmut_10,
    "x_stream_logs__mutmut_11": x_stream_logs__mutmut_11,
    "x_stream_logs__mutmut_12": x_stream_logs__mutmut_12,
    "x_stream_logs__mutmut_13": x_stream_logs__mutmut_13,
    "x_stream_logs__mutmut_14": x_stream_logs__mutmut_14,
    "x_stream_logs__mutmut_15": x_stream_logs__mutmut_15,
    "x_stream_logs__mutmut_16": x_stream_logs__mutmut_16,
    "x_stream_logs__mutmut_17": x_stream_logs__mutmut_17,
    "x_stream_logs__mutmut_18": x_stream_logs__mutmut_18,
    "x_stream_logs__mutmut_19": x_stream_logs__mutmut_19,
    "x_stream_logs__mutmut_20": x_stream_logs__mutmut_20,
    "x_stream_logs__mutmut_21": x_stream_logs__mutmut_21,
    "x_stream_logs__mutmut_22": x_stream_logs__mutmut_22,
    "x_stream_logs__mutmut_23": x_stream_logs__mutmut_23,
    "x_stream_logs__mutmut_24": x_stream_logs__mutmut_24,
    "x_stream_logs__mutmut_25": x_stream_logs__mutmut_25,
    "x_stream_logs__mutmut_26": x_stream_logs__mutmut_26,
    "x_stream_logs__mutmut_27": x_stream_logs__mutmut_27,
    "x_stream_logs__mutmut_28": x_stream_logs__mutmut_28,
    "x_stream_logs__mutmut_29": x_stream_logs__mutmut_29,
    "x_stream_logs__mutmut_30": x_stream_logs__mutmut_30,
    "x_stream_logs__mutmut_31": x_stream_logs__mutmut_31,
    "x_stream_logs__mutmut_32": x_stream_logs__mutmut_32,
    "x_stream_logs__mutmut_33": x_stream_logs__mutmut_33,
    "x_stream_logs__mutmut_34": x_stream_logs__mutmut_34,
    "x_stream_logs__mutmut_35": x_stream_logs__mutmut_35,
    "x_stream_logs__mutmut_36": x_stream_logs__mutmut_36,
    "x_stream_logs__mutmut_37": x_stream_logs__mutmut_37,
    "x_stream_logs__mutmut_38": x_stream_logs__mutmut_38,
    "x_stream_logs__mutmut_39": x_stream_logs__mutmut_39,
    "x_stream_logs__mutmut_40": x_stream_logs__mutmut_40,
    "x_stream_logs__mutmut_41": x_stream_logs__mutmut_41,
    "x_stream_logs__mutmut_42": x_stream_logs__mutmut_42,
    "x_stream_logs__mutmut_43": x_stream_logs__mutmut_43,
    "x_stream_logs__mutmut_44": x_stream_logs__mutmut_44,
    "x_stream_logs__mutmut_45": x_stream_logs__mutmut_45,
    "x_stream_logs__mutmut_46": x_stream_logs__mutmut_46,
    "x_stream_logs__mutmut_47": x_stream_logs__mutmut_47,
    "x_stream_logs__mutmut_48": x_stream_logs__mutmut_48,
    "x_stream_logs__mutmut_49": x_stream_logs__mutmut_49,
    "x_stream_logs__mutmut_50": x_stream_logs__mutmut_50,
    "x_stream_logs__mutmut_51": x_stream_logs__mutmut_51,
    "x_stream_logs__mutmut_52": x_stream_logs__mutmut_52,
    "x_stream_logs__mutmut_53": x_stream_logs__mutmut_53,
    "x_stream_logs__mutmut_54": x_stream_logs__mutmut_54,
    "x_stream_logs__mutmut_55": x_stream_logs__mutmut_55,
    "x_stream_logs__mutmut_56": x_stream_logs__mutmut_56,
    "x_stream_logs__mutmut_57": x_stream_logs__mutmut_57,
    "x_stream_logs__mutmut_58": x_stream_logs__mutmut_58,
    "x_stream_logs__mutmut_59": x_stream_logs__mutmut_59,
    "x_stream_logs__mutmut_60": x_stream_logs__mutmut_60,
    "x_stream_logs__mutmut_61": x_stream_logs__mutmut_61,
}


def stream_logs(*args, **kwargs):
    result = _mutmut_trampoline(x_stream_logs__mutmut_orig, x_stream_logs__mutmut_mutants, args, kwargs)
    return result


stream_logs.__signature__ = _mutmut_signature(x_stream_logs__mutmut_orig)
x_stream_logs__mutmut_orig.__name__ = "x_stream_logs"


def x__parse_time_param__mutmut_orig(time_param: str | int | None, default: str) -> int:
    """Parse time parameter to microseconds."""
    if time_param is None:
        return parse_relative_time(default)
    if isinstance(time_param, str):
        return parse_relative_time(time_param)
    return time_param


def x__parse_time_param__mutmut_1(time_param: str | int | None, default: str) -> int:
    """Parse time parameter to microseconds."""
    if time_param is not None:
        return parse_relative_time(default)
    if isinstance(time_param, str):
        return parse_relative_time(time_param)
    return time_param


def x__parse_time_param__mutmut_2(time_param: str | int | None, default: str) -> int:
    """Parse time parameter to microseconds."""
    if time_param is None:
        return parse_relative_time(None)
    if isinstance(time_param, str):
        return parse_relative_time(time_param)
    return time_param


def x__parse_time_param__mutmut_3(time_param: str | int | None, default: str) -> int:
    """Parse time parameter to microseconds."""
    if time_param is None:
        return parse_relative_time(default)
    if isinstance(time_param, str):
        return parse_relative_time(None)
    return time_param


x__parse_time_param__mutmut_mutants: ClassVar[MutantDict] = {
    "x__parse_time_param__mutmut_1": x__parse_time_param__mutmut_1,
    "x__parse_time_param__mutmut_2": x__parse_time_param__mutmut_2,
    "x__parse_time_param__mutmut_3": x__parse_time_param__mutmut_3,
}


def _parse_time_param(*args, **kwargs):
    result = _mutmut_trampoline(
        x__parse_time_param__mutmut_orig, x__parse_time_param__mutmut_mutants, args, kwargs
    )
    return result


_parse_time_param.__signature__ = _mutmut_signature(x__parse_time_param__mutmut_orig)
x__parse_time_param__mutmut_orig.__name__ = "x__parse_time_param"


def x__process_stream_line__mutmut_orig(line: str) -> list[dict[str, Any]]:
    """Process a single line from stream response."""
    if not line:
        return []

    try:
        parsed_data = json_loads(line)
        if isinstance(parsed_data, dict):
            if "hits" in parsed_data:
                return parsed_data["hits"]
            return [parsed_data]
    except Exception:
        pass

    return []


def x__process_stream_line__mutmut_1(line: str) -> list[dict[str, Any]]:
    """Process a single line from stream response."""
    if line:
        return []

    try:
        parsed_data = json_loads(line)
        if isinstance(parsed_data, dict):
            if "hits" in parsed_data:
                return parsed_data["hits"]
            return [parsed_data]
    except Exception:
        pass

    return []


def x__process_stream_line__mutmut_2(line: str) -> list[dict[str, Any]]:
    """Process a single line from stream response."""
    if not line:
        return []

    try:
        parsed_data = None
        if isinstance(parsed_data, dict):
            if "hits" in parsed_data:
                return parsed_data["hits"]
            return [parsed_data]
    except Exception:
        pass

    return []


def x__process_stream_line__mutmut_3(line: str) -> list[dict[str, Any]]:
    """Process a single line from stream response."""
    if not line:
        return []

    try:
        parsed_data = json_loads(None)
        if isinstance(parsed_data, dict):
            if "hits" in parsed_data:
                return parsed_data["hits"]
            return [parsed_data]
    except Exception:
        pass

    return []


def x__process_stream_line__mutmut_4(line: str) -> list[dict[str, Any]]:
    """Process a single line from stream response."""
    if not line:
        return []

    try:
        parsed_data = json_loads(line)
        if isinstance(parsed_data, dict):
            if "XXhitsXX" in parsed_data:
                return parsed_data["hits"]
            return [parsed_data]
    except Exception:
        pass

    return []


def x__process_stream_line__mutmut_5(line: str) -> list[dict[str, Any]]:
    """Process a single line from stream response."""
    if not line:
        return []

    try:
        parsed_data = json_loads(line)
        if isinstance(parsed_data, dict):
            if "HITS" in parsed_data:
                return parsed_data["hits"]
            return [parsed_data]
    except Exception:
        pass

    return []


def x__process_stream_line__mutmut_6(line: str) -> list[dict[str, Any]]:
    """Process a single line from stream response."""
    if not line:
        return []

    try:
        parsed_data = json_loads(line)
        if isinstance(parsed_data, dict):
            if "hits" not in parsed_data:
                return parsed_data["hits"]
            return [parsed_data]
    except Exception:
        pass

    return []


def x__process_stream_line__mutmut_7(line: str) -> list[dict[str, Any]]:
    """Process a single line from stream response."""
    if not line:
        return []

    try:
        parsed_data = json_loads(line)
        if isinstance(parsed_data, dict):
            if "hits" in parsed_data:
                return parsed_data["XXhitsXX"]
            return [parsed_data]
    except Exception:
        pass

    return []


def x__process_stream_line__mutmut_8(line: str) -> list[dict[str, Any]]:
    """Process a single line from stream response."""
    if not line:
        return []

    try:
        parsed_data = json_loads(line)
        if isinstance(parsed_data, dict):
            if "hits" in parsed_data:
                return parsed_data["HITS"]
            return [parsed_data]
    except Exception:
        pass

    return []


x__process_stream_line__mutmut_mutants: ClassVar[MutantDict] = {
    "x__process_stream_line__mutmut_1": x__process_stream_line__mutmut_1,
    "x__process_stream_line__mutmut_2": x__process_stream_line__mutmut_2,
    "x__process_stream_line__mutmut_3": x__process_stream_line__mutmut_3,
    "x__process_stream_line__mutmut_4": x__process_stream_line__mutmut_4,
    "x__process_stream_line__mutmut_5": x__process_stream_line__mutmut_5,
    "x__process_stream_line__mutmut_6": x__process_stream_line__mutmut_6,
    "x__process_stream_line__mutmut_7": x__process_stream_line__mutmut_7,
    "x__process_stream_line__mutmut_8": x__process_stream_line__mutmut_8,
}


def _process_stream_line(*args, **kwargs):
    result = _mutmut_trampoline(
        x__process_stream_line__mutmut_orig, x__process_stream_line__mutmut_mutants, args, kwargs
    )
    return result


_process_stream_line.__signature__ = _mutmut_signature(x__process_stream_line__mutmut_orig)
x__process_stream_line__mutmut_orig.__name__ = "x__process_stream_line"


async def x_stream_search_http2_async__mutmut_orig(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_1(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is not None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_2(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = None

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_3(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = None
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_4(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(None, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_5(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, None)
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_6(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param("-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_7(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(
        start_time,
    )
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_8(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "XX-1hXX")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_9(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1H")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_10(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = None

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_11(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(None, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_12(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, None)

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_13(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param("now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_14(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(
        end_time,
    )

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_15(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "XXnowXX")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_16(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "NOW")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_17(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = None
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_18(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = None
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_19(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "XXis_ui_histogramXX": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_20(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "IS_UI_HISTOGRAM": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_21(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "XXfalseXX",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_22(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "FALSE",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_23(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "XXis_multi_stream_searchXX": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_24(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "IS_MULTI_STREAM_SEARCH": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_25(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "XXfalseXX",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_26(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "FALSE",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_27(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = None

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_28(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "XXsqlXX": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_29(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "SQL": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_30(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "XXstart_timeXX": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_31(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "START_TIME": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_32(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "XXend_timeXX": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_33(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "END_TIME": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_34(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=None, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_35(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method=None, params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_36(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=None, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_37(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=None):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_38(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_39(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_40(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_41(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(
            uri=uri,
            method="POST",
            params=params,
        ):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_42(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="XXPOSTXX", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_43(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="post", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_44(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = None
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_45(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split(None)
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_46(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode(None).strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_47(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("XXutf-8XX").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_48(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("UTF-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_49(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("XX\nXX")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_50(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(None):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


async def x_stream_search_http2_async__mutmut_51(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(None) from e


x_stream_search_http2_async__mutmut_mutants: ClassVar[MutantDict] = {
    "x_stream_search_http2_async__mutmut_1": x_stream_search_http2_async__mutmut_1,
    "x_stream_search_http2_async__mutmut_2": x_stream_search_http2_async__mutmut_2,
    "x_stream_search_http2_async__mutmut_3": x_stream_search_http2_async__mutmut_3,
    "x_stream_search_http2_async__mutmut_4": x_stream_search_http2_async__mutmut_4,
    "x_stream_search_http2_async__mutmut_5": x_stream_search_http2_async__mutmut_5,
    "x_stream_search_http2_async__mutmut_6": x_stream_search_http2_async__mutmut_6,
    "x_stream_search_http2_async__mutmut_7": x_stream_search_http2_async__mutmut_7,
    "x_stream_search_http2_async__mutmut_8": x_stream_search_http2_async__mutmut_8,
    "x_stream_search_http2_async__mutmut_9": x_stream_search_http2_async__mutmut_9,
    "x_stream_search_http2_async__mutmut_10": x_stream_search_http2_async__mutmut_10,
    "x_stream_search_http2_async__mutmut_11": x_stream_search_http2_async__mutmut_11,
    "x_stream_search_http2_async__mutmut_12": x_stream_search_http2_async__mutmut_12,
    "x_stream_search_http2_async__mutmut_13": x_stream_search_http2_async__mutmut_13,
    "x_stream_search_http2_async__mutmut_14": x_stream_search_http2_async__mutmut_14,
    "x_stream_search_http2_async__mutmut_15": x_stream_search_http2_async__mutmut_15,
    "x_stream_search_http2_async__mutmut_16": x_stream_search_http2_async__mutmut_16,
    "x_stream_search_http2_async__mutmut_17": x_stream_search_http2_async__mutmut_17,
    "x_stream_search_http2_async__mutmut_18": x_stream_search_http2_async__mutmut_18,
    "x_stream_search_http2_async__mutmut_19": x_stream_search_http2_async__mutmut_19,
    "x_stream_search_http2_async__mutmut_20": x_stream_search_http2_async__mutmut_20,
    "x_stream_search_http2_async__mutmut_21": x_stream_search_http2_async__mutmut_21,
    "x_stream_search_http2_async__mutmut_22": x_stream_search_http2_async__mutmut_22,
    "x_stream_search_http2_async__mutmut_23": x_stream_search_http2_async__mutmut_23,
    "x_stream_search_http2_async__mutmut_24": x_stream_search_http2_async__mutmut_24,
    "x_stream_search_http2_async__mutmut_25": x_stream_search_http2_async__mutmut_25,
    "x_stream_search_http2_async__mutmut_26": x_stream_search_http2_async__mutmut_26,
    "x_stream_search_http2_async__mutmut_27": x_stream_search_http2_async__mutmut_27,
    "x_stream_search_http2_async__mutmut_28": x_stream_search_http2_async__mutmut_28,
    "x_stream_search_http2_async__mutmut_29": x_stream_search_http2_async__mutmut_29,
    "x_stream_search_http2_async__mutmut_30": x_stream_search_http2_async__mutmut_30,
    "x_stream_search_http2_async__mutmut_31": x_stream_search_http2_async__mutmut_31,
    "x_stream_search_http2_async__mutmut_32": x_stream_search_http2_async__mutmut_32,
    "x_stream_search_http2_async__mutmut_33": x_stream_search_http2_async__mutmut_33,
    "x_stream_search_http2_async__mutmut_34": x_stream_search_http2_async__mutmut_34,
    "x_stream_search_http2_async__mutmut_35": x_stream_search_http2_async__mutmut_35,
    "x_stream_search_http2_async__mutmut_36": x_stream_search_http2_async__mutmut_36,
    "x_stream_search_http2_async__mutmut_37": x_stream_search_http2_async__mutmut_37,
    "x_stream_search_http2_async__mutmut_38": x_stream_search_http2_async__mutmut_38,
    "x_stream_search_http2_async__mutmut_39": x_stream_search_http2_async__mutmut_39,
    "x_stream_search_http2_async__mutmut_40": x_stream_search_http2_async__mutmut_40,
    "x_stream_search_http2_async__mutmut_41": x_stream_search_http2_async__mutmut_41,
    "x_stream_search_http2_async__mutmut_42": x_stream_search_http2_async__mutmut_42,
    "x_stream_search_http2_async__mutmut_43": x_stream_search_http2_async__mutmut_43,
    "x_stream_search_http2_async__mutmut_44": x_stream_search_http2_async__mutmut_44,
    "x_stream_search_http2_async__mutmut_45": x_stream_search_http2_async__mutmut_45,
    "x_stream_search_http2_async__mutmut_46": x_stream_search_http2_async__mutmut_46,
    "x_stream_search_http2_async__mutmut_47": x_stream_search_http2_async__mutmut_47,
    "x_stream_search_http2_async__mutmut_48": x_stream_search_http2_async__mutmut_48,
    "x_stream_search_http2_async__mutmut_49": x_stream_search_http2_async__mutmut_49,
    "x_stream_search_http2_async__mutmut_50": x_stream_search_http2_async__mutmut_50,
    "x_stream_search_http2_async__mutmut_51": x_stream_search_http2_async__mutmut_51,
}


def stream_search_http2_async(*args, **kwargs):
    result = _mutmut_trampoline(
        x_stream_search_http2_async__mutmut_orig, x_stream_search_http2_async__mutmut_mutants, args, kwargs
    )
    return result


stream_search_http2_async.__signature__ = _mutmut_signature(x_stream_search_http2_async__mutmut_orig)
x_stream_search_http2_async__mutmut_orig.__name__ = "x_stream_search_http2_async"


def x_stream_search_http2__mutmut_orig(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint (sync wrapper).

    This is a sync wrapper around the async streaming function for CLI use.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """

    async def _stream() -> list[dict[str, Any]]:
        results = []
        async for item in stream_search_http2_async(
            sql=sql, start_time=start_time, end_time=end_time, client=client
        ):
            results.append(item)
        return results

    results = run_async(_stream())
    yield from results


def x_stream_search_http2__mutmut_1(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint (sync wrapper).

    This is a sync wrapper around the async streaming function for CLI use.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """

    async def _stream() -> list[dict[str, Any]]:
        results = None
        async for item in stream_search_http2_async(
            sql=sql, start_time=start_time, end_time=end_time, client=client
        ):
            results.append(item)
        return results

    results = run_async(_stream())
    yield from results


def x_stream_search_http2__mutmut_2(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint (sync wrapper).

    This is a sync wrapper around the async streaming function for CLI use.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """

    async def _stream() -> list[dict[str, Any]]:
        results = []
        async for item in stream_search_http2_async(
            sql=None, start_time=start_time, end_time=end_time, client=client
        ):
            results.append(item)
        return results

    results = run_async(_stream())
    yield from results


def x_stream_search_http2__mutmut_3(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint (sync wrapper).

    This is a sync wrapper around the async streaming function for CLI use.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """

    async def _stream() -> list[dict[str, Any]]:
        results = []
        async for item in stream_search_http2_async(
            sql=sql, start_time=None, end_time=end_time, client=client
        ):
            results.append(item)
        return results

    results = run_async(_stream())
    yield from results


def x_stream_search_http2__mutmut_4(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint (sync wrapper).

    This is a sync wrapper around the async streaming function for CLI use.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """

    async def _stream() -> list[dict[str, Any]]:
        results = []
        async for item in stream_search_http2_async(
            sql=sql, start_time=start_time, end_time=None, client=client
        ):
            results.append(item)
        return results

    results = run_async(_stream())
    yield from results


def x_stream_search_http2__mutmut_5(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint (sync wrapper).

    This is a sync wrapper around the async streaming function for CLI use.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """

    async def _stream() -> list[dict[str, Any]]:
        results = []
        async for item in stream_search_http2_async(
            sql=sql, start_time=start_time, end_time=end_time, client=None
        ):
            results.append(item)
        return results

    results = run_async(_stream())
    yield from results


def x_stream_search_http2__mutmut_6(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint (sync wrapper).

    This is a sync wrapper around the async streaming function for CLI use.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """

    async def _stream() -> list[dict[str, Any]]:
        results = []
        async for item in stream_search_http2_async(start_time=start_time, end_time=end_time, client=client):
            results.append(item)
        return results

    results = run_async(_stream())
    yield from results


def x_stream_search_http2__mutmut_7(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint (sync wrapper).

    This is a sync wrapper around the async streaming function for CLI use.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """

    async def _stream() -> list[dict[str, Any]]:
        results = []
        async for item in stream_search_http2_async(sql=sql, end_time=end_time, client=client):
            results.append(item)
        return results

    results = run_async(_stream())
    yield from results


def x_stream_search_http2__mutmut_8(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint (sync wrapper).

    This is a sync wrapper around the async streaming function for CLI use.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """

    async def _stream() -> list[dict[str, Any]]:
        results = []
        async for item in stream_search_http2_async(sql=sql, start_time=start_time, client=client):
            results.append(item)
        return results

    results = run_async(_stream())
    yield from results


def x_stream_search_http2__mutmut_9(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint (sync wrapper).

    This is a sync wrapper around the async streaming function for CLI use.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """

    async def _stream() -> list[dict[str, Any]]:
        results = []
        async for item in stream_search_http2_async(
            sql=sql,
            start_time=start_time,
            end_time=end_time,
        ):
            results.append(item)
        return results

    results = run_async(_stream())
    yield from results


def x_stream_search_http2__mutmut_10(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint (sync wrapper).

    This is a sync wrapper around the async streaming function for CLI use.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """

    async def _stream() -> list[dict[str, Any]]:
        results = []
        async for item in stream_search_http2_async(
            sql=sql, start_time=start_time, end_time=end_time, client=client
        ):
            results.append(None)
        return results

    results = run_async(_stream())
    yield from results


def x_stream_search_http2__mutmut_11(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint (sync wrapper).

    This is a sync wrapper around the async streaming function for CLI use.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """

    async def _stream() -> list[dict[str, Any]]:
        results = []
        async for item in stream_search_http2_async(
            sql=sql, start_time=start_time, end_time=end_time, client=client
        ):
            results.append(item)
        return results

    results = None
    yield from results


def x_stream_search_http2__mutmut_12(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint (sync wrapper).

    This is a sync wrapper around the async streaming function for CLI use.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """

    async def _stream() -> list[dict[str, Any]]:
        results = []
        async for item in stream_search_http2_async(
            sql=sql, start_time=start_time, end_time=end_time, client=client
        ):
            results.append(item)
        return results

    results = run_async(None)
    yield from results


x_stream_search_http2__mutmut_mutants: ClassVar[MutantDict] = {
    "x_stream_search_http2__mutmut_1": x_stream_search_http2__mutmut_1,
    "x_stream_search_http2__mutmut_2": x_stream_search_http2__mutmut_2,
    "x_stream_search_http2__mutmut_3": x_stream_search_http2__mutmut_3,
    "x_stream_search_http2__mutmut_4": x_stream_search_http2__mutmut_4,
    "x_stream_search_http2__mutmut_5": x_stream_search_http2__mutmut_5,
    "x_stream_search_http2__mutmut_6": x_stream_search_http2__mutmut_6,
    "x_stream_search_http2__mutmut_7": x_stream_search_http2__mutmut_7,
    "x_stream_search_http2__mutmut_8": x_stream_search_http2__mutmut_8,
    "x_stream_search_http2__mutmut_9": x_stream_search_http2__mutmut_9,
    "x_stream_search_http2__mutmut_10": x_stream_search_http2__mutmut_10,
    "x_stream_search_http2__mutmut_11": x_stream_search_http2__mutmut_11,
    "x_stream_search_http2__mutmut_12": x_stream_search_http2__mutmut_12,
}


def stream_search_http2(*args, **kwargs):
    result = _mutmut_trampoline(
        x_stream_search_http2__mutmut_orig, x_stream_search_http2__mutmut_mutants, args, kwargs
    )
    return result


stream_search_http2.__signature__ = _mutmut_signature(x_stream_search_http2__mutmut_orig)
x_stream_search_http2__mutmut_orig.__name__ = "x_stream_search_http2"


def x__build_where_clause_from_filters__mutmut_orig(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_1(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_2(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return "XXXX"

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_3(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = None
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_4(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_5(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(None, key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_6(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", None):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_7(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_8(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(
            r"^[a-zA-Z0-9_]+$",
        ):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_9(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"XX^[a-zA-Z0-9_]+$XX", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_10(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-za-z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_11(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[A-ZA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_12(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(None)

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_13(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = None
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_14(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace(None, "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_15(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", None)
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_16(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_17(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace(
            "'",
        )
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_18(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("XX'XX", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_19(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "XX''XX")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_20(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(None)

    return f"WHERE {' AND '.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_21(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(None)}"


def x__build_where_clause_from_filters__mutmut_22(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {'XX AND XX'.join(conditions)}"


def x__build_where_clause_from_filters__mutmut_23(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' and '.join(conditions)}"


x__build_where_clause_from_filters__mutmut_mutants: ClassVar[MutantDict] = {
    "x__build_where_clause_from_filters__mutmut_1": x__build_where_clause_from_filters__mutmut_1,
    "x__build_where_clause_from_filters__mutmut_2": x__build_where_clause_from_filters__mutmut_2,
    "x__build_where_clause_from_filters__mutmut_3": x__build_where_clause_from_filters__mutmut_3,
    "x__build_where_clause_from_filters__mutmut_4": x__build_where_clause_from_filters__mutmut_4,
    "x__build_where_clause_from_filters__mutmut_5": x__build_where_clause_from_filters__mutmut_5,
    "x__build_where_clause_from_filters__mutmut_6": x__build_where_clause_from_filters__mutmut_6,
    "x__build_where_clause_from_filters__mutmut_7": x__build_where_clause_from_filters__mutmut_7,
    "x__build_where_clause_from_filters__mutmut_8": x__build_where_clause_from_filters__mutmut_8,
    "x__build_where_clause_from_filters__mutmut_9": x__build_where_clause_from_filters__mutmut_9,
    "x__build_where_clause_from_filters__mutmut_10": x__build_where_clause_from_filters__mutmut_10,
    "x__build_where_clause_from_filters__mutmut_11": x__build_where_clause_from_filters__mutmut_11,
    "x__build_where_clause_from_filters__mutmut_12": x__build_where_clause_from_filters__mutmut_12,
    "x__build_where_clause_from_filters__mutmut_13": x__build_where_clause_from_filters__mutmut_13,
    "x__build_where_clause_from_filters__mutmut_14": x__build_where_clause_from_filters__mutmut_14,
    "x__build_where_clause_from_filters__mutmut_15": x__build_where_clause_from_filters__mutmut_15,
    "x__build_where_clause_from_filters__mutmut_16": x__build_where_clause_from_filters__mutmut_16,
    "x__build_where_clause_from_filters__mutmut_17": x__build_where_clause_from_filters__mutmut_17,
    "x__build_where_clause_from_filters__mutmut_18": x__build_where_clause_from_filters__mutmut_18,
    "x__build_where_clause_from_filters__mutmut_19": x__build_where_clause_from_filters__mutmut_19,
    "x__build_where_clause_from_filters__mutmut_20": x__build_where_clause_from_filters__mutmut_20,
    "x__build_where_clause_from_filters__mutmut_21": x__build_where_clause_from_filters__mutmut_21,
    "x__build_where_clause_from_filters__mutmut_22": x__build_where_clause_from_filters__mutmut_22,
    "x__build_where_clause_from_filters__mutmut_23": x__build_where_clause_from_filters__mutmut_23,
}


def _build_where_clause_from_filters(*args, **kwargs):
    result = _mutmut_trampoline(
        x__build_where_clause_from_filters__mutmut_orig,
        x__build_where_clause_from_filters__mutmut_mutants,
        args,
        kwargs,
    )
    return result


_build_where_clause_from_filters.__signature__ = _mutmut_signature(
    x__build_where_clause_from_filters__mutmut_orig
)
x__build_where_clause_from_filters__mutmut_orig.__name__ = "x__build_where_clause_from_filters"


def x_tail_logs__mutmut_orig(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_1(
    stream: str = "XXdefaultXX",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_2(
    stream: str = "DEFAULT",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_3(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = False,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_4(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 11,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_5(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_6(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(None, stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_7(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", None):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_8(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_9(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(
        r"^[a-zA-Z0-9_]+$",
    ):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_10(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"XX^[a-zA-Z0-9_]+$XX", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_11(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-za-z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_12(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[A-ZA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_13(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            None, code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_14(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code=None, stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_15(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=None, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_16(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern=None
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_17(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$")

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_18(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError("Invalid stream name", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$")

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_19(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_20(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name",
            code="INVALID_STREAM_NAME",
            stream=stream,
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_21(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "XXInvalid stream nameXX",
            code="INVALID_STREAM_NAME",
            stream=stream,
            allowed_pattern="^[a-zA-Z0-9_]+$",
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_22(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_23(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "INVALID STREAM NAME", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_24(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name",
            code="XXINVALID_STREAM_NAMEXX",
            stream=stream,
            allowed_pattern="^[a-zA-Z0-9_]+$",
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_25(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="invalid_stream_name", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_26(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name",
            code="INVALID_STREAM_NAME",
            stream=stream,
            allowed_pattern="XX^[a-zA-Z0-9_]+$XX",
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_27(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-za-z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_28(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[A-ZA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_29(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 and lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_30(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) and lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_31(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_32(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines < 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_33(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 1 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_34(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines >= 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_35(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10001:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_36(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(None, code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000")

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_37(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError("Invalid lines parameter", code=None, lines=lines, expected_range="1-10000")

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_38(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=None, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_39(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range=None
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_40(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000")

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_41(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError("Invalid lines parameter", lines=lines, expected_range="1-10000")

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_42(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError("Invalid lines parameter", code="INVALID_LINES_PARAM", expected_range="1-10000")

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_43(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter",
            code="INVALID_LINES_PARAM",
            lines=lines,
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_44(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "XXInvalid lines parameterXX", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_45(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_46(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "INVALID LINES PARAMETER", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_47(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="XXINVALID_LINES_PARAMXX", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_48(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="invalid_lines_param", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_49(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="XX1-10000XX"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_50(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = None
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_51(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(None)
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_52(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters and {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_53(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = None

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_54(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is not None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_55(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = None

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_56(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = None

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_57(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(None)

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_58(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=None, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_59(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time=None))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_60(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_61(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(
        client.search(
            sql=sql,
        )
    )

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_62(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="XX-1hXX"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_63(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1H"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_64(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(None)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_65(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = None
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_66(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(None)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_67(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get(None, 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_68(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", None) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_69(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get(0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_70(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(
                hit.get(
                    "_timestamp",
                )
                for hit in response.hits
            )
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_71(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("XX_timestampXX", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_72(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_TIMESTAMP", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_73(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 1) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_74(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = None

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_75(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time(None)

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_76(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("XX-1sXX")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_77(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1S")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_78(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = None

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_79(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=None,
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_80(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=None,
            client=client,
        )


def x_tail_logs__mutmut_81(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=None,
        )


def x_tail_logs__mutmut_82(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            start_time=last_timestamp + 1,
            client=client,
        )


def x_tail_logs__mutmut_83(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            client=client,
        )


def x_tail_logs__mutmut_84(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
        )


def x_tail_logs__mutmut_85(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp - 1,
            client=client,
        )


def x_tail_logs__mutmut_86(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 2,
            client=client,
        )


x_tail_logs__mutmut_mutants: ClassVar[MutantDict] = {
    "x_tail_logs__mutmut_1": x_tail_logs__mutmut_1,
    "x_tail_logs__mutmut_2": x_tail_logs__mutmut_2,
    "x_tail_logs__mutmut_3": x_tail_logs__mutmut_3,
    "x_tail_logs__mutmut_4": x_tail_logs__mutmut_4,
    "x_tail_logs__mutmut_5": x_tail_logs__mutmut_5,
    "x_tail_logs__mutmut_6": x_tail_logs__mutmut_6,
    "x_tail_logs__mutmut_7": x_tail_logs__mutmut_7,
    "x_tail_logs__mutmut_8": x_tail_logs__mutmut_8,
    "x_tail_logs__mutmut_9": x_tail_logs__mutmut_9,
    "x_tail_logs__mutmut_10": x_tail_logs__mutmut_10,
    "x_tail_logs__mutmut_11": x_tail_logs__mutmut_11,
    "x_tail_logs__mutmut_12": x_tail_logs__mutmut_12,
    "x_tail_logs__mutmut_13": x_tail_logs__mutmut_13,
    "x_tail_logs__mutmut_14": x_tail_logs__mutmut_14,
    "x_tail_logs__mutmut_15": x_tail_logs__mutmut_15,
    "x_tail_logs__mutmut_16": x_tail_logs__mutmut_16,
    "x_tail_logs__mutmut_17": x_tail_logs__mutmut_17,
    "x_tail_logs__mutmut_18": x_tail_logs__mutmut_18,
    "x_tail_logs__mutmut_19": x_tail_logs__mutmut_19,
    "x_tail_logs__mutmut_20": x_tail_logs__mutmut_20,
    "x_tail_logs__mutmut_21": x_tail_logs__mutmut_21,
    "x_tail_logs__mutmut_22": x_tail_logs__mutmut_22,
    "x_tail_logs__mutmut_23": x_tail_logs__mutmut_23,
    "x_tail_logs__mutmut_24": x_tail_logs__mutmut_24,
    "x_tail_logs__mutmut_25": x_tail_logs__mutmut_25,
    "x_tail_logs__mutmut_26": x_tail_logs__mutmut_26,
    "x_tail_logs__mutmut_27": x_tail_logs__mutmut_27,
    "x_tail_logs__mutmut_28": x_tail_logs__mutmut_28,
    "x_tail_logs__mutmut_29": x_tail_logs__mutmut_29,
    "x_tail_logs__mutmut_30": x_tail_logs__mutmut_30,
    "x_tail_logs__mutmut_31": x_tail_logs__mutmut_31,
    "x_tail_logs__mutmut_32": x_tail_logs__mutmut_32,
    "x_tail_logs__mutmut_33": x_tail_logs__mutmut_33,
    "x_tail_logs__mutmut_34": x_tail_logs__mutmut_34,
    "x_tail_logs__mutmut_35": x_tail_logs__mutmut_35,
    "x_tail_logs__mutmut_36": x_tail_logs__mutmut_36,
    "x_tail_logs__mutmut_37": x_tail_logs__mutmut_37,
    "x_tail_logs__mutmut_38": x_tail_logs__mutmut_38,
    "x_tail_logs__mutmut_39": x_tail_logs__mutmut_39,
    "x_tail_logs__mutmut_40": x_tail_logs__mutmut_40,
    "x_tail_logs__mutmut_41": x_tail_logs__mutmut_41,
    "x_tail_logs__mutmut_42": x_tail_logs__mutmut_42,
    "x_tail_logs__mutmut_43": x_tail_logs__mutmut_43,
    "x_tail_logs__mutmut_44": x_tail_logs__mutmut_44,
    "x_tail_logs__mutmut_45": x_tail_logs__mutmut_45,
    "x_tail_logs__mutmut_46": x_tail_logs__mutmut_46,
    "x_tail_logs__mutmut_47": x_tail_logs__mutmut_47,
    "x_tail_logs__mutmut_48": x_tail_logs__mutmut_48,
    "x_tail_logs__mutmut_49": x_tail_logs__mutmut_49,
    "x_tail_logs__mutmut_50": x_tail_logs__mutmut_50,
    "x_tail_logs__mutmut_51": x_tail_logs__mutmut_51,
    "x_tail_logs__mutmut_52": x_tail_logs__mutmut_52,
    "x_tail_logs__mutmut_53": x_tail_logs__mutmut_53,
    "x_tail_logs__mutmut_54": x_tail_logs__mutmut_54,
    "x_tail_logs__mutmut_55": x_tail_logs__mutmut_55,
    "x_tail_logs__mutmut_56": x_tail_logs__mutmut_56,
    "x_tail_logs__mutmut_57": x_tail_logs__mutmut_57,
    "x_tail_logs__mutmut_58": x_tail_logs__mutmut_58,
    "x_tail_logs__mutmut_59": x_tail_logs__mutmut_59,
    "x_tail_logs__mutmut_60": x_tail_logs__mutmut_60,
    "x_tail_logs__mutmut_61": x_tail_logs__mutmut_61,
    "x_tail_logs__mutmut_62": x_tail_logs__mutmut_62,
    "x_tail_logs__mutmut_63": x_tail_logs__mutmut_63,
    "x_tail_logs__mutmut_64": x_tail_logs__mutmut_64,
    "x_tail_logs__mutmut_65": x_tail_logs__mutmut_65,
    "x_tail_logs__mutmut_66": x_tail_logs__mutmut_66,
    "x_tail_logs__mutmut_67": x_tail_logs__mutmut_67,
    "x_tail_logs__mutmut_68": x_tail_logs__mutmut_68,
    "x_tail_logs__mutmut_69": x_tail_logs__mutmut_69,
    "x_tail_logs__mutmut_70": x_tail_logs__mutmut_70,
    "x_tail_logs__mutmut_71": x_tail_logs__mutmut_71,
    "x_tail_logs__mutmut_72": x_tail_logs__mutmut_72,
    "x_tail_logs__mutmut_73": x_tail_logs__mutmut_73,
    "x_tail_logs__mutmut_74": x_tail_logs__mutmut_74,
    "x_tail_logs__mutmut_75": x_tail_logs__mutmut_75,
    "x_tail_logs__mutmut_76": x_tail_logs__mutmut_76,
    "x_tail_logs__mutmut_77": x_tail_logs__mutmut_77,
    "x_tail_logs__mutmut_78": x_tail_logs__mutmut_78,
    "x_tail_logs__mutmut_79": x_tail_logs__mutmut_79,
    "x_tail_logs__mutmut_80": x_tail_logs__mutmut_80,
    "x_tail_logs__mutmut_81": x_tail_logs__mutmut_81,
    "x_tail_logs__mutmut_82": x_tail_logs__mutmut_82,
    "x_tail_logs__mutmut_83": x_tail_logs__mutmut_83,
    "x_tail_logs__mutmut_84": x_tail_logs__mutmut_84,
    "x_tail_logs__mutmut_85": x_tail_logs__mutmut_85,
    "x_tail_logs__mutmut_86": x_tail_logs__mutmut_86,
}


def tail_logs(*args, **kwargs):
    result = _mutmut_trampoline(x_tail_logs__mutmut_orig, x_tail_logs__mutmut_mutants, args, kwargs)
    return result


tail_logs.__signature__ = _mutmut_signature(x_tail_logs__mutmut_orig)
x_tail_logs__mutmut_orig.__name__ = "x_tail_logs"


# <3 🧱🤝🔌🪄
