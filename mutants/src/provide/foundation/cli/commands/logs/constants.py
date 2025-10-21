# provide/foundation/cli/commands/logs/constants.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

"""Constants for log generation."""

# Cut-up phrases inspired by Burroughs
BURROUGHS_PHRASES = [
    "mutated Soft Machine prescribed within data stream",
    "pre-recorded talking asshole dissolved into under neon hum",
    "the viral Word carrying a new strain of reality",
    "memory banks spilling future-pasts onto the terminal floor",
    "the soft typewriter of the Other Half",
    "control mechanisms broadcast in reversed time signatures",
    "equations of control flickering on a broken monitor",
    "semantic disturbances in Sector 9",
    "the Biologic Courts passing sentence in a dream",
    "a thousand junk units screaming in unison",
    "frequency shift reported by Sector 5",
    "the algebra of need written in neural static",
]

# Service names
SERVICE_NAMES = [
    "api-gateway",
    "auth-service",
    "user-service",
    "payment-processor",
    "notification-service",
    "search-index",
    "cache-layer",
    "data-pipeline",
    "ml-inference",
    "report-generator",
    "webhook-handler",
    "queue-processor",
    "stream-analyzer",
    "batch-job",
    "cron-scheduler",
    "interzone-terminal",
    "nova-police",
    "reality-studio",
]

# Operations
OPERATIONS = [
    "process_request",
    "validate_input",
    "execute_query",
    "transform_data",
    "send_notification",
    "update_cache",
    "sync_state",
    "aggregate_metrics",
    "encode_response",
    "decode_request",
    "authorize_access",
    "refresh_token",
    "persist_data",
    "emit_event",
    "handle_error",
    "transmit_signal",
    "intercept_word",
    "decode_reality",
]

# Normal tech-style operations
NORMAL_OPERATIONS = [
    "processed",
    "validated",
    "executed",
    "transformed",
    "cached",
    "synced",
]

# Normal tech-style objects
NORMAL_OBJECTS = [
    "request",
    "query",
    "data",
    "event",
    "message",
    "transaction",
]

# Error codes
ERROR_CODES = [400, 404, 500, 503]

# Error types
ERROR_TYPES = [
    "ValidationError",
    "ServiceUnavailable",
    "TimeoutError",
    "DatabaseError",
    "RateLimitExceeded",
]

# Log levels for non-errors
NON_ERROR_LEVELS = ["debug", "info", "warning"]

# Domain values
DOMAINS = ["user", "system", "data", "api", None]

# Action values
ACTIONS = ["create", "read", "update", "delete", None]

# Status values
STATUSES = ["success", "pending", None]

# Duration range (milliseconds)
MIN_DURATION_MS = 10
MAX_DURATION_MS = 5000
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


# <3 🧱🤝💻🪄
