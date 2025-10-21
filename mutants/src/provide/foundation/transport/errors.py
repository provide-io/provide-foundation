# provide/foundation/transport/errors.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from provide.foundation.errors.base import FoundationError

"""Transport-specific error types."""

if TYPE_CHECKING:
    from provide.foundation.transport.base import Request, Response
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


class TransportError(FoundationError):
    """Base transport error."""

    def xǁTransportErrorǁ__init____mutmut_orig(self, message: str, *, request: Request | None = None, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.request = request

    def xǁTransportErrorǁ__init____mutmut_1(self, message: str, *, request: Request | None = None, **kwargs: Any) -> None:
        super().__init__(None, **kwargs)
        self.request = request

    def xǁTransportErrorǁ__init____mutmut_2(self, message: str, *, request: Request | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.request = request

    def xǁTransportErrorǁ__init____mutmut_3(self, message: str, *, request: Request | None = None, **kwargs: Any) -> None:
        super().__init__(message, )
        self.request = request

    def xǁTransportErrorǁ__init____mutmut_4(self, message: str, *, request: Request | None = None, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.request = None
    
    xǁTransportErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTransportErrorǁ__init____mutmut_1': xǁTransportErrorǁ__init____mutmut_1, 
        'xǁTransportErrorǁ__init____mutmut_2': xǁTransportErrorǁ__init____mutmut_2, 
        'xǁTransportErrorǁ__init____mutmut_3': xǁTransportErrorǁ__init____mutmut_3, 
        'xǁTransportErrorǁ__init____mutmut_4': xǁTransportErrorǁ__init____mutmut_4
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTransportErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁTransportErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁTransportErrorǁ__init____mutmut_orig)
    xǁTransportErrorǁ__init____mutmut_orig.__name__ = 'xǁTransportErrorǁ__init__'


class TransportConnectionError(TransportError):
    """Transport connection failed."""


class TransportTimeoutError(TransportError):
    """Transport request timed out."""


class HTTPResponseError(TransportError):
    """HTTP response error (4xx/5xx status codes)."""

    def xǁHTTPResponseErrorǁ__init____mutmut_orig(self, message: str, *, status_code: int, response: Response, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.status_code = status_code
        self.response = response

    def xǁHTTPResponseErrorǁ__init____mutmut_1(self, message: str, *, status_code: int, response: Response, **kwargs: Any) -> None:
        super().__init__(None, **kwargs)
        self.status_code = status_code
        self.response = response

    def xǁHTTPResponseErrorǁ__init____mutmut_2(self, message: str, *, status_code: int, response: Response, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.status_code = status_code
        self.response = response

    def xǁHTTPResponseErrorǁ__init____mutmut_3(self, message: str, *, status_code: int, response: Response, **kwargs: Any) -> None:
        super().__init__(message, )
        self.status_code = status_code
        self.response = response

    def xǁHTTPResponseErrorǁ__init____mutmut_4(self, message: str, *, status_code: int, response: Response, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.status_code = None
        self.response = response

    def xǁHTTPResponseErrorǁ__init____mutmut_5(self, message: str, *, status_code: int, response: Response, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.status_code = status_code
        self.response = None
    
    xǁHTTPResponseErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁHTTPResponseErrorǁ__init____mutmut_1': xǁHTTPResponseErrorǁ__init____mutmut_1, 
        'xǁHTTPResponseErrorǁ__init____mutmut_2': xǁHTTPResponseErrorǁ__init____mutmut_2, 
        'xǁHTTPResponseErrorǁ__init____mutmut_3': xǁHTTPResponseErrorǁ__init____mutmut_3, 
        'xǁHTTPResponseErrorǁ__init____mutmut_4': xǁHTTPResponseErrorǁ__init____mutmut_4, 
        'xǁHTTPResponseErrorǁ__init____mutmut_5': xǁHTTPResponseErrorǁ__init____mutmut_5
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁHTTPResponseErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁHTTPResponseErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁHTTPResponseErrorǁ__init____mutmut_orig)
    xǁHTTPResponseErrorǁ__init____mutmut_orig.__name__ = 'xǁHTTPResponseErrorǁ__init__'


class TransportConfigurationError(TransportError):
    """Transport configuration error."""


class TransportNotFoundError(TransportError):
    """No transport found for the given URI scheme."""

    def xǁTransportNotFoundErrorǁ__init____mutmut_orig(self, message: str, *, scheme: str, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.scheme = scheme

    def xǁTransportNotFoundErrorǁ__init____mutmut_1(self, message: str, *, scheme: str, **kwargs: Any) -> None:
        super().__init__(None, **kwargs)
        self.scheme = scheme

    def xǁTransportNotFoundErrorǁ__init____mutmut_2(self, message: str, *, scheme: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.scheme = scheme

    def xǁTransportNotFoundErrorǁ__init____mutmut_3(self, message: str, *, scheme: str, **kwargs: Any) -> None:
        super().__init__(message, )
        self.scheme = scheme

    def xǁTransportNotFoundErrorǁ__init____mutmut_4(self, message: str, *, scheme: str, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.scheme = None
    
    xǁTransportNotFoundErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTransportNotFoundErrorǁ__init____mutmut_1': xǁTransportNotFoundErrorǁ__init____mutmut_1, 
        'xǁTransportNotFoundErrorǁ__init____mutmut_2': xǁTransportNotFoundErrorǁ__init____mutmut_2, 
        'xǁTransportNotFoundErrorǁ__init____mutmut_3': xǁTransportNotFoundErrorǁ__init____mutmut_3, 
        'xǁTransportNotFoundErrorǁ__init____mutmut_4': xǁTransportNotFoundErrorǁ__init____mutmut_4
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTransportNotFoundErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁTransportNotFoundErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁTransportNotFoundErrorǁ__init____mutmut_orig)
    xǁTransportNotFoundErrorǁ__init____mutmut_orig.__name__ = 'xǁTransportNotFoundErrorǁ__init__'


class TransportCacheEvictedError(TransportError):
    """Transport was evicted from cache due to failures."""

    def xǁTransportCacheEvictedErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        scheme: str,
        consecutive_failures: int,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.scheme = scheme
        self.consecutive_failures = consecutive_failures

    def xǁTransportCacheEvictedErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        scheme: str,
        consecutive_failures: int,
        **kwargs: Any,
    ) -> None:
        super().__init__(None, **kwargs)
        self.scheme = scheme
        self.consecutive_failures = consecutive_failures

    def xǁTransportCacheEvictedErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        scheme: str,
        consecutive_failures: int,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.scheme = scheme
        self.consecutive_failures = consecutive_failures

    def xǁTransportCacheEvictedErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        scheme: str,
        consecutive_failures: int,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, )
        self.scheme = scheme
        self.consecutive_failures = consecutive_failures

    def xǁTransportCacheEvictedErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        scheme: str,
        consecutive_failures: int,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.scheme = None
        self.consecutive_failures = consecutive_failures

    def xǁTransportCacheEvictedErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        scheme: str,
        consecutive_failures: int,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.scheme = scheme
        self.consecutive_failures = None
    
    xǁTransportCacheEvictedErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTransportCacheEvictedErrorǁ__init____mutmut_1': xǁTransportCacheEvictedErrorǁ__init____mutmut_1, 
        'xǁTransportCacheEvictedErrorǁ__init____mutmut_2': xǁTransportCacheEvictedErrorǁ__init____mutmut_2, 
        'xǁTransportCacheEvictedErrorǁ__init____mutmut_3': xǁTransportCacheEvictedErrorǁ__init____mutmut_3, 
        'xǁTransportCacheEvictedErrorǁ__init____mutmut_4': xǁTransportCacheEvictedErrorǁ__init____mutmut_4, 
        'xǁTransportCacheEvictedErrorǁ__init____mutmut_5': xǁTransportCacheEvictedErrorǁ__init____mutmut_5
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTransportCacheEvictedErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁTransportCacheEvictedErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁTransportCacheEvictedErrorǁ__init____mutmut_orig)
    xǁTransportCacheEvictedErrorǁ__init____mutmut_orig.__name__ = 'xǁTransportCacheEvictedErrorǁ__init__'


__all__ = [
    "HTTPResponseError",
    "TransportCacheEvictedError",
    "TransportConfigurationError",
    "TransportConnectionError",
    "TransportError",
    "TransportNotFoundError",
    "TransportTimeoutError",
]


# <3 🧱🤝🚚🪄
