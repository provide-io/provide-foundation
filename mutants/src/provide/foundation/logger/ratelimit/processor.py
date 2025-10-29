# provide/foundation/logger/ratelimit/processor.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# processor.py
#
import time
from typing import Any

import structlog

from provide.foundation.logger.ratelimit.limiters import GlobalRateLimiter

"""Structlog processor for rate limiting log messages."""
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


class RateLimiterProcessor:
    """Structlog processor that applies rate limiting to log messages.
    Can be configured with global and per-logger rate limits.
    """

    def xǁRateLimiterProcessorǁ__init____mutmut_orig(
        self,
        emit_warning_on_limit: bool = True,
        warning_interval_seconds: float = 60.0,
        summary_interval_seconds: float = 5.0,
    ) -> None:
        """Initialize the rate limiter processor.

        Args:
            emit_warning_on_limit: Whether to emit a warning when rate limited
            warning_interval_seconds: Minimum seconds between rate limit warnings
            summary_interval_seconds: Interval for rate limit summary reports

        """
        self.rate_limiter = GlobalRateLimiter()
        self.emit_warning_on_limit = emit_warning_on_limit
        self.warning_interval_seconds = warning_interval_seconds

        # Track last warning time per logger
        self.last_warning_times: dict[str, float] = {}

        # Track suppressed message counts
        self.suppressed_counts: dict[str, int] = {}
        self.last_summary_time = time.monotonic()
        self.summary_interval = summary_interval_seconds  # Emit summary periodically

    def xǁRateLimiterProcessorǁ__init____mutmut_1(
        self,
        emit_warning_on_limit: bool = False,
        warning_interval_seconds: float = 60.0,
        summary_interval_seconds: float = 5.0,
    ) -> None:
        """Initialize the rate limiter processor.

        Args:
            emit_warning_on_limit: Whether to emit a warning when rate limited
            warning_interval_seconds: Minimum seconds between rate limit warnings
            summary_interval_seconds: Interval for rate limit summary reports

        """
        self.rate_limiter = GlobalRateLimiter()
        self.emit_warning_on_limit = emit_warning_on_limit
        self.warning_interval_seconds = warning_interval_seconds

        # Track last warning time per logger
        self.last_warning_times: dict[str, float] = {}

        # Track suppressed message counts
        self.suppressed_counts: dict[str, int] = {}
        self.last_summary_time = time.monotonic()
        self.summary_interval = summary_interval_seconds  # Emit summary periodically

    def xǁRateLimiterProcessorǁ__init____mutmut_2(
        self,
        emit_warning_on_limit: bool = True,
        warning_interval_seconds: float = 61.0,
        summary_interval_seconds: float = 5.0,
    ) -> None:
        """Initialize the rate limiter processor.

        Args:
            emit_warning_on_limit: Whether to emit a warning when rate limited
            warning_interval_seconds: Minimum seconds between rate limit warnings
            summary_interval_seconds: Interval for rate limit summary reports

        """
        self.rate_limiter = GlobalRateLimiter()
        self.emit_warning_on_limit = emit_warning_on_limit
        self.warning_interval_seconds = warning_interval_seconds

        # Track last warning time per logger
        self.last_warning_times: dict[str, float] = {}

        # Track suppressed message counts
        self.suppressed_counts: dict[str, int] = {}
        self.last_summary_time = time.monotonic()
        self.summary_interval = summary_interval_seconds  # Emit summary periodically

    def xǁRateLimiterProcessorǁ__init____mutmut_3(
        self,
        emit_warning_on_limit: bool = True,
        warning_interval_seconds: float = 60.0,
        summary_interval_seconds: float = 6.0,
    ) -> None:
        """Initialize the rate limiter processor.

        Args:
            emit_warning_on_limit: Whether to emit a warning when rate limited
            warning_interval_seconds: Minimum seconds between rate limit warnings
            summary_interval_seconds: Interval for rate limit summary reports

        """
        self.rate_limiter = GlobalRateLimiter()
        self.emit_warning_on_limit = emit_warning_on_limit
        self.warning_interval_seconds = warning_interval_seconds

        # Track last warning time per logger
        self.last_warning_times: dict[str, float] = {}

        # Track suppressed message counts
        self.suppressed_counts: dict[str, int] = {}
        self.last_summary_time = time.monotonic()
        self.summary_interval = summary_interval_seconds  # Emit summary periodically

    def xǁRateLimiterProcessorǁ__init____mutmut_4(
        self,
        emit_warning_on_limit: bool = True,
        warning_interval_seconds: float = 60.0,
        summary_interval_seconds: float = 5.0,
    ) -> None:
        """Initialize the rate limiter processor.

        Args:
            emit_warning_on_limit: Whether to emit a warning when rate limited
            warning_interval_seconds: Minimum seconds between rate limit warnings
            summary_interval_seconds: Interval for rate limit summary reports

        """
        self.rate_limiter = None
        self.emit_warning_on_limit = emit_warning_on_limit
        self.warning_interval_seconds = warning_interval_seconds

        # Track last warning time per logger
        self.last_warning_times: dict[str, float] = {}

        # Track suppressed message counts
        self.suppressed_counts: dict[str, int] = {}
        self.last_summary_time = time.monotonic()
        self.summary_interval = summary_interval_seconds  # Emit summary periodically

    def xǁRateLimiterProcessorǁ__init____mutmut_5(
        self,
        emit_warning_on_limit: bool = True,
        warning_interval_seconds: float = 60.0,
        summary_interval_seconds: float = 5.0,
    ) -> None:
        """Initialize the rate limiter processor.

        Args:
            emit_warning_on_limit: Whether to emit a warning when rate limited
            warning_interval_seconds: Minimum seconds between rate limit warnings
            summary_interval_seconds: Interval for rate limit summary reports

        """
        self.rate_limiter = GlobalRateLimiter()
        self.emit_warning_on_limit = None
        self.warning_interval_seconds = warning_interval_seconds

        # Track last warning time per logger
        self.last_warning_times: dict[str, float] = {}

        # Track suppressed message counts
        self.suppressed_counts: dict[str, int] = {}
        self.last_summary_time = time.monotonic()
        self.summary_interval = summary_interval_seconds  # Emit summary periodically

    def xǁRateLimiterProcessorǁ__init____mutmut_6(
        self,
        emit_warning_on_limit: bool = True,
        warning_interval_seconds: float = 60.0,
        summary_interval_seconds: float = 5.0,
    ) -> None:
        """Initialize the rate limiter processor.

        Args:
            emit_warning_on_limit: Whether to emit a warning when rate limited
            warning_interval_seconds: Minimum seconds between rate limit warnings
            summary_interval_seconds: Interval for rate limit summary reports

        """
        self.rate_limiter = GlobalRateLimiter()
        self.emit_warning_on_limit = emit_warning_on_limit
        self.warning_interval_seconds = None

        # Track last warning time per logger
        self.last_warning_times: dict[str, float] = {}

        # Track suppressed message counts
        self.suppressed_counts: dict[str, int] = {}
        self.last_summary_time = time.monotonic()
        self.summary_interval = summary_interval_seconds  # Emit summary periodically

    def xǁRateLimiterProcessorǁ__init____mutmut_7(
        self,
        emit_warning_on_limit: bool = True,
        warning_interval_seconds: float = 60.0,
        summary_interval_seconds: float = 5.0,
    ) -> None:
        """Initialize the rate limiter processor.

        Args:
            emit_warning_on_limit: Whether to emit a warning when rate limited
            warning_interval_seconds: Minimum seconds between rate limit warnings
            summary_interval_seconds: Interval for rate limit summary reports

        """
        self.rate_limiter = GlobalRateLimiter()
        self.emit_warning_on_limit = emit_warning_on_limit
        self.warning_interval_seconds = warning_interval_seconds

        # Track last warning time per logger
        self.last_warning_times: dict[str, float] = None

        # Track suppressed message counts
        self.suppressed_counts: dict[str, int] = {}
        self.last_summary_time = time.monotonic()
        self.summary_interval = summary_interval_seconds  # Emit summary periodically

    def xǁRateLimiterProcessorǁ__init____mutmut_8(
        self,
        emit_warning_on_limit: bool = True,
        warning_interval_seconds: float = 60.0,
        summary_interval_seconds: float = 5.0,
    ) -> None:
        """Initialize the rate limiter processor.

        Args:
            emit_warning_on_limit: Whether to emit a warning when rate limited
            warning_interval_seconds: Minimum seconds between rate limit warnings
            summary_interval_seconds: Interval for rate limit summary reports

        """
        self.rate_limiter = GlobalRateLimiter()
        self.emit_warning_on_limit = emit_warning_on_limit
        self.warning_interval_seconds = warning_interval_seconds

        # Track last warning time per logger
        self.last_warning_times: dict[str, float] = {}

        # Track suppressed message counts
        self.suppressed_counts: dict[str, int] = None
        self.last_summary_time = time.monotonic()
        self.summary_interval = summary_interval_seconds  # Emit summary periodically

    def xǁRateLimiterProcessorǁ__init____mutmut_9(
        self,
        emit_warning_on_limit: bool = True,
        warning_interval_seconds: float = 60.0,
        summary_interval_seconds: float = 5.0,
    ) -> None:
        """Initialize the rate limiter processor.

        Args:
            emit_warning_on_limit: Whether to emit a warning when rate limited
            warning_interval_seconds: Minimum seconds between rate limit warnings
            summary_interval_seconds: Interval for rate limit summary reports

        """
        self.rate_limiter = GlobalRateLimiter()
        self.emit_warning_on_limit = emit_warning_on_limit
        self.warning_interval_seconds = warning_interval_seconds

        # Track last warning time per logger
        self.last_warning_times: dict[str, float] = {}

        # Track suppressed message counts
        self.suppressed_counts: dict[str, int] = {}
        self.last_summary_time = None
        self.summary_interval = summary_interval_seconds  # Emit summary periodically

    def xǁRateLimiterProcessorǁ__init____mutmut_10(
        self,
        emit_warning_on_limit: bool = True,
        warning_interval_seconds: float = 60.0,
        summary_interval_seconds: float = 5.0,
    ) -> None:
        """Initialize the rate limiter processor.

        Args:
            emit_warning_on_limit: Whether to emit a warning when rate limited
            warning_interval_seconds: Minimum seconds between rate limit warnings
            summary_interval_seconds: Interval for rate limit summary reports

        """
        self.rate_limiter = GlobalRateLimiter()
        self.emit_warning_on_limit = emit_warning_on_limit
        self.warning_interval_seconds = warning_interval_seconds

        # Track last warning time per logger
        self.last_warning_times: dict[str, float] = {}

        # Track suppressed message counts
        self.suppressed_counts: dict[str, int] = {}
        self.last_summary_time = time.monotonic()
        self.summary_interval = None  # Emit summary periodically

    xǁRateLimiterProcessorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁRateLimiterProcessorǁ__init____mutmut_1": xǁRateLimiterProcessorǁ__init____mutmut_1,
        "xǁRateLimiterProcessorǁ__init____mutmut_2": xǁRateLimiterProcessorǁ__init____mutmut_2,
        "xǁRateLimiterProcessorǁ__init____mutmut_3": xǁRateLimiterProcessorǁ__init____mutmut_3,
        "xǁRateLimiterProcessorǁ__init____mutmut_4": xǁRateLimiterProcessorǁ__init____mutmut_4,
        "xǁRateLimiterProcessorǁ__init____mutmut_5": xǁRateLimiterProcessorǁ__init____mutmut_5,
        "xǁRateLimiterProcessorǁ__init____mutmut_6": xǁRateLimiterProcessorǁ__init____mutmut_6,
        "xǁRateLimiterProcessorǁ__init____mutmut_7": xǁRateLimiterProcessorǁ__init____mutmut_7,
        "xǁRateLimiterProcessorǁ__init____mutmut_8": xǁRateLimiterProcessorǁ__init____mutmut_8,
        "xǁRateLimiterProcessorǁ__init____mutmut_9": xǁRateLimiterProcessorǁ__init____mutmut_9,
        "xǁRateLimiterProcessorǁ__init____mutmut_10": xǁRateLimiterProcessorǁ__init____mutmut_10,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁRateLimiterProcessorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁRateLimiterProcessorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁRateLimiterProcessorǁ__init____mutmut_orig)
    xǁRateLimiterProcessorǁ__init____mutmut_orig.__name__ = "xǁRateLimiterProcessorǁ__init__"

    def xǁRateLimiterProcessorǁ__call____mutmut_orig(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_1(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = None

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_2(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get(None, "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_3(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", None)

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_4(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_5(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get(
            "logger_name",
        )

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_6(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("XXlogger_nameXX", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_7(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("LOGGER_NAME", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_8(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "XXunknownXX")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_9(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "UNKNOWN")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_10(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = None

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_11(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(None, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_12(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, None)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_13(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_14(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(
            logger_name,
        )

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_15(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_16(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_17(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = None
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_18(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 1
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_19(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] = 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_20(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] -= 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_21(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 2

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_22(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = None
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_23(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = None

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_24(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(None, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_25(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, None)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_26(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_27(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(
                    logger_name,
                )

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_28(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 1)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_29(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now + last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_30(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning > self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_31(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = None

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_32(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "XXeventXX": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_33(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "EVENT": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_34(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "XXlevelXX": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_35(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "LEVEL": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_36(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "XXwarningXX",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_37(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "WARNING",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_38(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "XXlogger_nameXX": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_39(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "LOGGER_NAME": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_40(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "XXprovide.foundation.ratelimitXX",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_41(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "PROVIDE.FOUNDATION.RATELIMIT",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_42(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "XXsuppressed_countXX": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_43(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "SUPPRESSED_COUNT": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_44(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "XXoriginal_loggerXX": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_45(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "ORIGINAL_LOGGER": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_46(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "XX_rate_limit_warningXX": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_47(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_RATE_LIMIT_WARNING": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_48(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": False,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_49(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = None
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_50(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now + self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_51(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time > self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = now

        return event_dict

    def xǁRateLimiterProcessorǁ__call____mutmut_52(
        self,
        logger: Any,
        method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Process a log event, applying rate limiting.

        Args:
            logger: The logger instance
            method_name: The log method name (debug, info, etc.)
            event_dict: The event dictionary

        Returns:
            The event dictionary if allowed, or raises DropEvent if rate limited

        """
        logger_name = event_dict.get("logger_name", "unknown")

        # Check if this log is allowed (pass event_dict for tracking)
        allowed, reason = self.rate_limiter.is_allowed(logger_name, event_dict)

        if not allowed:
            # Track suppressed count
            if logger_name not in self.suppressed_counts:
                self.suppressed_counts[logger_name] = 0
            self.suppressed_counts[logger_name] += 1

            # Optionally emit a warning about rate limiting
            if self.emit_warning_on_limit:
                now = time.monotonic()
                last_warning = self.last_warning_times.get(logger_name, 0)

                if now - last_warning >= self.warning_interval_seconds:
                    # Create a rate limit warning event
                    self.last_warning_times[logger_name] = now

                    # Return a modified event indicating rate limiting
                    return {
                        "event": f"⚠️ Rate limit: {reason}",
                        "level": "warning",
                        "logger_name": "provide.foundation.ratelimit",
                        "suppressed_count": self.suppressed_counts[logger_name],
                        "original_logger": logger_name,
                        "_rate_limit_warning": True,
                    }

            # Drop the event
            raise structlog.DropEvent

        # Check if we should emit a summary
        now = time.monotonic()
        if now - self.last_summary_time >= self.summary_interval:
            # Always check and emit summary if there's been any rate limiting
            self._emit_summary()
            self.last_summary_time = None

        return event_dict

    xǁRateLimiterProcessorǁ__call____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁRateLimiterProcessorǁ__call____mutmut_1": xǁRateLimiterProcessorǁ__call____mutmut_1,
        "xǁRateLimiterProcessorǁ__call____mutmut_2": xǁRateLimiterProcessorǁ__call____mutmut_2,
        "xǁRateLimiterProcessorǁ__call____mutmut_3": xǁRateLimiterProcessorǁ__call____mutmut_3,
        "xǁRateLimiterProcessorǁ__call____mutmut_4": xǁRateLimiterProcessorǁ__call____mutmut_4,
        "xǁRateLimiterProcessorǁ__call____mutmut_5": xǁRateLimiterProcessorǁ__call____mutmut_5,
        "xǁRateLimiterProcessorǁ__call____mutmut_6": xǁRateLimiterProcessorǁ__call____mutmut_6,
        "xǁRateLimiterProcessorǁ__call____mutmut_7": xǁRateLimiterProcessorǁ__call____mutmut_7,
        "xǁRateLimiterProcessorǁ__call____mutmut_8": xǁRateLimiterProcessorǁ__call____mutmut_8,
        "xǁRateLimiterProcessorǁ__call____mutmut_9": xǁRateLimiterProcessorǁ__call____mutmut_9,
        "xǁRateLimiterProcessorǁ__call____mutmut_10": xǁRateLimiterProcessorǁ__call____mutmut_10,
        "xǁRateLimiterProcessorǁ__call____mutmut_11": xǁRateLimiterProcessorǁ__call____mutmut_11,
        "xǁRateLimiterProcessorǁ__call____mutmut_12": xǁRateLimiterProcessorǁ__call____mutmut_12,
        "xǁRateLimiterProcessorǁ__call____mutmut_13": xǁRateLimiterProcessorǁ__call____mutmut_13,
        "xǁRateLimiterProcessorǁ__call____mutmut_14": xǁRateLimiterProcessorǁ__call____mutmut_14,
        "xǁRateLimiterProcessorǁ__call____mutmut_15": xǁRateLimiterProcessorǁ__call____mutmut_15,
        "xǁRateLimiterProcessorǁ__call____mutmut_16": xǁRateLimiterProcessorǁ__call____mutmut_16,
        "xǁRateLimiterProcessorǁ__call____mutmut_17": xǁRateLimiterProcessorǁ__call____mutmut_17,
        "xǁRateLimiterProcessorǁ__call____mutmut_18": xǁRateLimiterProcessorǁ__call____mutmut_18,
        "xǁRateLimiterProcessorǁ__call____mutmut_19": xǁRateLimiterProcessorǁ__call____mutmut_19,
        "xǁRateLimiterProcessorǁ__call____mutmut_20": xǁRateLimiterProcessorǁ__call____mutmut_20,
        "xǁRateLimiterProcessorǁ__call____mutmut_21": xǁRateLimiterProcessorǁ__call____mutmut_21,
        "xǁRateLimiterProcessorǁ__call____mutmut_22": xǁRateLimiterProcessorǁ__call____mutmut_22,
        "xǁRateLimiterProcessorǁ__call____mutmut_23": xǁRateLimiterProcessorǁ__call____mutmut_23,
        "xǁRateLimiterProcessorǁ__call____mutmut_24": xǁRateLimiterProcessorǁ__call____mutmut_24,
        "xǁRateLimiterProcessorǁ__call____mutmut_25": xǁRateLimiterProcessorǁ__call____mutmut_25,
        "xǁRateLimiterProcessorǁ__call____mutmut_26": xǁRateLimiterProcessorǁ__call____mutmut_26,
        "xǁRateLimiterProcessorǁ__call____mutmut_27": xǁRateLimiterProcessorǁ__call____mutmut_27,
        "xǁRateLimiterProcessorǁ__call____mutmut_28": xǁRateLimiterProcessorǁ__call____mutmut_28,
        "xǁRateLimiterProcessorǁ__call____mutmut_29": xǁRateLimiterProcessorǁ__call____mutmut_29,
        "xǁRateLimiterProcessorǁ__call____mutmut_30": xǁRateLimiterProcessorǁ__call____mutmut_30,
        "xǁRateLimiterProcessorǁ__call____mutmut_31": xǁRateLimiterProcessorǁ__call____mutmut_31,
        "xǁRateLimiterProcessorǁ__call____mutmut_32": xǁRateLimiterProcessorǁ__call____mutmut_32,
        "xǁRateLimiterProcessorǁ__call____mutmut_33": xǁRateLimiterProcessorǁ__call____mutmut_33,
        "xǁRateLimiterProcessorǁ__call____mutmut_34": xǁRateLimiterProcessorǁ__call____mutmut_34,
        "xǁRateLimiterProcessorǁ__call____mutmut_35": xǁRateLimiterProcessorǁ__call____mutmut_35,
        "xǁRateLimiterProcessorǁ__call____mutmut_36": xǁRateLimiterProcessorǁ__call____mutmut_36,
        "xǁRateLimiterProcessorǁ__call____mutmut_37": xǁRateLimiterProcessorǁ__call____mutmut_37,
        "xǁRateLimiterProcessorǁ__call____mutmut_38": xǁRateLimiterProcessorǁ__call____mutmut_38,
        "xǁRateLimiterProcessorǁ__call____mutmut_39": xǁRateLimiterProcessorǁ__call____mutmut_39,
        "xǁRateLimiterProcessorǁ__call____mutmut_40": xǁRateLimiterProcessorǁ__call____mutmut_40,
        "xǁRateLimiterProcessorǁ__call____mutmut_41": xǁRateLimiterProcessorǁ__call____mutmut_41,
        "xǁRateLimiterProcessorǁ__call____mutmut_42": xǁRateLimiterProcessorǁ__call____mutmut_42,
        "xǁRateLimiterProcessorǁ__call____mutmut_43": xǁRateLimiterProcessorǁ__call____mutmut_43,
        "xǁRateLimiterProcessorǁ__call____mutmut_44": xǁRateLimiterProcessorǁ__call____mutmut_44,
        "xǁRateLimiterProcessorǁ__call____mutmut_45": xǁRateLimiterProcessorǁ__call____mutmut_45,
        "xǁRateLimiterProcessorǁ__call____mutmut_46": xǁRateLimiterProcessorǁ__call____mutmut_46,
        "xǁRateLimiterProcessorǁ__call____mutmut_47": xǁRateLimiterProcessorǁ__call____mutmut_47,
        "xǁRateLimiterProcessorǁ__call____mutmut_48": xǁRateLimiterProcessorǁ__call____mutmut_48,
        "xǁRateLimiterProcessorǁ__call____mutmut_49": xǁRateLimiterProcessorǁ__call____mutmut_49,
        "xǁRateLimiterProcessorǁ__call____mutmut_50": xǁRateLimiterProcessorǁ__call____mutmut_50,
        "xǁRateLimiterProcessorǁ__call____mutmut_51": xǁRateLimiterProcessorǁ__call____mutmut_51,
        "xǁRateLimiterProcessorǁ__call____mutmut_52": xǁRateLimiterProcessorǁ__call____mutmut_52,
    }

    def __call__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁRateLimiterProcessorǁ__call____mutmut_orig"),
            object.__getattribute__(self, "xǁRateLimiterProcessorǁ__call____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __call__.__signature__ = _mutmut_signature(xǁRateLimiterProcessorǁ__call____mutmut_orig)
    xǁRateLimiterProcessorǁ__call____mutmut_orig.__name__ = "xǁRateLimiterProcessorǁ__call__"

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_orig(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_1(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = None

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_2(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = None
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_3(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") and {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_4(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get(None) or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_5(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("XXglobalXX") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_6(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("GLOBAL") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_7(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = None

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_8(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get(None, 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_9(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", None)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_10(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get(0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_11(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get(
            "total_denied",
        )

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_12(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("XXtotal_deniedXX", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_13(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("TOTAL_DENIED", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_14(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 1)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_15(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts or total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_16(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_17(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied != 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_18(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 1:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_19(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = None

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_20(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(None)

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_21(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = None

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_22(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger(None)

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_23(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("XXprovide.foundation.ratelimit.summaryXX")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_24(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("PROVIDE.FOUNDATION.RATELIMIT.SUMMARY")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_25(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = None
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_26(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get(None, 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_27(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", None)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_28(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get(0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_29(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get(
                "total_allowed",
            )
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_30(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("XXtotal_allowedXX", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_31(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("TOTAL_ALLOWED", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_32(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 1)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_33(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = None
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_34(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed - total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_35(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = None

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_36(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts / 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_37(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied * total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_38(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 101 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_39(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts >= 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_40(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 1 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_41(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 1

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_42(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                None,
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_43(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=None,
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_44(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=None,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_45(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=None,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_46(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=None,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_47(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=None,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_48(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=None,
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_49(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=None,
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_50(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=None,
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_51(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_52(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_53(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_54(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_55(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_56(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_57(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_58(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_59(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_60(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get(None, 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_61(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', None):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_62(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get(0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_63(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available'):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_64(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('XXtokens_availableXX', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_65(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('TOKENS_AVAILABLE', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_66(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 1):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_67(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get(None, 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_68(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', None):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_69(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get(0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_70(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity'):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_71(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('XXcapacityXX', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_72(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('CAPACITY', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_73(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 1):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_74(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(None) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_75(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get(None, 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_76(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", None),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_77(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get(0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_78(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get(
                    "tokens_available",
                ),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_79(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("XXtokens_availableXX", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_80(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("TOKENS_AVAILABLE", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_81(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 1),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_82(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get(None, 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_83(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", None),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_84(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get(0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_85(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get(
                    "capacity",
                ),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_86(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("XXcapacityXX", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_87(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("CAPACITY", 0),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_88(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 1),
                refill_rate=global_stats.get("refill_rate", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_89(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get(None, 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_90(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", None),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_91(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get(0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_92(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get(
                    "refill_rate",
                ),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_93(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("XXrefill_rateXX", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_94(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("REFILL_RATE", 0),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    def xǁRateLimiterProcessorǁ_emit_summary__mutmut_95(self) -> None:
        """Emit a summary of rate-limited messages."""
        # Get current stats first to check if any rate limiting has occurred
        stats = self.rate_limiter.get_stats()

        # Check if there's been any rate limiting activity
        global_stats = stats.get("global") or {}
        total_denied = global_stats.get("total_denied", 0)

        if not self.suppressed_counts and total_denied == 0:
            return  # No rate limiting activity to report

        total_suppressed = sum(self.suppressed_counts.values())

        # Get a logger for rate limit summaries
        try:
            from provide.foundation.logger import get_logger

            summary_logger = get_logger("provide.foundation.ratelimit.summary")

            # Calculate rate limiting percentage
            total_allowed = global_stats.get("total_allowed", 0)
            total_attempts = total_allowed + total_denied
            denial_rate = total_denied / total_attempts * 100 if total_attempts > 0 else 0

            # Format the summary message
            summary_logger.warning(
                f"⚠️ Rate limiting active: {total_suppressed:,} logs dropped in last {self.summary_interval}s | "
                f"Denial rate: {denial_rate:.1f}% | "
                f"Tokens: {global_stats.get('tokens_available', 0):.0f}/{global_stats.get('capacity', 0):.0f}",
                suppressed_by_logger=dict(self.suppressed_counts) if self.suppressed_counts else {},
                total_suppressed=total_suppressed,
                total_denied_overall=total_denied,
                total_allowed_overall=total_allowed,
                denial_rate_percent=denial_rate,
                tokens_available=global_stats.get("tokens_available", 0),
                capacity=global_stats.get("capacity", 0),
                refill_rate=global_stats.get("refill_rate", 1),
            )

            # Reset counts after summary
            self.suppressed_counts.clear()
        except Exception:
            # If we can't log the summary, just clear counts
            self.suppressed_counts.clear()

    xǁRateLimiterProcessorǁ_emit_summary__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_1": xǁRateLimiterProcessorǁ_emit_summary__mutmut_1,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_2": xǁRateLimiterProcessorǁ_emit_summary__mutmut_2,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_3": xǁRateLimiterProcessorǁ_emit_summary__mutmut_3,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_4": xǁRateLimiterProcessorǁ_emit_summary__mutmut_4,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_5": xǁRateLimiterProcessorǁ_emit_summary__mutmut_5,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_6": xǁRateLimiterProcessorǁ_emit_summary__mutmut_6,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_7": xǁRateLimiterProcessorǁ_emit_summary__mutmut_7,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_8": xǁRateLimiterProcessorǁ_emit_summary__mutmut_8,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_9": xǁRateLimiterProcessorǁ_emit_summary__mutmut_9,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_10": xǁRateLimiterProcessorǁ_emit_summary__mutmut_10,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_11": xǁRateLimiterProcessorǁ_emit_summary__mutmut_11,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_12": xǁRateLimiterProcessorǁ_emit_summary__mutmut_12,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_13": xǁRateLimiterProcessorǁ_emit_summary__mutmut_13,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_14": xǁRateLimiterProcessorǁ_emit_summary__mutmut_14,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_15": xǁRateLimiterProcessorǁ_emit_summary__mutmut_15,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_16": xǁRateLimiterProcessorǁ_emit_summary__mutmut_16,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_17": xǁRateLimiterProcessorǁ_emit_summary__mutmut_17,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_18": xǁRateLimiterProcessorǁ_emit_summary__mutmut_18,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_19": xǁRateLimiterProcessorǁ_emit_summary__mutmut_19,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_20": xǁRateLimiterProcessorǁ_emit_summary__mutmut_20,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_21": xǁRateLimiterProcessorǁ_emit_summary__mutmut_21,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_22": xǁRateLimiterProcessorǁ_emit_summary__mutmut_22,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_23": xǁRateLimiterProcessorǁ_emit_summary__mutmut_23,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_24": xǁRateLimiterProcessorǁ_emit_summary__mutmut_24,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_25": xǁRateLimiterProcessorǁ_emit_summary__mutmut_25,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_26": xǁRateLimiterProcessorǁ_emit_summary__mutmut_26,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_27": xǁRateLimiterProcessorǁ_emit_summary__mutmut_27,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_28": xǁRateLimiterProcessorǁ_emit_summary__mutmut_28,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_29": xǁRateLimiterProcessorǁ_emit_summary__mutmut_29,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_30": xǁRateLimiterProcessorǁ_emit_summary__mutmut_30,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_31": xǁRateLimiterProcessorǁ_emit_summary__mutmut_31,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_32": xǁRateLimiterProcessorǁ_emit_summary__mutmut_32,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_33": xǁRateLimiterProcessorǁ_emit_summary__mutmut_33,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_34": xǁRateLimiterProcessorǁ_emit_summary__mutmut_34,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_35": xǁRateLimiterProcessorǁ_emit_summary__mutmut_35,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_36": xǁRateLimiterProcessorǁ_emit_summary__mutmut_36,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_37": xǁRateLimiterProcessorǁ_emit_summary__mutmut_37,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_38": xǁRateLimiterProcessorǁ_emit_summary__mutmut_38,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_39": xǁRateLimiterProcessorǁ_emit_summary__mutmut_39,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_40": xǁRateLimiterProcessorǁ_emit_summary__mutmut_40,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_41": xǁRateLimiterProcessorǁ_emit_summary__mutmut_41,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_42": xǁRateLimiterProcessorǁ_emit_summary__mutmut_42,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_43": xǁRateLimiterProcessorǁ_emit_summary__mutmut_43,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_44": xǁRateLimiterProcessorǁ_emit_summary__mutmut_44,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_45": xǁRateLimiterProcessorǁ_emit_summary__mutmut_45,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_46": xǁRateLimiterProcessorǁ_emit_summary__mutmut_46,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_47": xǁRateLimiterProcessorǁ_emit_summary__mutmut_47,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_48": xǁRateLimiterProcessorǁ_emit_summary__mutmut_48,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_49": xǁRateLimiterProcessorǁ_emit_summary__mutmut_49,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_50": xǁRateLimiterProcessorǁ_emit_summary__mutmut_50,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_51": xǁRateLimiterProcessorǁ_emit_summary__mutmut_51,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_52": xǁRateLimiterProcessorǁ_emit_summary__mutmut_52,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_53": xǁRateLimiterProcessorǁ_emit_summary__mutmut_53,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_54": xǁRateLimiterProcessorǁ_emit_summary__mutmut_54,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_55": xǁRateLimiterProcessorǁ_emit_summary__mutmut_55,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_56": xǁRateLimiterProcessorǁ_emit_summary__mutmut_56,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_57": xǁRateLimiterProcessorǁ_emit_summary__mutmut_57,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_58": xǁRateLimiterProcessorǁ_emit_summary__mutmut_58,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_59": xǁRateLimiterProcessorǁ_emit_summary__mutmut_59,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_60": xǁRateLimiterProcessorǁ_emit_summary__mutmut_60,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_61": xǁRateLimiterProcessorǁ_emit_summary__mutmut_61,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_62": xǁRateLimiterProcessorǁ_emit_summary__mutmut_62,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_63": xǁRateLimiterProcessorǁ_emit_summary__mutmut_63,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_64": xǁRateLimiterProcessorǁ_emit_summary__mutmut_64,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_65": xǁRateLimiterProcessorǁ_emit_summary__mutmut_65,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_66": xǁRateLimiterProcessorǁ_emit_summary__mutmut_66,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_67": xǁRateLimiterProcessorǁ_emit_summary__mutmut_67,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_68": xǁRateLimiterProcessorǁ_emit_summary__mutmut_68,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_69": xǁRateLimiterProcessorǁ_emit_summary__mutmut_69,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_70": xǁRateLimiterProcessorǁ_emit_summary__mutmut_70,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_71": xǁRateLimiterProcessorǁ_emit_summary__mutmut_71,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_72": xǁRateLimiterProcessorǁ_emit_summary__mutmut_72,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_73": xǁRateLimiterProcessorǁ_emit_summary__mutmut_73,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_74": xǁRateLimiterProcessorǁ_emit_summary__mutmut_74,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_75": xǁRateLimiterProcessorǁ_emit_summary__mutmut_75,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_76": xǁRateLimiterProcessorǁ_emit_summary__mutmut_76,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_77": xǁRateLimiterProcessorǁ_emit_summary__mutmut_77,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_78": xǁRateLimiterProcessorǁ_emit_summary__mutmut_78,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_79": xǁRateLimiterProcessorǁ_emit_summary__mutmut_79,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_80": xǁRateLimiterProcessorǁ_emit_summary__mutmut_80,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_81": xǁRateLimiterProcessorǁ_emit_summary__mutmut_81,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_82": xǁRateLimiterProcessorǁ_emit_summary__mutmut_82,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_83": xǁRateLimiterProcessorǁ_emit_summary__mutmut_83,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_84": xǁRateLimiterProcessorǁ_emit_summary__mutmut_84,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_85": xǁRateLimiterProcessorǁ_emit_summary__mutmut_85,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_86": xǁRateLimiterProcessorǁ_emit_summary__mutmut_86,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_87": xǁRateLimiterProcessorǁ_emit_summary__mutmut_87,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_88": xǁRateLimiterProcessorǁ_emit_summary__mutmut_88,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_89": xǁRateLimiterProcessorǁ_emit_summary__mutmut_89,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_90": xǁRateLimiterProcessorǁ_emit_summary__mutmut_90,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_91": xǁRateLimiterProcessorǁ_emit_summary__mutmut_91,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_92": xǁRateLimiterProcessorǁ_emit_summary__mutmut_92,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_93": xǁRateLimiterProcessorǁ_emit_summary__mutmut_93,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_94": xǁRateLimiterProcessorǁ_emit_summary__mutmut_94,
        "xǁRateLimiterProcessorǁ_emit_summary__mutmut_95": xǁRateLimiterProcessorǁ_emit_summary__mutmut_95,
    }

    def _emit_summary(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁRateLimiterProcessorǁ_emit_summary__mutmut_orig"),
            object.__getattribute__(self, "xǁRateLimiterProcessorǁ_emit_summary__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _emit_summary.__signature__ = _mutmut_signature(xǁRateLimiterProcessorǁ_emit_summary__mutmut_orig)
    xǁRateLimiterProcessorǁ_emit_summary__mutmut_orig.__name__ = "xǁRateLimiterProcessorǁ_emit_summary"


def x_create_rate_limiter_processor__mutmut_orig(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_1(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = False,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_2(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 6.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_3(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1001,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_4(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "XXdrop_oldestXX",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_5(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "DROP_OLDEST",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_6(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = None

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_7(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=None,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_8(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=None,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_9(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_10(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_11(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = None

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_12(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 or overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_13(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size >= 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_14(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 1 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_15(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy not in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_16(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "XXdrop_oldestXX",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_17(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "DROP_OLDEST",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_18(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "XXdrop_newestXX",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_19(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "DROP_NEWEST",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_20(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=None,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_21(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=None,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_22(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=None,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_23(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=None,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_24(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=None,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_25(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=None,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_26(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=None,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_27(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_28(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_29(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_30(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_31(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_memory_mb=max_memory_mb,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_32(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        overflow_policy=overflow_policy,
    )

    return processor


def x_create_rate_limiter_processor__mutmut_33(
    global_rate: float | None = None,
    global_capacity: float | None = None,
    per_logger_rates: dict[str, tuple[float, float]] | None = None,
    emit_warnings: bool = True,
    summary_interval: float = 5.0,
    max_queue_size: int = 1000,
    max_memory_mb: float | None = None,
    overflow_policy: str = "drop_oldest",
) -> RateLimiterProcessor:
    """Factory function to create and configure a rate limiter processor.

    Args:
        global_rate: Global logs per second limit
        global_capacity: Global burst capacity
        per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
        emit_warnings: Whether to emit warnings when rate limited
        summary_interval: Seconds between rate limit summary reports
        max_queue_size: Maximum queue size when buffering
        max_memory_mb: Maximum memory for buffered logs
        overflow_policy: Policy when queue is full

    Returns:
        Configured RateLimiterProcessor instance

    """
    processor = RateLimiterProcessor(
        emit_warning_on_limit=emit_warnings,
        summary_interval_seconds=summary_interval,
    )

    # Determine if we should use buffered rate limiting
    use_buffered = max_queue_size > 0 and overflow_policy in (
        "drop_oldest",
        "drop_newest",
    )

    # Configure the global rate limiter
    processor.rate_limiter.configure(
        global_rate=global_rate,
        global_capacity=global_capacity,
        per_logger_rates=per_logger_rates,
        use_buffered=use_buffered,
        max_queue_size=max_queue_size,
        max_memory_mb=max_memory_mb,
    )

    return processor


x_create_rate_limiter_processor__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_rate_limiter_processor__mutmut_1": x_create_rate_limiter_processor__mutmut_1,
    "x_create_rate_limiter_processor__mutmut_2": x_create_rate_limiter_processor__mutmut_2,
    "x_create_rate_limiter_processor__mutmut_3": x_create_rate_limiter_processor__mutmut_3,
    "x_create_rate_limiter_processor__mutmut_4": x_create_rate_limiter_processor__mutmut_4,
    "x_create_rate_limiter_processor__mutmut_5": x_create_rate_limiter_processor__mutmut_5,
    "x_create_rate_limiter_processor__mutmut_6": x_create_rate_limiter_processor__mutmut_6,
    "x_create_rate_limiter_processor__mutmut_7": x_create_rate_limiter_processor__mutmut_7,
    "x_create_rate_limiter_processor__mutmut_8": x_create_rate_limiter_processor__mutmut_8,
    "x_create_rate_limiter_processor__mutmut_9": x_create_rate_limiter_processor__mutmut_9,
    "x_create_rate_limiter_processor__mutmut_10": x_create_rate_limiter_processor__mutmut_10,
    "x_create_rate_limiter_processor__mutmut_11": x_create_rate_limiter_processor__mutmut_11,
    "x_create_rate_limiter_processor__mutmut_12": x_create_rate_limiter_processor__mutmut_12,
    "x_create_rate_limiter_processor__mutmut_13": x_create_rate_limiter_processor__mutmut_13,
    "x_create_rate_limiter_processor__mutmut_14": x_create_rate_limiter_processor__mutmut_14,
    "x_create_rate_limiter_processor__mutmut_15": x_create_rate_limiter_processor__mutmut_15,
    "x_create_rate_limiter_processor__mutmut_16": x_create_rate_limiter_processor__mutmut_16,
    "x_create_rate_limiter_processor__mutmut_17": x_create_rate_limiter_processor__mutmut_17,
    "x_create_rate_limiter_processor__mutmut_18": x_create_rate_limiter_processor__mutmut_18,
    "x_create_rate_limiter_processor__mutmut_19": x_create_rate_limiter_processor__mutmut_19,
    "x_create_rate_limiter_processor__mutmut_20": x_create_rate_limiter_processor__mutmut_20,
    "x_create_rate_limiter_processor__mutmut_21": x_create_rate_limiter_processor__mutmut_21,
    "x_create_rate_limiter_processor__mutmut_22": x_create_rate_limiter_processor__mutmut_22,
    "x_create_rate_limiter_processor__mutmut_23": x_create_rate_limiter_processor__mutmut_23,
    "x_create_rate_limiter_processor__mutmut_24": x_create_rate_limiter_processor__mutmut_24,
    "x_create_rate_limiter_processor__mutmut_25": x_create_rate_limiter_processor__mutmut_25,
    "x_create_rate_limiter_processor__mutmut_26": x_create_rate_limiter_processor__mutmut_26,
    "x_create_rate_limiter_processor__mutmut_27": x_create_rate_limiter_processor__mutmut_27,
    "x_create_rate_limiter_processor__mutmut_28": x_create_rate_limiter_processor__mutmut_28,
    "x_create_rate_limiter_processor__mutmut_29": x_create_rate_limiter_processor__mutmut_29,
    "x_create_rate_limiter_processor__mutmut_30": x_create_rate_limiter_processor__mutmut_30,
    "x_create_rate_limiter_processor__mutmut_31": x_create_rate_limiter_processor__mutmut_31,
    "x_create_rate_limiter_processor__mutmut_32": x_create_rate_limiter_processor__mutmut_32,
    "x_create_rate_limiter_processor__mutmut_33": x_create_rate_limiter_processor__mutmut_33,
}


def create_rate_limiter_processor(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_rate_limiter_processor__mutmut_orig,
        x_create_rate_limiter_processor__mutmut_mutants,
        args,
        kwargs,
    )
    return result


create_rate_limiter_processor.__signature__ = _mutmut_signature(x_create_rate_limiter_processor__mutmut_orig)
x_create_rate_limiter_processor__mutmut_orig.__name__ = "x_create_rate_limiter_processor"


# <3 🧱🤝📝🪄
