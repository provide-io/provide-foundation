# provide/foundation/transport/defaults.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

"""Transport defaults for Foundation configuration."""

# =================================
# Transport Defaults
# =================================
DEFAULT_TRANSPORT_TIMEOUT = 30.0
DEFAULT_TRANSPORT_MAX_RETRIES = 3
DEFAULT_TRANSPORT_RETRY_BACKOFF_FACTOR = 0.5
DEFAULT_TRANSPORT_VERIFY_SSL = True

# =================================
# HTTP Transport Defaults
# =================================
DEFAULT_HTTP_POOL_CONNECTIONS = 10
DEFAULT_HTTP_POOL_MAXSIZE = 100
DEFAULT_HTTP_FOLLOW_REDIRECTS = True
DEFAULT_HTTP_USE_HTTP2 = False
DEFAULT_HTTP_MAX_REDIRECTS = 5

# =================================
# Transport Middleware Defaults
# =================================
DEFAULT_TRANSPORT_LOG_REQUESTS = True
DEFAULT_TRANSPORT_LOG_RESPONSES = True
DEFAULT_TRANSPORT_LOG_BODIES = False

# =================================
# Transport Cache Defaults
# =================================
DEFAULT_TRANSPORT_FAILURE_THRESHOLD = 3

__all__ = [
    "DEFAULT_HTTP_FOLLOW_REDIRECTS",
    "DEFAULT_HTTP_MAX_REDIRECTS",
    "DEFAULT_HTTP_POOL_CONNECTIONS",
    "DEFAULT_HTTP_POOL_MAXSIZE",
    "DEFAULT_HTTP_USE_HTTP2",
    "DEFAULT_TRANSPORT_FAILURE_THRESHOLD",
    "DEFAULT_TRANSPORT_LOG_BODIES",
    "DEFAULT_TRANSPORT_LOG_REQUESTS",
    "DEFAULT_TRANSPORT_LOG_RESPONSES",
    "DEFAULT_TRANSPORT_MAX_RETRIES",
    "DEFAULT_TRANSPORT_RETRY_BACKOFF_FACTOR",
    "DEFAULT_TRANSPORT_TIMEOUT",
    "DEFAULT_TRANSPORT_VERIFY_SSL",
]
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


# <3 🧱🤝🚚🪄
