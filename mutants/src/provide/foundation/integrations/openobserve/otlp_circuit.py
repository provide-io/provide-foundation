# provide/foundation/integrations/openobserve/otlp_circuit.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import threading
import time
from typing import Any, Literal

"""Circuit breaker pattern for OTLP connection failures.

This prevents log spam when OTLP endpoint is unreachable by:
- Tracking failure counts and timestamps
- Automatically disabling OTLP after threshold failures
- Implementing exponential backoff before retry attempts
- Auto-recovering after cooldown period
"""

CircuitState = Literal["closed", "open", "half_open"]
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


class OTLPCircuitBreaker:
    """Circuit breaker for OTLP connections with exponential backoff.

    States:
        - closed: Normal operation, requests allowed
        - open: Too many failures, requests blocked
        - half_open: Testing if service recovered

    Examples:
        >>> breaker = OTLPCircuitBreaker(failure_threshold=3, timeout=60.0)
        >>> if breaker.can_attempt():
        ...     success = send_otlp_log()
        ...     if success:
        ...         breaker.record_success()
        ...     else:
        ...         breaker.record_failure()
    """

    def xǁOTLPCircuitBreakerǁ__init____mutmut_orig(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "closed"
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_1(
        self,
        failure_threshold: int = 6,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "closed"
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_2(
        self,
        failure_threshold: int = 5,
        timeout: float = 61.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "closed"
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_3(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 11.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "closed"
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_4(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = None
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "closed"
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_5(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = None
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "closed"
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_6(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = None

        self._state: CircuitState = "closed"
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_7(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = None
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_8(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "XXclosedXX"
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_9(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "CLOSED"
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_10(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "closed"
        self._failure_count = None
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_11(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "closed"
        self._failure_count = 1
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_12(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "closed"
        self._failure_count = 0
        self._last_failure_time: float | None = ""
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_13(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "closed"
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = ""
        self._open_count = 0  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_14(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "closed"
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = None  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_15(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "closed"
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 1  # Track how many times we've opened
        self._lock = threading.Lock()

    def xǁOTLPCircuitBreakerǁ__init____mutmut_16(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before attempting half-open (doubles each time)
            half_open_timeout: Seconds to wait in half-open before trying again
        """
        self.failure_threshold = failure_threshold
        self.base_timeout = timeout
        self.half_open_timeout = half_open_timeout

        self._state: CircuitState = "closed"
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._last_attempt_time: float | None = None
        self._open_count = 0  # Track how many times we've opened
        self._lock = None

    xǁOTLPCircuitBreakerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOTLPCircuitBreakerǁ__init____mutmut_1": xǁOTLPCircuitBreakerǁ__init____mutmut_1,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_2": xǁOTLPCircuitBreakerǁ__init____mutmut_2,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_3": xǁOTLPCircuitBreakerǁ__init____mutmut_3,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_4": xǁOTLPCircuitBreakerǁ__init____mutmut_4,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_5": xǁOTLPCircuitBreakerǁ__init____mutmut_5,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_6": xǁOTLPCircuitBreakerǁ__init____mutmut_6,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_7": xǁOTLPCircuitBreakerǁ__init____mutmut_7,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_8": xǁOTLPCircuitBreakerǁ__init____mutmut_8,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_9": xǁOTLPCircuitBreakerǁ__init____mutmut_9,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_10": xǁOTLPCircuitBreakerǁ__init____mutmut_10,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_11": xǁOTLPCircuitBreakerǁ__init____mutmut_11,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_12": xǁOTLPCircuitBreakerǁ__init____mutmut_12,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_13": xǁOTLPCircuitBreakerǁ__init____mutmut_13,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_14": xǁOTLPCircuitBreakerǁ__init____mutmut_14,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_15": xǁOTLPCircuitBreakerǁ__init____mutmut_15,
        "xǁOTLPCircuitBreakerǁ__init____mutmut_16": xǁOTLPCircuitBreakerǁ__init____mutmut_16,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOTLPCircuitBreakerǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁOTLPCircuitBreakerǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁOTLPCircuitBreakerǁ__init____mutmut_orig)
    xǁOTLPCircuitBreakerǁ__init____mutmut_orig.__name__ = "xǁOTLPCircuitBreakerǁ__init__"

    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        with self._lock:
            return self._state

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_orig(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_1(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = None

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_2(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state != "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_3(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "XXclosedXX":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_4(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "CLOSED":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_5(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return False

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_6(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state != "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_7(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "XXopenXX":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_8(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "OPEN":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_9(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is not None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_10(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return True

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_11(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = None
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_12(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout / (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_13(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 * min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_14(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (3 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_15(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(None, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_16(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, None))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_17(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_18(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (
                    2
                    ** min(
                        self._open_count,
                    )
                )
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_19(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 11))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_20(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now + self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_21(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time > current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_22(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = None
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_23(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "XXhalf_openXX"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_24(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "HALF_OPEN"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_25(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = None
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_26(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return False

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_27(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return True

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_28(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state != "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_29(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "XXhalf_openXX":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_30(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "HALF_OPEN":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_31(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is not None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_32(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return False

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_33(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now + self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_34(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time > self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_35(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = None
                    return True

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_36(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return False

                return False

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_37(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return True

            return False

    def xǁOTLPCircuitBreakerǁcan_attempt__mutmut_38(self) -> bool:
        """Check if we can attempt an OTLP operation.

        Returns:
            True if operation should be attempted, False if circuit is open
        """
        with self._lock:
            now = time.time()

            if self._state == "closed":
                return True

            if self._state == "open":
                # Check if enough time has passed to try half-open
                if self._last_failure_time is None:
                    return False

                # Exponential backoff: timeout doubles each time circuit opens
                current_timeout = self.base_timeout * (2 ** min(self._open_count, 10))
                if now - self._last_failure_time >= current_timeout:
                    self._state = "half_open"
                    self._last_attempt_time = now
                    return True

                return False

            if self._state == "half_open":
                # Only allow one attempt in half-open state within timeout window
                if self._last_attempt_time is None:
                    return True

                if now - self._last_attempt_time >= self.half_open_timeout:
                    self._last_attempt_time = now
                    return True

                return False

            return True

    xǁOTLPCircuitBreakerǁcan_attempt__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_1": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_1,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_2": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_2,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_3": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_3,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_4": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_4,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_5": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_5,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_6": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_6,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_7": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_7,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_8": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_8,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_9": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_9,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_10": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_10,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_11": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_11,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_12": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_12,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_13": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_13,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_14": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_14,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_15": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_15,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_16": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_16,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_17": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_17,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_18": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_18,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_19": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_19,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_20": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_20,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_21": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_21,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_22": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_22,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_23": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_23,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_24": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_24,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_25": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_25,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_26": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_26,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_27": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_27,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_28": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_28,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_29": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_29,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_30": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_30,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_31": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_31,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_32": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_32,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_33": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_33,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_34": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_34,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_35": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_35,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_36": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_36,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_37": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_37,
        "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_38": xǁOTLPCircuitBreakerǁcan_attempt__mutmut_38,
    }

    def can_attempt(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_orig"),
            object.__getattribute__(self, "xǁOTLPCircuitBreakerǁcan_attempt__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    can_attempt.__signature__ = _mutmut_signature(xǁOTLPCircuitBreakerǁcan_attempt__mutmut_orig)
    xǁOTLPCircuitBreakerǁcan_attempt__mutmut_orig.__name__ = "xǁOTLPCircuitBreakerǁcan_attempt"

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_orig(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(0, self._open_count - 1)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_1(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = None
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(0, self._open_count - 1)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_2(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "XXclosedXX"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(0, self._open_count - 1)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_3(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "CLOSED"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(0, self._open_count - 1)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_4(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = None
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(0, self._open_count - 1)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_5(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 1
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(0, self._open_count - 1)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_6(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = ""
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(0, self._open_count - 1)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_7(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = ""
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(0, self._open_count - 1)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_8(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count >= 0:
                self._open_count = max(0, self._open_count - 1)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_9(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 1:
                self._open_count = max(0, self._open_count - 1)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_10(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = None

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_11(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(None, self._open_count - 1)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_12(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(0, None)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_13(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(self._open_count - 1)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_14(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(
                    0,
                )

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_15(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(1, self._open_count - 1)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_16(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(0, self._open_count + 1)

    def xǁOTLPCircuitBreakerǁrecord_success__mutmut_17(self) -> None:
        """Record a successful operation."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            # Don't reset _open_count completely, but decay it
            if self._open_count > 0:
                self._open_count = max(0, self._open_count - 2)

    xǁOTLPCircuitBreakerǁrecord_success__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_1": xǁOTLPCircuitBreakerǁrecord_success__mutmut_1,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_2": xǁOTLPCircuitBreakerǁrecord_success__mutmut_2,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_3": xǁOTLPCircuitBreakerǁrecord_success__mutmut_3,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_4": xǁOTLPCircuitBreakerǁrecord_success__mutmut_4,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_5": xǁOTLPCircuitBreakerǁrecord_success__mutmut_5,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_6": xǁOTLPCircuitBreakerǁrecord_success__mutmut_6,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_7": xǁOTLPCircuitBreakerǁrecord_success__mutmut_7,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_8": xǁOTLPCircuitBreakerǁrecord_success__mutmut_8,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_9": xǁOTLPCircuitBreakerǁrecord_success__mutmut_9,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_10": xǁOTLPCircuitBreakerǁrecord_success__mutmut_10,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_11": xǁOTLPCircuitBreakerǁrecord_success__mutmut_11,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_12": xǁOTLPCircuitBreakerǁrecord_success__mutmut_12,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_13": xǁOTLPCircuitBreakerǁrecord_success__mutmut_13,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_14": xǁOTLPCircuitBreakerǁrecord_success__mutmut_14,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_15": xǁOTLPCircuitBreakerǁrecord_success__mutmut_15,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_16": xǁOTLPCircuitBreakerǁrecord_success__mutmut_16,
        "xǁOTLPCircuitBreakerǁrecord_success__mutmut_17": xǁOTLPCircuitBreakerǁrecord_success__mutmut_17,
    }

    def record_success(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOTLPCircuitBreakerǁrecord_success__mutmut_orig"),
            object.__getattribute__(self, "xǁOTLPCircuitBreakerǁrecord_success__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    record_success.__signature__ = _mutmut_signature(xǁOTLPCircuitBreakerǁrecord_success__mutmut_orig)
    xǁOTLPCircuitBreakerǁrecord_success__mutmut_orig.__name__ = "xǁOTLPCircuitBreakerǁrecord_success"

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_orig(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_1(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count = 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_2(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count -= 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_3(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 2
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_4(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = None

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_5(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state != "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_6(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "XXhalf_openXX":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_7(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "HALF_OPEN":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_8(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = None
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_9(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "XXopenXX"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_10(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "OPEN"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_11(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count = 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_12(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count -= 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_13(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 2
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_14(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count > self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_15(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = None
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_16(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "XXopenXX"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_17(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "OPEN"
                self._open_count += 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_18(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count = 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_19(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count -= 1

    def xǁOTLPCircuitBreakerǁrecord_failure__mutmut_20(self, error: Exception | None = None) -> None:
        """Record a failed operation.

        Args:
            error: Optional exception that caused the failure
        """
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half_open":
                # Failed during recovery attempt, go back to open
                self._state = "open"
                self._open_count += 1
            elif self._failure_count >= self.failure_threshold:
                # Too many failures, open the circuit
                self._state = "open"
                self._open_count += 2

    xǁOTLPCircuitBreakerǁrecord_failure__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_1": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_1,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_2": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_2,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_3": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_3,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_4": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_4,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_5": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_5,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_6": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_6,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_7": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_7,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_8": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_8,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_9": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_9,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_10": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_10,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_11": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_11,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_12": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_12,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_13": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_13,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_14": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_14,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_15": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_15,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_16": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_16,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_17": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_17,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_18": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_18,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_19": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_19,
        "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_20": xǁOTLPCircuitBreakerǁrecord_failure__mutmut_20,
    }

    def record_failure(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_orig"),
            object.__getattribute__(self, "xǁOTLPCircuitBreakerǁrecord_failure__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    record_failure.__signature__ = _mutmut_signature(xǁOTLPCircuitBreakerǁrecord_failure__mutmut_orig)
    xǁOTLPCircuitBreakerǁrecord_failure__mutmut_orig.__name__ = "xǁOTLPCircuitBreakerǁrecord_failure"

    def xǁOTLPCircuitBreakerǁreset__mutmut_orig(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            self._open_count = 0

    def xǁOTLPCircuitBreakerǁreset__mutmut_1(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        with self._lock:
            self._state = None
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            self._open_count = 0

    def xǁOTLPCircuitBreakerǁreset__mutmut_2(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        with self._lock:
            self._state = "XXclosedXX"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            self._open_count = 0

    def xǁOTLPCircuitBreakerǁreset__mutmut_3(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        with self._lock:
            self._state = "CLOSED"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            self._open_count = 0

    def xǁOTLPCircuitBreakerǁreset__mutmut_4(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        with self._lock:
            self._state = "closed"
            self._failure_count = None
            self._last_failure_time = None
            self._last_attempt_time = None
            self._open_count = 0

    def xǁOTLPCircuitBreakerǁreset__mutmut_5(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 1
            self._last_failure_time = None
            self._last_attempt_time = None
            self._open_count = 0

    def xǁOTLPCircuitBreakerǁreset__mutmut_6(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = ""
            self._last_attempt_time = None
            self._open_count = 0

    def xǁOTLPCircuitBreakerǁreset__mutmut_7(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = ""
            self._open_count = 0

    def xǁOTLPCircuitBreakerǁreset__mutmut_8(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            self._open_count = None

    def xǁOTLPCircuitBreakerǁreset__mutmut_9(self) -> None:
        """Manually reset the circuit breaker to closed state."""
        with self._lock:
            self._state = "closed"
            self._failure_count = 0
            self._last_failure_time = None
            self._last_attempt_time = None
            self._open_count = 1

    xǁOTLPCircuitBreakerǁreset__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOTLPCircuitBreakerǁreset__mutmut_1": xǁOTLPCircuitBreakerǁreset__mutmut_1,
        "xǁOTLPCircuitBreakerǁreset__mutmut_2": xǁOTLPCircuitBreakerǁreset__mutmut_2,
        "xǁOTLPCircuitBreakerǁreset__mutmut_3": xǁOTLPCircuitBreakerǁreset__mutmut_3,
        "xǁOTLPCircuitBreakerǁreset__mutmut_4": xǁOTLPCircuitBreakerǁreset__mutmut_4,
        "xǁOTLPCircuitBreakerǁreset__mutmut_5": xǁOTLPCircuitBreakerǁreset__mutmut_5,
        "xǁOTLPCircuitBreakerǁreset__mutmut_6": xǁOTLPCircuitBreakerǁreset__mutmut_6,
        "xǁOTLPCircuitBreakerǁreset__mutmut_7": xǁOTLPCircuitBreakerǁreset__mutmut_7,
        "xǁOTLPCircuitBreakerǁreset__mutmut_8": xǁOTLPCircuitBreakerǁreset__mutmut_8,
        "xǁOTLPCircuitBreakerǁreset__mutmut_9": xǁOTLPCircuitBreakerǁreset__mutmut_9,
    }

    def reset(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOTLPCircuitBreakerǁreset__mutmut_orig"),
            object.__getattribute__(self, "xǁOTLPCircuitBreakerǁreset__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    reset.__signature__ = _mutmut_signature(xǁOTLPCircuitBreakerǁreset__mutmut_orig)
    xǁOTLPCircuitBreakerǁreset__mutmut_orig.__name__ = "xǁOTLPCircuitBreakerǁreset"

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_orig(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_1(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "XXstateXX": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_2(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "STATE": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_3(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "XXfailure_countXX": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_4(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "FAILURE_COUNT": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_5(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "XXopen_countXX": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_6(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "OPEN_COUNT": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_7(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "XXlast_failure_timeXX": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_8(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "LAST_FAILURE_TIME": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_9(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "XXlast_attempt_timeXX": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_10(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "LAST_ATTEMPT_TIME": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_11(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "XXcurrent_timeoutXX": self.base_timeout * (2 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_12(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "CURRENT_TIMEOUT": self.base_timeout * (2 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_13(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout / (2 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_14(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 * min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_15(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (3 ** min(self._open_count, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_16(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(None, 10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_17(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(self._open_count, None)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_18(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(10)),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_19(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout
                * (
                    2
                    ** min(
                        self._open_count,
                    )
                ),
            }

    def xǁOTLPCircuitBreakerǁget_stats__mutmut_20(self) -> dict[str, Any]:
        """Get circuit breaker statistics.

        Returns:
            Dictionary with current state and statistics
        """
        with self._lock:
            return {
                "state": self._state,
                "failure_count": self._failure_count,
                "open_count": self._open_count,
                "last_failure_time": self._last_failure_time,
                "last_attempt_time": self._last_attempt_time,
                "current_timeout": self.base_timeout * (2 ** min(self._open_count, 11)),
            }

    xǁOTLPCircuitBreakerǁget_stats__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_1": xǁOTLPCircuitBreakerǁget_stats__mutmut_1,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_2": xǁOTLPCircuitBreakerǁget_stats__mutmut_2,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_3": xǁOTLPCircuitBreakerǁget_stats__mutmut_3,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_4": xǁOTLPCircuitBreakerǁget_stats__mutmut_4,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_5": xǁOTLPCircuitBreakerǁget_stats__mutmut_5,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_6": xǁOTLPCircuitBreakerǁget_stats__mutmut_6,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_7": xǁOTLPCircuitBreakerǁget_stats__mutmut_7,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_8": xǁOTLPCircuitBreakerǁget_stats__mutmut_8,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_9": xǁOTLPCircuitBreakerǁget_stats__mutmut_9,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_10": xǁOTLPCircuitBreakerǁget_stats__mutmut_10,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_11": xǁOTLPCircuitBreakerǁget_stats__mutmut_11,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_12": xǁOTLPCircuitBreakerǁget_stats__mutmut_12,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_13": xǁOTLPCircuitBreakerǁget_stats__mutmut_13,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_14": xǁOTLPCircuitBreakerǁget_stats__mutmut_14,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_15": xǁOTLPCircuitBreakerǁget_stats__mutmut_15,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_16": xǁOTLPCircuitBreakerǁget_stats__mutmut_16,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_17": xǁOTLPCircuitBreakerǁget_stats__mutmut_17,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_18": xǁOTLPCircuitBreakerǁget_stats__mutmut_18,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_19": xǁOTLPCircuitBreakerǁget_stats__mutmut_19,
        "xǁOTLPCircuitBreakerǁget_stats__mutmut_20": xǁOTLPCircuitBreakerǁget_stats__mutmut_20,
    }

    def get_stats(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁOTLPCircuitBreakerǁget_stats__mutmut_orig"),
            object.__getattribute__(self, "xǁOTLPCircuitBreakerǁget_stats__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_stats.__signature__ = _mutmut_signature(xǁOTLPCircuitBreakerǁget_stats__mutmut_orig)
    xǁOTLPCircuitBreakerǁget_stats__mutmut_orig.__name__ = "xǁOTLPCircuitBreakerǁget_stats"


# Global circuit breaker instance
_otlp_circuit_breaker: OTLPCircuitBreaker | None = None
_circuit_breaker_lock = threading.Lock()


def x_get_otlp_circuit_breaker__mutmut_orig() -> OTLPCircuitBreaker:
    """Get the global OTLP circuit breaker instance.

    Returns:
        Shared OTLPCircuitBreaker instance
    """
    global _otlp_circuit_breaker

    if _otlp_circuit_breaker is None:
        with _circuit_breaker_lock:
            if _otlp_circuit_breaker is None:
                _otlp_circuit_breaker = OTLPCircuitBreaker(
                    failure_threshold=5,  # Open after 5 failures
                    timeout=30.0,  # Start with 30s timeout
                    half_open_timeout=10.0,  # Wait 10s between half-open attempts
                )

    return _otlp_circuit_breaker


def x_get_otlp_circuit_breaker__mutmut_1() -> OTLPCircuitBreaker:
    """Get the global OTLP circuit breaker instance.

    Returns:
        Shared OTLPCircuitBreaker instance
    """
    global _otlp_circuit_breaker

    if _otlp_circuit_breaker is not None:
        with _circuit_breaker_lock:
            if _otlp_circuit_breaker is None:
                _otlp_circuit_breaker = OTLPCircuitBreaker(
                    failure_threshold=5,  # Open after 5 failures
                    timeout=30.0,  # Start with 30s timeout
                    half_open_timeout=10.0,  # Wait 10s between half-open attempts
                )

    return _otlp_circuit_breaker


def x_get_otlp_circuit_breaker__mutmut_2() -> OTLPCircuitBreaker:
    """Get the global OTLP circuit breaker instance.

    Returns:
        Shared OTLPCircuitBreaker instance
    """
    global _otlp_circuit_breaker

    if _otlp_circuit_breaker is None:
        with _circuit_breaker_lock:
            if _otlp_circuit_breaker is not None:
                _otlp_circuit_breaker = OTLPCircuitBreaker(
                    failure_threshold=5,  # Open after 5 failures
                    timeout=30.0,  # Start with 30s timeout
                    half_open_timeout=10.0,  # Wait 10s between half-open attempts
                )

    return _otlp_circuit_breaker


def x_get_otlp_circuit_breaker__mutmut_3() -> OTLPCircuitBreaker:
    """Get the global OTLP circuit breaker instance.

    Returns:
        Shared OTLPCircuitBreaker instance
    """
    global _otlp_circuit_breaker

    if _otlp_circuit_breaker is None:
        with _circuit_breaker_lock:
            if _otlp_circuit_breaker is None:
                _otlp_circuit_breaker = None

    return _otlp_circuit_breaker


def x_get_otlp_circuit_breaker__mutmut_4() -> OTLPCircuitBreaker:
    """Get the global OTLP circuit breaker instance.

    Returns:
        Shared OTLPCircuitBreaker instance
    """
    global _otlp_circuit_breaker

    if _otlp_circuit_breaker is None:
        with _circuit_breaker_lock:
            if _otlp_circuit_breaker is None:
                _otlp_circuit_breaker = OTLPCircuitBreaker(
                    failure_threshold=None,  # Open after 5 failures
                    timeout=30.0,  # Start with 30s timeout
                    half_open_timeout=10.0,  # Wait 10s between half-open attempts
                )

    return _otlp_circuit_breaker


def x_get_otlp_circuit_breaker__mutmut_5() -> OTLPCircuitBreaker:
    """Get the global OTLP circuit breaker instance.

    Returns:
        Shared OTLPCircuitBreaker instance
    """
    global _otlp_circuit_breaker

    if _otlp_circuit_breaker is None:
        with _circuit_breaker_lock:
            if _otlp_circuit_breaker is None:
                _otlp_circuit_breaker = OTLPCircuitBreaker(
                    failure_threshold=5,  # Open after 5 failures
                    timeout=None,  # Start with 30s timeout
                    half_open_timeout=10.0,  # Wait 10s between half-open attempts
                )

    return _otlp_circuit_breaker


def x_get_otlp_circuit_breaker__mutmut_6() -> OTLPCircuitBreaker:
    """Get the global OTLP circuit breaker instance.

    Returns:
        Shared OTLPCircuitBreaker instance
    """
    global _otlp_circuit_breaker

    if _otlp_circuit_breaker is None:
        with _circuit_breaker_lock:
            if _otlp_circuit_breaker is None:
                _otlp_circuit_breaker = OTLPCircuitBreaker(
                    failure_threshold=5,  # Open after 5 failures
                    timeout=30.0,  # Start with 30s timeout
                    half_open_timeout=None,  # Wait 10s between half-open attempts
                )

    return _otlp_circuit_breaker


def x_get_otlp_circuit_breaker__mutmut_7() -> OTLPCircuitBreaker:
    """Get the global OTLP circuit breaker instance.

    Returns:
        Shared OTLPCircuitBreaker instance
    """
    global _otlp_circuit_breaker

    if _otlp_circuit_breaker is None:
        with _circuit_breaker_lock:
            if _otlp_circuit_breaker is None:
                _otlp_circuit_breaker = OTLPCircuitBreaker(
                    timeout=30.0,  # Start with 30s timeout
                    half_open_timeout=10.0,  # Wait 10s between half-open attempts
                )

    return _otlp_circuit_breaker


def x_get_otlp_circuit_breaker__mutmut_8() -> OTLPCircuitBreaker:
    """Get the global OTLP circuit breaker instance.

    Returns:
        Shared OTLPCircuitBreaker instance
    """
    global _otlp_circuit_breaker

    if _otlp_circuit_breaker is None:
        with _circuit_breaker_lock:
            if _otlp_circuit_breaker is None:
                _otlp_circuit_breaker = OTLPCircuitBreaker(
                    failure_threshold=5,  # Open after 5 failures
                    half_open_timeout=10.0,  # Wait 10s between half-open attempts
                )

    return _otlp_circuit_breaker


def x_get_otlp_circuit_breaker__mutmut_9() -> OTLPCircuitBreaker:
    """Get the global OTLP circuit breaker instance.

    Returns:
        Shared OTLPCircuitBreaker instance
    """
    global _otlp_circuit_breaker

    if _otlp_circuit_breaker is None:
        with _circuit_breaker_lock:
            if _otlp_circuit_breaker is None:
                _otlp_circuit_breaker = OTLPCircuitBreaker(
                    failure_threshold=5,  # Open after 5 failures
                    timeout=30.0,  # Start with 30s timeout
                )

    return _otlp_circuit_breaker


def x_get_otlp_circuit_breaker__mutmut_10() -> OTLPCircuitBreaker:
    """Get the global OTLP circuit breaker instance.

    Returns:
        Shared OTLPCircuitBreaker instance
    """
    global _otlp_circuit_breaker

    if _otlp_circuit_breaker is None:
        with _circuit_breaker_lock:
            if _otlp_circuit_breaker is None:
                _otlp_circuit_breaker = OTLPCircuitBreaker(
                    failure_threshold=6,  # Open after 5 failures
                    timeout=30.0,  # Start with 30s timeout
                    half_open_timeout=10.0,  # Wait 10s between half-open attempts
                )

    return _otlp_circuit_breaker


def x_get_otlp_circuit_breaker__mutmut_11() -> OTLPCircuitBreaker:
    """Get the global OTLP circuit breaker instance.

    Returns:
        Shared OTLPCircuitBreaker instance
    """
    global _otlp_circuit_breaker

    if _otlp_circuit_breaker is None:
        with _circuit_breaker_lock:
            if _otlp_circuit_breaker is None:
                _otlp_circuit_breaker = OTLPCircuitBreaker(
                    failure_threshold=5,  # Open after 5 failures
                    timeout=31.0,  # Start with 30s timeout
                    half_open_timeout=10.0,  # Wait 10s between half-open attempts
                )

    return _otlp_circuit_breaker


def x_get_otlp_circuit_breaker__mutmut_12() -> OTLPCircuitBreaker:
    """Get the global OTLP circuit breaker instance.

    Returns:
        Shared OTLPCircuitBreaker instance
    """
    global _otlp_circuit_breaker

    if _otlp_circuit_breaker is None:
        with _circuit_breaker_lock:
            if _otlp_circuit_breaker is None:
                _otlp_circuit_breaker = OTLPCircuitBreaker(
                    failure_threshold=5,  # Open after 5 failures
                    timeout=30.0,  # Start with 30s timeout
                    half_open_timeout=11.0,  # Wait 10s between half-open attempts
                )

    return _otlp_circuit_breaker


x_get_otlp_circuit_breaker__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_otlp_circuit_breaker__mutmut_1": x_get_otlp_circuit_breaker__mutmut_1,
    "x_get_otlp_circuit_breaker__mutmut_2": x_get_otlp_circuit_breaker__mutmut_2,
    "x_get_otlp_circuit_breaker__mutmut_3": x_get_otlp_circuit_breaker__mutmut_3,
    "x_get_otlp_circuit_breaker__mutmut_4": x_get_otlp_circuit_breaker__mutmut_4,
    "x_get_otlp_circuit_breaker__mutmut_5": x_get_otlp_circuit_breaker__mutmut_5,
    "x_get_otlp_circuit_breaker__mutmut_6": x_get_otlp_circuit_breaker__mutmut_6,
    "x_get_otlp_circuit_breaker__mutmut_7": x_get_otlp_circuit_breaker__mutmut_7,
    "x_get_otlp_circuit_breaker__mutmut_8": x_get_otlp_circuit_breaker__mutmut_8,
    "x_get_otlp_circuit_breaker__mutmut_9": x_get_otlp_circuit_breaker__mutmut_9,
    "x_get_otlp_circuit_breaker__mutmut_10": x_get_otlp_circuit_breaker__mutmut_10,
    "x_get_otlp_circuit_breaker__mutmut_11": x_get_otlp_circuit_breaker__mutmut_11,
    "x_get_otlp_circuit_breaker__mutmut_12": x_get_otlp_circuit_breaker__mutmut_12,
}


def get_otlp_circuit_breaker(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_otlp_circuit_breaker__mutmut_orig, x_get_otlp_circuit_breaker__mutmut_mutants, args, kwargs
    )
    return result


get_otlp_circuit_breaker.__signature__ = _mutmut_signature(x_get_otlp_circuit_breaker__mutmut_orig)
x_get_otlp_circuit_breaker__mutmut_orig.__name__ = "x_get_otlp_circuit_breaker"


def x_reset_otlp_circuit_breaker__mutmut_orig() -> None:
    """Reset the global circuit breaker (primarily for testing)."""
    global _otlp_circuit_breaker

    with _circuit_breaker_lock:
        if _otlp_circuit_breaker is not None:
            _otlp_circuit_breaker.reset()


def x_reset_otlp_circuit_breaker__mutmut_1() -> None:
    """Reset the global circuit breaker (primarily for testing)."""
    global _otlp_circuit_breaker

    with _circuit_breaker_lock:
        if _otlp_circuit_breaker is None:
            _otlp_circuit_breaker.reset()


x_reset_otlp_circuit_breaker__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_otlp_circuit_breaker__mutmut_1": x_reset_otlp_circuit_breaker__mutmut_1
}


def reset_otlp_circuit_breaker(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_otlp_circuit_breaker__mutmut_orig, x_reset_otlp_circuit_breaker__mutmut_mutants, args, kwargs
    )
    return result


reset_otlp_circuit_breaker.__signature__ = _mutmut_signature(x_reset_otlp_circuit_breaker__mutmut_orig)
x_reset_otlp_circuit_breaker__mutmut_orig.__name__ = "x_reset_otlp_circuit_breaker"


__all__ = [
    "OTLPCircuitBreaker",
    "get_otlp_circuit_breaker",
    "reset_otlp_circuit_breaker",
]


# <3 🧱🤝🔌🪄
