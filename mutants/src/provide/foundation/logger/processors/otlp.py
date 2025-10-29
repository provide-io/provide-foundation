# provide/foundation/logger/processors/otlp.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""OTLP processor for sending logs to OpenTelemetry endpoints.

This processor uses the generic OTLPLogClient to send logs to any OTLP-compatible backend.
"""

from __future__ import annotations

import contextlib
from typing import Any

from provide.foundation.logger.otlp.client import OTLPLogClient
from provide.foundation.logger.otlp.severity import map_level_to_severity

# Global logger provider instance
_OTLP_LOGGER_PROVIDER: Any | None = None
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


def x__convert_timestamp_to_nanos__mutmut_orig(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_1(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_2(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = None
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_3(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(None)
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_4(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace(None, "+00:00"))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_5(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("Z", None))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_6(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("+00:00"))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_7(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(
            timestamp.replace(
                "Z",
            )
        )
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_8(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("XXZXX", "+00:00"))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_9(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("z", "+00:00"))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_10(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("Z", "XX+00:00XX"))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_11(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return int(None)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_12(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return int(dt.timestamp() / 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_13(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1000000001)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_14(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(None) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_15(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp / 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_16(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1000000001) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_17(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp <= 10_000_000_000 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_18(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10000000001 else int(timestamp)

    return None


def x__convert_timestamp_to_nanos__mutmut_19(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(None)

    return None


x__convert_timestamp_to_nanos__mutmut_mutants: ClassVar[MutantDict] = {
    "x__convert_timestamp_to_nanos__mutmut_1": x__convert_timestamp_to_nanos__mutmut_1,
    "x__convert_timestamp_to_nanos__mutmut_2": x__convert_timestamp_to_nanos__mutmut_2,
    "x__convert_timestamp_to_nanos__mutmut_3": x__convert_timestamp_to_nanos__mutmut_3,
    "x__convert_timestamp_to_nanos__mutmut_4": x__convert_timestamp_to_nanos__mutmut_4,
    "x__convert_timestamp_to_nanos__mutmut_5": x__convert_timestamp_to_nanos__mutmut_5,
    "x__convert_timestamp_to_nanos__mutmut_6": x__convert_timestamp_to_nanos__mutmut_6,
    "x__convert_timestamp_to_nanos__mutmut_7": x__convert_timestamp_to_nanos__mutmut_7,
    "x__convert_timestamp_to_nanos__mutmut_8": x__convert_timestamp_to_nanos__mutmut_8,
    "x__convert_timestamp_to_nanos__mutmut_9": x__convert_timestamp_to_nanos__mutmut_9,
    "x__convert_timestamp_to_nanos__mutmut_10": x__convert_timestamp_to_nanos__mutmut_10,
    "x__convert_timestamp_to_nanos__mutmut_11": x__convert_timestamp_to_nanos__mutmut_11,
    "x__convert_timestamp_to_nanos__mutmut_12": x__convert_timestamp_to_nanos__mutmut_12,
    "x__convert_timestamp_to_nanos__mutmut_13": x__convert_timestamp_to_nanos__mutmut_13,
    "x__convert_timestamp_to_nanos__mutmut_14": x__convert_timestamp_to_nanos__mutmut_14,
    "x__convert_timestamp_to_nanos__mutmut_15": x__convert_timestamp_to_nanos__mutmut_15,
    "x__convert_timestamp_to_nanos__mutmut_16": x__convert_timestamp_to_nanos__mutmut_16,
    "x__convert_timestamp_to_nanos__mutmut_17": x__convert_timestamp_to_nanos__mutmut_17,
    "x__convert_timestamp_to_nanos__mutmut_18": x__convert_timestamp_to_nanos__mutmut_18,
    "x__convert_timestamp_to_nanos__mutmut_19": x__convert_timestamp_to_nanos__mutmut_19,
}


def _convert_timestamp_to_nanos(*args, **kwargs):
    result = _mutmut_trampoline(
        x__convert_timestamp_to_nanos__mutmut_orig, x__convert_timestamp_to_nanos__mutmut_mutants, args, kwargs
    )
    return result


_convert_timestamp_to_nanos.__signature__ = _mutmut_signature(x__convert_timestamp_to_nanos__mutmut_orig)
x__convert_timestamp_to_nanos__mutmut_orig.__name__ = "x__convert_timestamp_to_nanos"


def x_create_otlp_processor__mutmut_orig(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_1(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_2(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is not None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_3(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = None
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_4(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(None)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_5(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_6(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = None
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_7(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_8(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = None

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_9(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(None)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_10(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop(None, False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_11(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", None):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_12(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop(False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_13(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop(
                "_skip_otlp",
            ):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_14(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("XX_skip_otlpXX", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_15(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_SKIP_OTLP", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_16(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", True):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_17(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = None
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_18(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(None)
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_19(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get(None, ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_20(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", None))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_21(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get(""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_22(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(
                    event_dict.get(
                        "event",
                    )
                )
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_23(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("XXeventXX", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_24(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("EVENT", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_25(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", "XXXX"))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_26(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = None

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_27(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).upper()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_28(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(None).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_29(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get(None, "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_30(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", None)).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_31(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_32(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(
                    event_dict.get(
                        "level",
                    )
                ).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_33(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("XXlevelXX", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_34(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("LEVEL", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_35(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "XXinfoXX")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_36(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "INFO")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_37(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = None

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_38(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(None) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_39(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_40(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("XXeventXX", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_41(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("EVENT", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_42(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "XXtimestampXX")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_43(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "TIMESTAMP")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_44(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = None
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_45(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["XXmessageXX"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_46(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["MESSAGE"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_47(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = None

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_48(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["XXlevelXX"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_49(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["LEVEL"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_50(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.lower()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_51(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = None

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_52(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(None)

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_53(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get(None))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_54(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("XXtimestampXX"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_55(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("TIMESTAMP"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_56(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = None
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_57(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(None)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_58(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = None

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_59(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.lower()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_60(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = None
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_61(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=None,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_62(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=None,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_63(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=None,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_64(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=None,
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_65(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=None,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_66(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=None,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_67(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=None,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_68(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_69(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_70(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_71(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_72(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_73(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_74(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_75(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_76(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_77(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(None),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def x_create_otlp_processor__mutmut_78(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord
                from opentelemetry.sdk._logs._internal import SeverityNumber

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    resource=_OTLP_LOGGER_PROVIDER.resource,
                    attributes=attributes,
                    limits=None,
                )
                otlp_logger.emit(None)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


x_create_otlp_processor__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_otlp_processor__mutmut_1": x_create_otlp_processor__mutmut_1,
    "x_create_otlp_processor__mutmut_2": x_create_otlp_processor__mutmut_2,
    "x_create_otlp_processor__mutmut_3": x_create_otlp_processor__mutmut_3,
    "x_create_otlp_processor__mutmut_4": x_create_otlp_processor__mutmut_4,
    "x_create_otlp_processor__mutmut_5": x_create_otlp_processor__mutmut_5,
    "x_create_otlp_processor__mutmut_6": x_create_otlp_processor__mutmut_6,
    "x_create_otlp_processor__mutmut_7": x_create_otlp_processor__mutmut_7,
    "x_create_otlp_processor__mutmut_8": x_create_otlp_processor__mutmut_8,
    "x_create_otlp_processor__mutmut_9": x_create_otlp_processor__mutmut_9,
    "x_create_otlp_processor__mutmut_10": x_create_otlp_processor__mutmut_10,
    "x_create_otlp_processor__mutmut_11": x_create_otlp_processor__mutmut_11,
    "x_create_otlp_processor__mutmut_12": x_create_otlp_processor__mutmut_12,
    "x_create_otlp_processor__mutmut_13": x_create_otlp_processor__mutmut_13,
    "x_create_otlp_processor__mutmut_14": x_create_otlp_processor__mutmut_14,
    "x_create_otlp_processor__mutmut_15": x_create_otlp_processor__mutmut_15,
    "x_create_otlp_processor__mutmut_16": x_create_otlp_processor__mutmut_16,
    "x_create_otlp_processor__mutmut_17": x_create_otlp_processor__mutmut_17,
    "x_create_otlp_processor__mutmut_18": x_create_otlp_processor__mutmut_18,
    "x_create_otlp_processor__mutmut_19": x_create_otlp_processor__mutmut_19,
    "x_create_otlp_processor__mutmut_20": x_create_otlp_processor__mutmut_20,
    "x_create_otlp_processor__mutmut_21": x_create_otlp_processor__mutmut_21,
    "x_create_otlp_processor__mutmut_22": x_create_otlp_processor__mutmut_22,
    "x_create_otlp_processor__mutmut_23": x_create_otlp_processor__mutmut_23,
    "x_create_otlp_processor__mutmut_24": x_create_otlp_processor__mutmut_24,
    "x_create_otlp_processor__mutmut_25": x_create_otlp_processor__mutmut_25,
    "x_create_otlp_processor__mutmut_26": x_create_otlp_processor__mutmut_26,
    "x_create_otlp_processor__mutmut_27": x_create_otlp_processor__mutmut_27,
    "x_create_otlp_processor__mutmut_28": x_create_otlp_processor__mutmut_28,
    "x_create_otlp_processor__mutmut_29": x_create_otlp_processor__mutmut_29,
    "x_create_otlp_processor__mutmut_30": x_create_otlp_processor__mutmut_30,
    "x_create_otlp_processor__mutmut_31": x_create_otlp_processor__mutmut_31,
    "x_create_otlp_processor__mutmut_32": x_create_otlp_processor__mutmut_32,
    "x_create_otlp_processor__mutmut_33": x_create_otlp_processor__mutmut_33,
    "x_create_otlp_processor__mutmut_34": x_create_otlp_processor__mutmut_34,
    "x_create_otlp_processor__mutmut_35": x_create_otlp_processor__mutmut_35,
    "x_create_otlp_processor__mutmut_36": x_create_otlp_processor__mutmut_36,
    "x_create_otlp_processor__mutmut_37": x_create_otlp_processor__mutmut_37,
    "x_create_otlp_processor__mutmut_38": x_create_otlp_processor__mutmut_38,
    "x_create_otlp_processor__mutmut_39": x_create_otlp_processor__mutmut_39,
    "x_create_otlp_processor__mutmut_40": x_create_otlp_processor__mutmut_40,
    "x_create_otlp_processor__mutmut_41": x_create_otlp_processor__mutmut_41,
    "x_create_otlp_processor__mutmut_42": x_create_otlp_processor__mutmut_42,
    "x_create_otlp_processor__mutmut_43": x_create_otlp_processor__mutmut_43,
    "x_create_otlp_processor__mutmut_44": x_create_otlp_processor__mutmut_44,
    "x_create_otlp_processor__mutmut_45": x_create_otlp_processor__mutmut_45,
    "x_create_otlp_processor__mutmut_46": x_create_otlp_processor__mutmut_46,
    "x_create_otlp_processor__mutmut_47": x_create_otlp_processor__mutmut_47,
    "x_create_otlp_processor__mutmut_48": x_create_otlp_processor__mutmut_48,
    "x_create_otlp_processor__mutmut_49": x_create_otlp_processor__mutmut_49,
    "x_create_otlp_processor__mutmut_50": x_create_otlp_processor__mutmut_50,
    "x_create_otlp_processor__mutmut_51": x_create_otlp_processor__mutmut_51,
    "x_create_otlp_processor__mutmut_52": x_create_otlp_processor__mutmut_52,
    "x_create_otlp_processor__mutmut_53": x_create_otlp_processor__mutmut_53,
    "x_create_otlp_processor__mutmut_54": x_create_otlp_processor__mutmut_54,
    "x_create_otlp_processor__mutmut_55": x_create_otlp_processor__mutmut_55,
    "x_create_otlp_processor__mutmut_56": x_create_otlp_processor__mutmut_56,
    "x_create_otlp_processor__mutmut_57": x_create_otlp_processor__mutmut_57,
    "x_create_otlp_processor__mutmut_58": x_create_otlp_processor__mutmut_58,
    "x_create_otlp_processor__mutmut_59": x_create_otlp_processor__mutmut_59,
    "x_create_otlp_processor__mutmut_60": x_create_otlp_processor__mutmut_60,
    "x_create_otlp_processor__mutmut_61": x_create_otlp_processor__mutmut_61,
    "x_create_otlp_processor__mutmut_62": x_create_otlp_processor__mutmut_62,
    "x_create_otlp_processor__mutmut_63": x_create_otlp_processor__mutmut_63,
    "x_create_otlp_processor__mutmut_64": x_create_otlp_processor__mutmut_64,
    "x_create_otlp_processor__mutmut_65": x_create_otlp_processor__mutmut_65,
    "x_create_otlp_processor__mutmut_66": x_create_otlp_processor__mutmut_66,
    "x_create_otlp_processor__mutmut_67": x_create_otlp_processor__mutmut_67,
    "x_create_otlp_processor__mutmut_68": x_create_otlp_processor__mutmut_68,
    "x_create_otlp_processor__mutmut_69": x_create_otlp_processor__mutmut_69,
    "x_create_otlp_processor__mutmut_70": x_create_otlp_processor__mutmut_70,
    "x_create_otlp_processor__mutmut_71": x_create_otlp_processor__mutmut_71,
    "x_create_otlp_processor__mutmut_72": x_create_otlp_processor__mutmut_72,
    "x_create_otlp_processor__mutmut_73": x_create_otlp_processor__mutmut_73,
    "x_create_otlp_processor__mutmut_74": x_create_otlp_processor__mutmut_74,
    "x_create_otlp_processor__mutmut_75": x_create_otlp_processor__mutmut_75,
    "x_create_otlp_processor__mutmut_76": x_create_otlp_processor__mutmut_76,
    "x_create_otlp_processor__mutmut_77": x_create_otlp_processor__mutmut_77,
    "x_create_otlp_processor__mutmut_78": x_create_otlp_processor__mutmut_78,
}


def create_otlp_processor(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_otlp_processor__mutmut_orig, x_create_otlp_processor__mutmut_mutants, args, kwargs
    )
    return result


create_otlp_processor.__signature__ = _mutmut_signature(x_create_otlp_processor__mutmut_orig)
x_create_otlp_processor__mutmut_orig.__name__ = "x_create_otlp_processor"


def x_flush_otlp_logs__mutmut_orig() -> None:
    """Flush any pending OTLP logs.

    Examples:
        >>> flush_otlp_logs()
        >>> # Ensures all pending logs are sent
    """
    global _OTLP_LOGGER_PROVIDER
    if _OTLP_LOGGER_PROVIDER is not None:
        with contextlib.suppress(Exception):
            _OTLP_LOGGER_PROVIDER.force_flush(timeout_millis=5000)


def x_flush_otlp_logs__mutmut_1() -> None:
    """Flush any pending OTLP logs.

    Examples:
        >>> flush_otlp_logs()
        >>> # Ensures all pending logs are sent
    """
    global _OTLP_LOGGER_PROVIDER
    if _OTLP_LOGGER_PROVIDER is None:
        with contextlib.suppress(Exception):
            _OTLP_LOGGER_PROVIDER.force_flush(timeout_millis=5000)


def x_flush_otlp_logs__mutmut_2() -> None:
    """Flush any pending OTLP logs.

    Examples:
        >>> flush_otlp_logs()
        >>> # Ensures all pending logs are sent
    """
    global _OTLP_LOGGER_PROVIDER
    if _OTLP_LOGGER_PROVIDER is not None:
        with contextlib.suppress(None):
            _OTLP_LOGGER_PROVIDER.force_flush(timeout_millis=5000)


def x_flush_otlp_logs__mutmut_3() -> None:
    """Flush any pending OTLP logs.

    Examples:
        >>> flush_otlp_logs()
        >>> # Ensures all pending logs are sent
    """
    global _OTLP_LOGGER_PROVIDER
    if _OTLP_LOGGER_PROVIDER is not None:
        with contextlib.suppress(Exception):
            _OTLP_LOGGER_PROVIDER.force_flush(timeout_millis=None)


def x_flush_otlp_logs__mutmut_4() -> None:
    """Flush any pending OTLP logs.

    Examples:
        >>> flush_otlp_logs()
        >>> # Ensures all pending logs are sent
    """
    global _OTLP_LOGGER_PROVIDER
    if _OTLP_LOGGER_PROVIDER is not None:
        with contextlib.suppress(Exception):
            _OTLP_LOGGER_PROVIDER.force_flush(timeout_millis=5001)


x_flush_otlp_logs__mutmut_mutants: ClassVar[MutantDict] = {
    "x_flush_otlp_logs__mutmut_1": x_flush_otlp_logs__mutmut_1,
    "x_flush_otlp_logs__mutmut_2": x_flush_otlp_logs__mutmut_2,
    "x_flush_otlp_logs__mutmut_3": x_flush_otlp_logs__mutmut_3,
    "x_flush_otlp_logs__mutmut_4": x_flush_otlp_logs__mutmut_4,
}


def flush_otlp_logs(*args, **kwargs):
    result = _mutmut_trampoline(
        x_flush_otlp_logs__mutmut_orig, x_flush_otlp_logs__mutmut_mutants, args, kwargs
    )
    return result


flush_otlp_logs.__signature__ = _mutmut_signature(x_flush_otlp_logs__mutmut_orig)
x_flush_otlp_logs__mutmut_orig.__name__ = "x_flush_otlp_logs"


def x_reset_otlp_provider__mutmut_orig() -> None:
    """Reset the global OTLP logger provider.

    This should be called when Foundation re-initializes to ensure
    a new LoggerProvider is created with updated configuration.
    The old provider is flushed before being reset to ensure no logs are lost.

    This is particularly important when service_name changes, as the
    OpenTelemetry Resource with service_name is immutable and baked into
    the LoggerProvider at creation time.

    Examples:
        >>> reset_otlp_provider()
        >>> # Forces recreation on next use
    """
    global _OTLP_LOGGER_PROVIDER
    if _OTLP_LOGGER_PROVIDER is not None:
        # Flush any pending logs before resetting
        flush_otlp_logs()
        _OTLP_LOGGER_PROVIDER = None


def x_reset_otlp_provider__mutmut_1() -> None:
    """Reset the global OTLP logger provider.

    This should be called when Foundation re-initializes to ensure
    a new LoggerProvider is created with updated configuration.
    The old provider is flushed before being reset to ensure no logs are lost.

    This is particularly important when service_name changes, as the
    OpenTelemetry Resource with service_name is immutable and baked into
    the LoggerProvider at creation time.

    Examples:
        >>> reset_otlp_provider()
        >>> # Forces recreation on next use
    """
    global _OTLP_LOGGER_PROVIDER
    if _OTLP_LOGGER_PROVIDER is None:
        # Flush any pending logs before resetting
        flush_otlp_logs()
        _OTLP_LOGGER_PROVIDER = None


def x_reset_otlp_provider__mutmut_2() -> None:
    """Reset the global OTLP logger provider.

    This should be called when Foundation re-initializes to ensure
    a new LoggerProvider is created with updated configuration.
    The old provider is flushed before being reset to ensure no logs are lost.

    This is particularly important when service_name changes, as the
    OpenTelemetry Resource with service_name is immutable and baked into
    the LoggerProvider at creation time.

    Examples:
        >>> reset_otlp_provider()
        >>> # Forces recreation on next use
    """
    global _OTLP_LOGGER_PROVIDER
    if _OTLP_LOGGER_PROVIDER is not None:
        # Flush any pending logs before resetting
        flush_otlp_logs()
        _OTLP_LOGGER_PROVIDER = ""


x_reset_otlp_provider__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_otlp_provider__mutmut_1": x_reset_otlp_provider__mutmut_1,
    "x_reset_otlp_provider__mutmut_2": x_reset_otlp_provider__mutmut_2,
}


def reset_otlp_provider(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_otlp_provider__mutmut_orig, x_reset_otlp_provider__mutmut_mutants, args, kwargs
    )
    return result


reset_otlp_provider.__signature__ = _mutmut_signature(x_reset_otlp_provider__mutmut_orig)
x_reset_otlp_provider__mutmut_orig.__name__ = "x_reset_otlp_provider"


__all__ = [
    "create_otlp_processor",
    "flush_otlp_logs",
    "reset_otlp_provider",
]


# <3 🧱🤝📝🪄
