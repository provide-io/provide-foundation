# provide/foundation/logger/ratelimit/limiters.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# limiters.py
#
import asyncio
import threading
import time
from typing import Any

"""Rate limiter implementations for Foundation's logging system."""
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


class SyncRateLimiter:
    """Synchronous token bucket rate limiter for controlling log output rates.
    Thread-safe implementation suitable for synchronous logging operations.
    """

    def xǁSyncRateLimiterǁ__init____mutmut_orig(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_1(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity < 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_2(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 1:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_3(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError(None)
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_4(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("XXCapacity must be positiveXX")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_5(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_6(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("CAPACITY MUST BE POSITIVE")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_7(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate < 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_8(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 1:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_9(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError(None)

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_10(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("XXRefill rate must be positiveXX")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_11(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_12(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("REFILL RATE MUST BE POSITIVE")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_13(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = None
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_14(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(None)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_15(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = None
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_16(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(None)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_17(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = None
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_18(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(None)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_19(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = None
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_20(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = None

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_21(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = None
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_22(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 1
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_23(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = None
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_24(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 1
        self.last_denied_time: float | None = None

    def xǁSyncRateLimiterǁ__init____mutmut_25(self, capacity: float, refill_rate: float) -> None:
        """Initialize the rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = ""
    
    xǁSyncRateLimiterǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSyncRateLimiterǁ__init____mutmut_1': xǁSyncRateLimiterǁ__init____mutmut_1, 
        'xǁSyncRateLimiterǁ__init____mutmut_2': xǁSyncRateLimiterǁ__init____mutmut_2, 
        'xǁSyncRateLimiterǁ__init____mutmut_3': xǁSyncRateLimiterǁ__init____mutmut_3, 
        'xǁSyncRateLimiterǁ__init____mutmut_4': xǁSyncRateLimiterǁ__init____mutmut_4, 
        'xǁSyncRateLimiterǁ__init____mutmut_5': xǁSyncRateLimiterǁ__init____mutmut_5, 
        'xǁSyncRateLimiterǁ__init____mutmut_6': xǁSyncRateLimiterǁ__init____mutmut_6, 
        'xǁSyncRateLimiterǁ__init____mutmut_7': xǁSyncRateLimiterǁ__init____mutmut_7, 
        'xǁSyncRateLimiterǁ__init____mutmut_8': xǁSyncRateLimiterǁ__init____mutmut_8, 
        'xǁSyncRateLimiterǁ__init____mutmut_9': xǁSyncRateLimiterǁ__init____mutmut_9, 
        'xǁSyncRateLimiterǁ__init____mutmut_10': xǁSyncRateLimiterǁ__init____mutmut_10, 
        'xǁSyncRateLimiterǁ__init____mutmut_11': xǁSyncRateLimiterǁ__init____mutmut_11, 
        'xǁSyncRateLimiterǁ__init____mutmut_12': xǁSyncRateLimiterǁ__init____mutmut_12, 
        'xǁSyncRateLimiterǁ__init____mutmut_13': xǁSyncRateLimiterǁ__init____mutmut_13, 
        'xǁSyncRateLimiterǁ__init____mutmut_14': xǁSyncRateLimiterǁ__init____mutmut_14, 
        'xǁSyncRateLimiterǁ__init____mutmut_15': xǁSyncRateLimiterǁ__init____mutmut_15, 
        'xǁSyncRateLimiterǁ__init____mutmut_16': xǁSyncRateLimiterǁ__init____mutmut_16, 
        'xǁSyncRateLimiterǁ__init____mutmut_17': xǁSyncRateLimiterǁ__init____mutmut_17, 
        'xǁSyncRateLimiterǁ__init____mutmut_18': xǁSyncRateLimiterǁ__init____mutmut_18, 
        'xǁSyncRateLimiterǁ__init____mutmut_19': xǁSyncRateLimiterǁ__init____mutmut_19, 
        'xǁSyncRateLimiterǁ__init____mutmut_20': xǁSyncRateLimiterǁ__init____mutmut_20, 
        'xǁSyncRateLimiterǁ__init____mutmut_21': xǁSyncRateLimiterǁ__init____mutmut_21, 
        'xǁSyncRateLimiterǁ__init____mutmut_22': xǁSyncRateLimiterǁ__init____mutmut_22, 
        'xǁSyncRateLimiterǁ__init____mutmut_23': xǁSyncRateLimiterǁ__init____mutmut_23, 
        'xǁSyncRateLimiterǁ__init____mutmut_24': xǁSyncRateLimiterǁ__init____mutmut_24, 
        'xǁSyncRateLimiterǁ__init____mutmut_25': xǁSyncRateLimiterǁ__init____mutmut_25
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSyncRateLimiterǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSyncRateLimiterǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSyncRateLimiterǁ__init____mutmut_orig)
    xǁSyncRateLimiterǁ__init____mutmut_orig.__name__ = 'xǁSyncRateLimiterǁ__init__'

    def xǁSyncRateLimiterǁis_allowed__mutmut_orig(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_1(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = None
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_2(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = None

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_3(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now + self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_4(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed >= 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_5(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 1:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_6(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = None
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_7(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed / self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_8(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = None
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_9(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(None, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_10(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, None)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_11(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_12(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, )
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_13(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens - tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_14(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = None

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_15(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens > 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_16(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 2.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_17(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens = 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_18(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens += 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_19(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 2.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_20(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed = 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_21(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed -= 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_22(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 2
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_23(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return False
            self.total_denied += 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_24(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied = 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_25(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied -= 1
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_26(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 2
            self.last_denied_time = now
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_27(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = None
            return False

    def xǁSyncRateLimiterǁis_allowed__mutmut_28(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return True
    
    xǁSyncRateLimiterǁis_allowed__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSyncRateLimiterǁis_allowed__mutmut_1': xǁSyncRateLimiterǁis_allowed__mutmut_1, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_2': xǁSyncRateLimiterǁis_allowed__mutmut_2, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_3': xǁSyncRateLimiterǁis_allowed__mutmut_3, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_4': xǁSyncRateLimiterǁis_allowed__mutmut_4, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_5': xǁSyncRateLimiterǁis_allowed__mutmut_5, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_6': xǁSyncRateLimiterǁis_allowed__mutmut_6, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_7': xǁSyncRateLimiterǁis_allowed__mutmut_7, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_8': xǁSyncRateLimiterǁis_allowed__mutmut_8, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_9': xǁSyncRateLimiterǁis_allowed__mutmut_9, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_10': xǁSyncRateLimiterǁis_allowed__mutmut_10, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_11': xǁSyncRateLimiterǁis_allowed__mutmut_11, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_12': xǁSyncRateLimiterǁis_allowed__mutmut_12, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_13': xǁSyncRateLimiterǁis_allowed__mutmut_13, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_14': xǁSyncRateLimiterǁis_allowed__mutmut_14, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_15': xǁSyncRateLimiterǁis_allowed__mutmut_15, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_16': xǁSyncRateLimiterǁis_allowed__mutmut_16, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_17': xǁSyncRateLimiterǁis_allowed__mutmut_17, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_18': xǁSyncRateLimiterǁis_allowed__mutmut_18, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_19': xǁSyncRateLimiterǁis_allowed__mutmut_19, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_20': xǁSyncRateLimiterǁis_allowed__mutmut_20, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_21': xǁSyncRateLimiterǁis_allowed__mutmut_21, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_22': xǁSyncRateLimiterǁis_allowed__mutmut_22, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_23': xǁSyncRateLimiterǁis_allowed__mutmut_23, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_24': xǁSyncRateLimiterǁis_allowed__mutmut_24, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_25': xǁSyncRateLimiterǁis_allowed__mutmut_25, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_26': xǁSyncRateLimiterǁis_allowed__mutmut_26, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_27': xǁSyncRateLimiterǁis_allowed__mutmut_27, 
        'xǁSyncRateLimiterǁis_allowed__mutmut_28': xǁSyncRateLimiterǁis_allowed__mutmut_28
    }
    
    def is_allowed(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSyncRateLimiterǁis_allowed__mutmut_orig"), object.__getattribute__(self, "xǁSyncRateLimiterǁis_allowed__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_allowed.__signature__ = _mutmut_signature(xǁSyncRateLimiterǁis_allowed__mutmut_orig)
    xǁSyncRateLimiterǁis_allowed__mutmut_orig.__name__ = 'xǁSyncRateLimiterǁis_allowed'

    def xǁSyncRateLimiterǁget_stats__mutmut_orig(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self.lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    def xǁSyncRateLimiterǁget_stats__mutmut_1(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self.lock:
            return {
                "XXtokens_availableXX": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    def xǁSyncRateLimiterǁget_stats__mutmut_2(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self.lock:
            return {
                "TOKENS_AVAILABLE": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    def xǁSyncRateLimiterǁget_stats__mutmut_3(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self.lock:
            return {
                "tokens_available": self.tokens,
                "XXcapacityXX": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    def xǁSyncRateLimiterǁget_stats__mutmut_4(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self.lock:
            return {
                "tokens_available": self.tokens,
                "CAPACITY": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    def xǁSyncRateLimiterǁget_stats__mutmut_5(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self.lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "XXrefill_rateXX": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    def xǁSyncRateLimiterǁget_stats__mutmut_6(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self.lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "REFILL_RATE": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    def xǁSyncRateLimiterǁget_stats__mutmut_7(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self.lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "XXtotal_allowedXX": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    def xǁSyncRateLimiterǁget_stats__mutmut_8(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self.lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "TOTAL_ALLOWED": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    def xǁSyncRateLimiterǁget_stats__mutmut_9(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self.lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "XXtotal_deniedXX": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    def xǁSyncRateLimiterǁget_stats__mutmut_10(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self.lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "TOTAL_DENIED": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    def xǁSyncRateLimiterǁget_stats__mutmut_11(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self.lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "XXlast_denied_timeXX": self.last_denied_time,
            }

    def xǁSyncRateLimiterǁget_stats__mutmut_12(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self.lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "LAST_DENIED_TIME": self.last_denied_time,
            }
    
    xǁSyncRateLimiterǁget_stats__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSyncRateLimiterǁget_stats__mutmut_1': xǁSyncRateLimiterǁget_stats__mutmut_1, 
        'xǁSyncRateLimiterǁget_stats__mutmut_2': xǁSyncRateLimiterǁget_stats__mutmut_2, 
        'xǁSyncRateLimiterǁget_stats__mutmut_3': xǁSyncRateLimiterǁget_stats__mutmut_3, 
        'xǁSyncRateLimiterǁget_stats__mutmut_4': xǁSyncRateLimiterǁget_stats__mutmut_4, 
        'xǁSyncRateLimiterǁget_stats__mutmut_5': xǁSyncRateLimiterǁget_stats__mutmut_5, 
        'xǁSyncRateLimiterǁget_stats__mutmut_6': xǁSyncRateLimiterǁget_stats__mutmut_6, 
        'xǁSyncRateLimiterǁget_stats__mutmut_7': xǁSyncRateLimiterǁget_stats__mutmut_7, 
        'xǁSyncRateLimiterǁget_stats__mutmut_8': xǁSyncRateLimiterǁget_stats__mutmut_8, 
        'xǁSyncRateLimiterǁget_stats__mutmut_9': xǁSyncRateLimiterǁget_stats__mutmut_9, 
        'xǁSyncRateLimiterǁget_stats__mutmut_10': xǁSyncRateLimiterǁget_stats__mutmut_10, 
        'xǁSyncRateLimiterǁget_stats__mutmut_11': xǁSyncRateLimiterǁget_stats__mutmut_11, 
        'xǁSyncRateLimiterǁget_stats__mutmut_12': xǁSyncRateLimiterǁget_stats__mutmut_12
    }
    
    def get_stats(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSyncRateLimiterǁget_stats__mutmut_orig"), object.__getattribute__(self, "xǁSyncRateLimiterǁget_stats__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_stats.__signature__ = _mutmut_signature(xǁSyncRateLimiterǁget_stats__mutmut_orig)
    xǁSyncRateLimiterǁget_stats__mutmut_orig.__name__ = 'xǁSyncRateLimiterǁget_stats'


class AsyncRateLimiter:
    """Asynchronous token bucket rate limiter.
    Uses asyncio.Lock for thread safety in async contexts.
    """

    def xǁAsyncRateLimiterǁ__init____mutmut_orig(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_1(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity < 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_2(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 1:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_3(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError(None)
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_4(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("XXCapacity must be positiveXX")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_5(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_6(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("CAPACITY MUST BE POSITIVE")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_7(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate < 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_8(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 1:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_9(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError(None)

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_10(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("XXRefill rate must be positiveXX")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_11(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_12(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("REFILL RATE MUST BE POSITIVE")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_13(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = None
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_14(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(None)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_15(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = None
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_16(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(None)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_17(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = None
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_18(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(None)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_19(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = None
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_20(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = None

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_21(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = None
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_22(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 1
        self.total_denied = 0
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_23(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = None
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_24(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 1
        self.last_denied_time: float | None = None

    def xǁAsyncRateLimiterǁ__init____mutmut_25(self, capacity: float, refill_rate: float) -> None:
        """Initialize the async rate limiter.

        Args:
            capacity: Maximum number of tokens (burst capacity)
            refill_rate: Tokens refilled per second

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

        # Track statistics
        self.total_allowed = 0
        self.total_denied = 0
        self.last_denied_time: float | None = ""
    
    xǁAsyncRateLimiterǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAsyncRateLimiterǁ__init____mutmut_1': xǁAsyncRateLimiterǁ__init____mutmut_1, 
        'xǁAsyncRateLimiterǁ__init____mutmut_2': xǁAsyncRateLimiterǁ__init____mutmut_2, 
        'xǁAsyncRateLimiterǁ__init____mutmut_3': xǁAsyncRateLimiterǁ__init____mutmut_3, 
        'xǁAsyncRateLimiterǁ__init____mutmut_4': xǁAsyncRateLimiterǁ__init____mutmut_4, 
        'xǁAsyncRateLimiterǁ__init____mutmut_5': xǁAsyncRateLimiterǁ__init____mutmut_5, 
        'xǁAsyncRateLimiterǁ__init____mutmut_6': xǁAsyncRateLimiterǁ__init____mutmut_6, 
        'xǁAsyncRateLimiterǁ__init____mutmut_7': xǁAsyncRateLimiterǁ__init____mutmut_7, 
        'xǁAsyncRateLimiterǁ__init____mutmut_8': xǁAsyncRateLimiterǁ__init____mutmut_8, 
        'xǁAsyncRateLimiterǁ__init____mutmut_9': xǁAsyncRateLimiterǁ__init____mutmut_9, 
        'xǁAsyncRateLimiterǁ__init____mutmut_10': xǁAsyncRateLimiterǁ__init____mutmut_10, 
        'xǁAsyncRateLimiterǁ__init____mutmut_11': xǁAsyncRateLimiterǁ__init____mutmut_11, 
        'xǁAsyncRateLimiterǁ__init____mutmut_12': xǁAsyncRateLimiterǁ__init____mutmut_12, 
        'xǁAsyncRateLimiterǁ__init____mutmut_13': xǁAsyncRateLimiterǁ__init____mutmut_13, 
        'xǁAsyncRateLimiterǁ__init____mutmut_14': xǁAsyncRateLimiterǁ__init____mutmut_14, 
        'xǁAsyncRateLimiterǁ__init____mutmut_15': xǁAsyncRateLimiterǁ__init____mutmut_15, 
        'xǁAsyncRateLimiterǁ__init____mutmut_16': xǁAsyncRateLimiterǁ__init____mutmut_16, 
        'xǁAsyncRateLimiterǁ__init____mutmut_17': xǁAsyncRateLimiterǁ__init____mutmut_17, 
        'xǁAsyncRateLimiterǁ__init____mutmut_18': xǁAsyncRateLimiterǁ__init____mutmut_18, 
        'xǁAsyncRateLimiterǁ__init____mutmut_19': xǁAsyncRateLimiterǁ__init____mutmut_19, 
        'xǁAsyncRateLimiterǁ__init____mutmut_20': xǁAsyncRateLimiterǁ__init____mutmut_20, 
        'xǁAsyncRateLimiterǁ__init____mutmut_21': xǁAsyncRateLimiterǁ__init____mutmut_21, 
        'xǁAsyncRateLimiterǁ__init____mutmut_22': xǁAsyncRateLimiterǁ__init____mutmut_22, 
        'xǁAsyncRateLimiterǁ__init____mutmut_23': xǁAsyncRateLimiterǁ__init____mutmut_23, 
        'xǁAsyncRateLimiterǁ__init____mutmut_24': xǁAsyncRateLimiterǁ__init____mutmut_24, 
        'xǁAsyncRateLimiterǁ__init____mutmut_25': xǁAsyncRateLimiterǁ__init____mutmut_25
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAsyncRateLimiterǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAsyncRateLimiterǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁAsyncRateLimiterǁ__init____mutmut_orig)
    xǁAsyncRateLimiterǁ__init____mutmut_orig.__name__ = 'xǁAsyncRateLimiterǁ__init__'

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_orig(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_1(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = None
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_2(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = None

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_3(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now + self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_4(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed >= 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_5(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 1:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_6(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = None
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_7(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed / self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_8(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = None
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_9(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(None, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_10(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, None)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_11(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_12(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, )
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_13(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens - tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_14(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = None

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_15(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens > 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_16(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 2.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_17(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens = 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_18(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens += 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_19(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 2.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_20(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed = 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_21(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed -= 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_22(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 2
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_23(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return False
            self.total_denied += 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_24(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied = 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_25(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied -= 1
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_26(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 2
            self.last_denied_time = now
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_27(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = None
            return False

    async def xǁAsyncRateLimiterǁis_allowed__mutmut_28(self) -> bool:
        """Check if a log message is allowed based on available tokens.

        Returns:
            True if the log should be allowed, False if rate limited

        """
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            if elapsed > 0:
                tokens_to_add = elapsed * self.refill_rate
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill = now

            # Try to consume a token
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                self.total_allowed += 1
                return True
            self.total_denied += 1
            self.last_denied_time = now
            return True
    
    xǁAsyncRateLimiterǁis_allowed__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAsyncRateLimiterǁis_allowed__mutmut_1': xǁAsyncRateLimiterǁis_allowed__mutmut_1, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_2': xǁAsyncRateLimiterǁis_allowed__mutmut_2, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_3': xǁAsyncRateLimiterǁis_allowed__mutmut_3, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_4': xǁAsyncRateLimiterǁis_allowed__mutmut_4, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_5': xǁAsyncRateLimiterǁis_allowed__mutmut_5, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_6': xǁAsyncRateLimiterǁis_allowed__mutmut_6, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_7': xǁAsyncRateLimiterǁis_allowed__mutmut_7, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_8': xǁAsyncRateLimiterǁis_allowed__mutmut_8, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_9': xǁAsyncRateLimiterǁis_allowed__mutmut_9, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_10': xǁAsyncRateLimiterǁis_allowed__mutmut_10, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_11': xǁAsyncRateLimiterǁis_allowed__mutmut_11, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_12': xǁAsyncRateLimiterǁis_allowed__mutmut_12, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_13': xǁAsyncRateLimiterǁis_allowed__mutmut_13, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_14': xǁAsyncRateLimiterǁis_allowed__mutmut_14, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_15': xǁAsyncRateLimiterǁis_allowed__mutmut_15, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_16': xǁAsyncRateLimiterǁis_allowed__mutmut_16, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_17': xǁAsyncRateLimiterǁis_allowed__mutmut_17, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_18': xǁAsyncRateLimiterǁis_allowed__mutmut_18, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_19': xǁAsyncRateLimiterǁis_allowed__mutmut_19, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_20': xǁAsyncRateLimiterǁis_allowed__mutmut_20, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_21': xǁAsyncRateLimiterǁis_allowed__mutmut_21, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_22': xǁAsyncRateLimiterǁis_allowed__mutmut_22, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_23': xǁAsyncRateLimiterǁis_allowed__mutmut_23, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_24': xǁAsyncRateLimiterǁis_allowed__mutmut_24, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_25': xǁAsyncRateLimiterǁis_allowed__mutmut_25, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_26': xǁAsyncRateLimiterǁis_allowed__mutmut_26, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_27': xǁAsyncRateLimiterǁis_allowed__mutmut_27, 
        'xǁAsyncRateLimiterǁis_allowed__mutmut_28': xǁAsyncRateLimiterǁis_allowed__mutmut_28
    }
    
    def is_allowed(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAsyncRateLimiterǁis_allowed__mutmut_orig"), object.__getattribute__(self, "xǁAsyncRateLimiterǁis_allowed__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_allowed.__signature__ = _mutmut_signature(xǁAsyncRateLimiterǁis_allowed__mutmut_orig)
    xǁAsyncRateLimiterǁis_allowed__mutmut_orig.__name__ = 'xǁAsyncRateLimiterǁis_allowed'

    async def xǁAsyncRateLimiterǁget_stats__mutmut_orig(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        async with self._lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    async def xǁAsyncRateLimiterǁget_stats__mutmut_1(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        async with self._lock:
            return {
                "XXtokens_availableXX": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    async def xǁAsyncRateLimiterǁget_stats__mutmut_2(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        async with self._lock:
            return {
                "TOKENS_AVAILABLE": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    async def xǁAsyncRateLimiterǁget_stats__mutmut_3(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        async with self._lock:
            return {
                "tokens_available": self.tokens,
                "XXcapacityXX": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    async def xǁAsyncRateLimiterǁget_stats__mutmut_4(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        async with self._lock:
            return {
                "tokens_available": self.tokens,
                "CAPACITY": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    async def xǁAsyncRateLimiterǁget_stats__mutmut_5(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        async with self._lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "XXrefill_rateXX": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    async def xǁAsyncRateLimiterǁget_stats__mutmut_6(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        async with self._lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "REFILL_RATE": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    async def xǁAsyncRateLimiterǁget_stats__mutmut_7(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        async with self._lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "XXtotal_allowedXX": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    async def xǁAsyncRateLimiterǁget_stats__mutmut_8(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        async with self._lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "TOTAL_ALLOWED": self.total_allowed,
                "total_denied": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    async def xǁAsyncRateLimiterǁget_stats__mutmut_9(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        async with self._lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "XXtotal_deniedXX": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    async def xǁAsyncRateLimiterǁget_stats__mutmut_10(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        async with self._lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "TOTAL_DENIED": self.total_denied,
                "last_denied_time": self.last_denied_time,
            }

    async def xǁAsyncRateLimiterǁget_stats__mutmut_11(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        async with self._lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "XXlast_denied_timeXX": self.last_denied_time,
            }

    async def xǁAsyncRateLimiterǁget_stats__mutmut_12(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        async with self._lock:
            return {
                "tokens_available": self.tokens,
                "capacity": self.capacity,
                "refill_rate": self.refill_rate,
                "total_allowed": self.total_allowed,
                "total_denied": self.total_denied,
                "LAST_DENIED_TIME": self.last_denied_time,
            }
    
    xǁAsyncRateLimiterǁget_stats__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAsyncRateLimiterǁget_stats__mutmut_1': xǁAsyncRateLimiterǁget_stats__mutmut_1, 
        'xǁAsyncRateLimiterǁget_stats__mutmut_2': xǁAsyncRateLimiterǁget_stats__mutmut_2, 
        'xǁAsyncRateLimiterǁget_stats__mutmut_3': xǁAsyncRateLimiterǁget_stats__mutmut_3, 
        'xǁAsyncRateLimiterǁget_stats__mutmut_4': xǁAsyncRateLimiterǁget_stats__mutmut_4, 
        'xǁAsyncRateLimiterǁget_stats__mutmut_5': xǁAsyncRateLimiterǁget_stats__mutmut_5, 
        'xǁAsyncRateLimiterǁget_stats__mutmut_6': xǁAsyncRateLimiterǁget_stats__mutmut_6, 
        'xǁAsyncRateLimiterǁget_stats__mutmut_7': xǁAsyncRateLimiterǁget_stats__mutmut_7, 
        'xǁAsyncRateLimiterǁget_stats__mutmut_8': xǁAsyncRateLimiterǁget_stats__mutmut_8, 
        'xǁAsyncRateLimiterǁget_stats__mutmut_9': xǁAsyncRateLimiterǁget_stats__mutmut_9, 
        'xǁAsyncRateLimiterǁget_stats__mutmut_10': xǁAsyncRateLimiterǁget_stats__mutmut_10, 
        'xǁAsyncRateLimiterǁget_stats__mutmut_11': xǁAsyncRateLimiterǁget_stats__mutmut_11, 
        'xǁAsyncRateLimiterǁget_stats__mutmut_12': xǁAsyncRateLimiterǁget_stats__mutmut_12
    }
    
    def get_stats(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAsyncRateLimiterǁget_stats__mutmut_orig"), object.__getattribute__(self, "xǁAsyncRateLimiterǁget_stats__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_stats.__signature__ = _mutmut_signature(xǁAsyncRateLimiterǁget_stats__mutmut_orig)
    xǁAsyncRateLimiterǁget_stats__mutmut_orig.__name__ = 'xǁAsyncRateLimiterǁget_stats'


class GlobalRateLimiter:
    """Global rate limiter singleton for Foundation's logging system.
    Manages per-logger and global rate limits.
    """

    _instance = None
    _lock = threading.Lock()
    _initialized: bool

    def __new__(cls) -> GlobalRateLimiter:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def xǁGlobalRateLimiterǁ__init____mutmut_orig(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = "drop_oldest"

    def xǁGlobalRateLimiterǁ__init____mutmut_1(self) -> None:
        if self._initialized:
            return

        self._initialized = None
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = "drop_oldest"

    def xǁGlobalRateLimiterǁ__init____mutmut_2(self) -> None:
        if self._initialized:
            return

        self._initialized = False
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = "drop_oldest"

    def xǁGlobalRateLimiterǁ__init____mutmut_3(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = ""
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = "drop_oldest"

    def xǁGlobalRateLimiterǁ__init____mutmut_4(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = None
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = "drop_oldest"

    def xǁGlobalRateLimiterǁ__init____mutmut_5(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = None

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = "drop_oldest"

    def xǁGlobalRateLimiterǁ__init____mutmut_6(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = ""
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = "drop_oldest"

    def xǁGlobalRateLimiterǁ__init____mutmut_7(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = ""
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = "drop_oldest"

    def xǁGlobalRateLimiterǁ__init____mutmut_8(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = None

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = "drop_oldest"

    def xǁGlobalRateLimiterǁ__init____mutmut_9(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = None
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = "drop_oldest"

    def xǁGlobalRateLimiterǁ__init____mutmut_10(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = True
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = "drop_oldest"

    def xǁGlobalRateLimiterǁ__init____mutmut_11(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = None
        self.max_memory_mb: float | None = None
        self.overflow_policy = "drop_oldest"

    def xǁGlobalRateLimiterǁ__init____mutmut_12(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1001
        self.max_memory_mb: float | None = None
        self.overflow_policy = "drop_oldest"

    def xǁGlobalRateLimiterǁ__init____mutmut_13(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = ""
        self.overflow_policy = "drop_oldest"

    def xǁGlobalRateLimiterǁ__init____mutmut_14(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = None

    def xǁGlobalRateLimiterǁ__init____mutmut_15(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = "XXdrop_oldestXX"

    def xǁGlobalRateLimiterǁ__init____mutmut_16(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        self.global_limiter: Any = None
        self.logger_limiters: dict[str, SyncRateLimiter] = {}
        self.lock = threading.Lock()

        # Default configuration (can be overridden)
        self.global_rate: float | None = None
        self.global_capacity: float | None = None
        self.per_logger_rates: dict[str, tuple[float, float]] = {}

        # Queue configuration
        self.use_buffered = False
        self.max_queue_size = 1000
        self.max_memory_mb: float | None = None
        self.overflow_policy = "DROP_OLDEST"
    
    xǁGlobalRateLimiterǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGlobalRateLimiterǁ__init____mutmut_1': xǁGlobalRateLimiterǁ__init____mutmut_1, 
        'xǁGlobalRateLimiterǁ__init____mutmut_2': xǁGlobalRateLimiterǁ__init____mutmut_2, 
        'xǁGlobalRateLimiterǁ__init____mutmut_3': xǁGlobalRateLimiterǁ__init____mutmut_3, 
        'xǁGlobalRateLimiterǁ__init____mutmut_4': xǁGlobalRateLimiterǁ__init____mutmut_4, 
        'xǁGlobalRateLimiterǁ__init____mutmut_5': xǁGlobalRateLimiterǁ__init____mutmut_5, 
        'xǁGlobalRateLimiterǁ__init____mutmut_6': xǁGlobalRateLimiterǁ__init____mutmut_6, 
        'xǁGlobalRateLimiterǁ__init____mutmut_7': xǁGlobalRateLimiterǁ__init____mutmut_7, 
        'xǁGlobalRateLimiterǁ__init____mutmut_8': xǁGlobalRateLimiterǁ__init____mutmut_8, 
        'xǁGlobalRateLimiterǁ__init____mutmut_9': xǁGlobalRateLimiterǁ__init____mutmut_9, 
        'xǁGlobalRateLimiterǁ__init____mutmut_10': xǁGlobalRateLimiterǁ__init____mutmut_10, 
        'xǁGlobalRateLimiterǁ__init____mutmut_11': xǁGlobalRateLimiterǁ__init____mutmut_11, 
        'xǁGlobalRateLimiterǁ__init____mutmut_12': xǁGlobalRateLimiterǁ__init____mutmut_12, 
        'xǁGlobalRateLimiterǁ__init____mutmut_13': xǁGlobalRateLimiterǁ__init____mutmut_13, 
        'xǁGlobalRateLimiterǁ__init____mutmut_14': xǁGlobalRateLimiterǁ__init____mutmut_14, 
        'xǁGlobalRateLimiterǁ__init____mutmut_15': xǁGlobalRateLimiterǁ__init____mutmut_15, 
        'xǁGlobalRateLimiterǁ__init____mutmut_16': xǁGlobalRateLimiterǁ__init____mutmut_16
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGlobalRateLimiterǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁGlobalRateLimiterǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁGlobalRateLimiterǁ__init____mutmut_orig)
    xǁGlobalRateLimiterǁ__init____mutmut_orig.__name__ = 'xǁGlobalRateLimiterǁ__init__'

    def xǁGlobalRateLimiterǁconfigure__mutmut_orig(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_1(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = True,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_2(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1001,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_3(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "XXdrop_oldestXX",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_4(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "DROP_OLDEST",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_5(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = None
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_6(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = None
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_7(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = None
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_8(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = None

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_9(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None or global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_10(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_11(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_12(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = None
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_13(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = None

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_14(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = None
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_15(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=None,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_16(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=None,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_17(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=None,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_18(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=None,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_19(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_20(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_21(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_22(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_23(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=False,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_24(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = None

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_25(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(None, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_26(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, None)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_27(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_28(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, )

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_29(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = None
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_30(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = None

    def xǁGlobalRateLimiterǁconfigure__mutmut_31(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(None, rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_32(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, None)

    def xǁGlobalRateLimiterǁconfigure__mutmut_33(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(rate)

    def xǁGlobalRateLimiterǁconfigure__mutmut_34(
        self,
        global_rate: float | None = None,
        global_capacity: float | None = None,
        per_logger_rates: dict[str, tuple[float, float]] | None = None,
        use_buffered: bool = False,
        max_queue_size: int = 1000,
        max_memory_mb: float | None = None,
        overflow_policy: str = "drop_oldest",
    ) -> None:
        """Configure the global rate limiter.

        Args:
            global_rate: Global logs per second limit
            global_capacity: Global burst capacity
            per_logger_rates: Dict of logger_name -> (rate, capacity) tuples
            use_buffered: Use buffered rate limiter with tracking
            max_queue_size: Maximum queue size for buffered limiter
            max_memory_mb: Maximum memory for buffered limiter
            overflow_policy: What to do when queue is full

        """
        with self.lock:
            self.use_buffered = use_buffered
            self.max_queue_size = max_queue_size
            self.max_memory_mb = max_memory_mb
            self.overflow_policy = overflow_policy

            if global_rate is not None and global_capacity is not None:
                self.global_rate = global_rate
                self.global_capacity = global_capacity

                if use_buffered:
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    self.global_limiter = BufferedRateLimiter(
                        capacity=global_capacity,
                        refill_rate=global_rate,
                        buffer_size=max_queue_size,
                        track_dropped=True,
                    )
                else:
                    self.global_limiter = SyncRateLimiter(global_capacity, global_rate)

            if per_logger_rates:
                self.per_logger_rates = per_logger_rates
                # Create rate limiters for configured loggers
                for logger_name, (rate, capacity) in per_logger_rates.items():
                    self.logger_limiters[logger_name] = SyncRateLimiter(capacity, )
    
    xǁGlobalRateLimiterǁconfigure__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGlobalRateLimiterǁconfigure__mutmut_1': xǁGlobalRateLimiterǁconfigure__mutmut_1, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_2': xǁGlobalRateLimiterǁconfigure__mutmut_2, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_3': xǁGlobalRateLimiterǁconfigure__mutmut_3, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_4': xǁGlobalRateLimiterǁconfigure__mutmut_4, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_5': xǁGlobalRateLimiterǁconfigure__mutmut_5, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_6': xǁGlobalRateLimiterǁconfigure__mutmut_6, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_7': xǁGlobalRateLimiterǁconfigure__mutmut_7, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_8': xǁGlobalRateLimiterǁconfigure__mutmut_8, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_9': xǁGlobalRateLimiterǁconfigure__mutmut_9, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_10': xǁGlobalRateLimiterǁconfigure__mutmut_10, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_11': xǁGlobalRateLimiterǁconfigure__mutmut_11, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_12': xǁGlobalRateLimiterǁconfigure__mutmut_12, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_13': xǁGlobalRateLimiterǁconfigure__mutmut_13, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_14': xǁGlobalRateLimiterǁconfigure__mutmut_14, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_15': xǁGlobalRateLimiterǁconfigure__mutmut_15, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_16': xǁGlobalRateLimiterǁconfigure__mutmut_16, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_17': xǁGlobalRateLimiterǁconfigure__mutmut_17, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_18': xǁGlobalRateLimiterǁconfigure__mutmut_18, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_19': xǁGlobalRateLimiterǁconfigure__mutmut_19, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_20': xǁGlobalRateLimiterǁconfigure__mutmut_20, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_21': xǁGlobalRateLimiterǁconfigure__mutmut_21, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_22': xǁGlobalRateLimiterǁconfigure__mutmut_22, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_23': xǁGlobalRateLimiterǁconfigure__mutmut_23, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_24': xǁGlobalRateLimiterǁconfigure__mutmut_24, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_25': xǁGlobalRateLimiterǁconfigure__mutmut_25, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_26': xǁGlobalRateLimiterǁconfigure__mutmut_26, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_27': xǁGlobalRateLimiterǁconfigure__mutmut_27, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_28': xǁGlobalRateLimiterǁconfigure__mutmut_28, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_29': xǁGlobalRateLimiterǁconfigure__mutmut_29, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_30': xǁGlobalRateLimiterǁconfigure__mutmut_30, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_31': xǁGlobalRateLimiterǁconfigure__mutmut_31, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_32': xǁGlobalRateLimiterǁconfigure__mutmut_32, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_33': xǁGlobalRateLimiterǁconfigure__mutmut_33, 
        'xǁGlobalRateLimiterǁconfigure__mutmut_34': xǁGlobalRateLimiterǁconfigure__mutmut_34
    }
    
    def configure(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGlobalRateLimiterǁconfigure__mutmut_orig"), object.__getattribute__(self, "xǁGlobalRateLimiterǁconfigure__mutmut_mutants"), args, kwargs, self)
        return result 
    
    configure.__signature__ = _mutmut_signature(xǁGlobalRateLimiterǁconfigure__mutmut_orig)
    xǁGlobalRateLimiterǁconfigure__mutmut_orig.__name__ = 'xǁGlobalRateLimiterǁconfigure'

    def xǁGlobalRateLimiterǁis_allowed__mutmut_orig(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_1(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters or not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_2(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name not in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_3(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_4(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return True, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_5(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = None
                        if not allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_6(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(None)
                        if not allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_7(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_8(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return True, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_9(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason and "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_10(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "XXGlobal rate limit exceededXX"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_11(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_12(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "GLOBAL RATE LIMIT EXCEEDED"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_13(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_14(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return True, "Global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_15(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "XXGlobal rate limit exceededXX"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_16(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "global rate limit exceeded"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_17(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "GLOBAL RATE LIMIT EXCEEDED"

            return True, None

    def xǁGlobalRateLimiterǁis_allowed__mutmut_18(self, logger_name: str, item: Any | None = None) -> tuple[bool, str | None]:
        """Check if a log from a specific logger is allowed.

        Args:
            logger_name: Name of the logger
            item: Optional item for buffered tracking

        Returns:
            Tuple of (allowed, reason) where reason is set if denied

        """
        with self.lock:
            # Check per-logger limit first
            if logger_name in self.logger_limiters and not self.logger_limiters[logger_name].is_allowed():
                return False, f"Logger '{logger_name}' rate limit exceeded"

            # Check global limit
            if self.global_limiter:
                if self.use_buffered:
                    # BufferedRateLimiter returns tuple
                    from provide.foundation.logger.ratelimit.queue_limiter import (
                        BufferedRateLimiter,
                    )

                    if isinstance(self.global_limiter, BufferedRateLimiter):
                        allowed, reason = self.global_limiter.is_allowed(item)
                        if not allowed:
                            return False, reason or "Global rate limit exceeded"
                # SyncRateLimiter returns bool
                elif not self.global_limiter.is_allowed():
                    return False, "Global rate limit exceeded"

            return False, None
    
    xǁGlobalRateLimiterǁis_allowed__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGlobalRateLimiterǁis_allowed__mutmut_1': xǁGlobalRateLimiterǁis_allowed__mutmut_1, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_2': xǁGlobalRateLimiterǁis_allowed__mutmut_2, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_3': xǁGlobalRateLimiterǁis_allowed__mutmut_3, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_4': xǁGlobalRateLimiterǁis_allowed__mutmut_4, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_5': xǁGlobalRateLimiterǁis_allowed__mutmut_5, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_6': xǁGlobalRateLimiterǁis_allowed__mutmut_6, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_7': xǁGlobalRateLimiterǁis_allowed__mutmut_7, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_8': xǁGlobalRateLimiterǁis_allowed__mutmut_8, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_9': xǁGlobalRateLimiterǁis_allowed__mutmut_9, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_10': xǁGlobalRateLimiterǁis_allowed__mutmut_10, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_11': xǁGlobalRateLimiterǁis_allowed__mutmut_11, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_12': xǁGlobalRateLimiterǁis_allowed__mutmut_12, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_13': xǁGlobalRateLimiterǁis_allowed__mutmut_13, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_14': xǁGlobalRateLimiterǁis_allowed__mutmut_14, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_15': xǁGlobalRateLimiterǁis_allowed__mutmut_15, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_16': xǁGlobalRateLimiterǁis_allowed__mutmut_16, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_17': xǁGlobalRateLimiterǁis_allowed__mutmut_17, 
        'xǁGlobalRateLimiterǁis_allowed__mutmut_18': xǁGlobalRateLimiterǁis_allowed__mutmut_18
    }
    
    def is_allowed(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGlobalRateLimiterǁis_allowed__mutmut_orig"), object.__getattribute__(self, "xǁGlobalRateLimiterǁis_allowed__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_allowed.__signature__ = _mutmut_signature(xǁGlobalRateLimiterǁis_allowed__mutmut_orig)
    xǁGlobalRateLimiterǁis_allowed__mutmut_orig.__name__ = 'xǁGlobalRateLimiterǁis_allowed'

    def xǁGlobalRateLimiterǁget_stats__mutmut_orig(self) -> dict[str, Any]:
        """Get comprehensive rate limiting statistics."""
        with self.lock:
            stats: dict[str, Any] = {
                "global": self.global_limiter.get_stats() if self.global_limiter else None,
                "per_logger": {},
            }

            for logger_name, limiter in self.logger_limiters.items():
                stats["per_logger"][logger_name] = limiter.get_stats()

            return stats

    def xǁGlobalRateLimiterǁget_stats__mutmut_1(self) -> dict[str, Any]:
        """Get comprehensive rate limiting statistics."""
        with self.lock:
            stats: dict[str, Any] = None

            for logger_name, limiter in self.logger_limiters.items():
                stats["per_logger"][logger_name] = limiter.get_stats()

            return stats

    def xǁGlobalRateLimiterǁget_stats__mutmut_2(self) -> dict[str, Any]:
        """Get comprehensive rate limiting statistics."""
        with self.lock:
            stats: dict[str, Any] = {
                "XXglobalXX": self.global_limiter.get_stats() if self.global_limiter else None,
                "per_logger": {},
            }

            for logger_name, limiter in self.logger_limiters.items():
                stats["per_logger"][logger_name] = limiter.get_stats()

            return stats

    def xǁGlobalRateLimiterǁget_stats__mutmut_3(self) -> dict[str, Any]:
        """Get comprehensive rate limiting statistics."""
        with self.lock:
            stats: dict[str, Any] = {
                "GLOBAL": self.global_limiter.get_stats() if self.global_limiter else None,
                "per_logger": {},
            }

            for logger_name, limiter in self.logger_limiters.items():
                stats["per_logger"][logger_name] = limiter.get_stats()

            return stats

    def xǁGlobalRateLimiterǁget_stats__mutmut_4(self) -> dict[str, Any]:
        """Get comprehensive rate limiting statistics."""
        with self.lock:
            stats: dict[str, Any] = {
                "global": self.global_limiter.get_stats() if self.global_limiter else None,
                "XXper_loggerXX": {},
            }

            for logger_name, limiter in self.logger_limiters.items():
                stats["per_logger"][logger_name] = limiter.get_stats()

            return stats

    def xǁGlobalRateLimiterǁget_stats__mutmut_5(self) -> dict[str, Any]:
        """Get comprehensive rate limiting statistics."""
        with self.lock:
            stats: dict[str, Any] = {
                "global": self.global_limiter.get_stats() if self.global_limiter else None,
                "PER_LOGGER": {},
            }

            for logger_name, limiter in self.logger_limiters.items():
                stats["per_logger"][logger_name] = limiter.get_stats()

            return stats

    def xǁGlobalRateLimiterǁget_stats__mutmut_6(self) -> dict[str, Any]:
        """Get comprehensive rate limiting statistics."""
        with self.lock:
            stats: dict[str, Any] = {
                "global": self.global_limiter.get_stats() if self.global_limiter else None,
                "per_logger": {},
            }

            for logger_name, limiter in self.logger_limiters.items():
                stats["per_logger"][logger_name] = None

            return stats

    def xǁGlobalRateLimiterǁget_stats__mutmut_7(self) -> dict[str, Any]:
        """Get comprehensive rate limiting statistics."""
        with self.lock:
            stats: dict[str, Any] = {
                "global": self.global_limiter.get_stats() if self.global_limiter else None,
                "per_logger": {},
            }

            for logger_name, limiter in self.logger_limiters.items():
                stats["XXper_loggerXX"][logger_name] = limiter.get_stats()

            return stats

    def xǁGlobalRateLimiterǁget_stats__mutmut_8(self) -> dict[str, Any]:
        """Get comprehensive rate limiting statistics."""
        with self.lock:
            stats: dict[str, Any] = {
                "global": self.global_limiter.get_stats() if self.global_limiter else None,
                "per_logger": {},
            }

            for logger_name, limiter in self.logger_limiters.items():
                stats["PER_LOGGER"][logger_name] = limiter.get_stats()

            return stats
    
    xǁGlobalRateLimiterǁget_stats__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGlobalRateLimiterǁget_stats__mutmut_1': xǁGlobalRateLimiterǁget_stats__mutmut_1, 
        'xǁGlobalRateLimiterǁget_stats__mutmut_2': xǁGlobalRateLimiterǁget_stats__mutmut_2, 
        'xǁGlobalRateLimiterǁget_stats__mutmut_3': xǁGlobalRateLimiterǁget_stats__mutmut_3, 
        'xǁGlobalRateLimiterǁget_stats__mutmut_4': xǁGlobalRateLimiterǁget_stats__mutmut_4, 
        'xǁGlobalRateLimiterǁget_stats__mutmut_5': xǁGlobalRateLimiterǁget_stats__mutmut_5, 
        'xǁGlobalRateLimiterǁget_stats__mutmut_6': xǁGlobalRateLimiterǁget_stats__mutmut_6, 
        'xǁGlobalRateLimiterǁget_stats__mutmut_7': xǁGlobalRateLimiterǁget_stats__mutmut_7, 
        'xǁGlobalRateLimiterǁget_stats__mutmut_8': xǁGlobalRateLimiterǁget_stats__mutmut_8
    }
    
    def get_stats(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGlobalRateLimiterǁget_stats__mutmut_orig"), object.__getattribute__(self, "xǁGlobalRateLimiterǁget_stats__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_stats.__signature__ = _mutmut_signature(xǁGlobalRateLimiterǁget_stats__mutmut_orig)
    xǁGlobalRateLimiterǁget_stats__mutmut_orig.__name__ = 'xǁGlobalRateLimiterǁget_stats'


# <3 🧱🤝📝🪄
