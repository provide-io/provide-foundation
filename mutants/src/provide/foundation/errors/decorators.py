# provide/foundation/errors/decorators.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Callable
import functools
import inspect
from typing import Any, Protocol, TypeVar, overload

"""Decorators for error handling and resilience patterns.

Provides decorators for common error handling patterns like retry,
fallback, and error suppression.
"""
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


class HasName(Protocol):
    """Protocol for objects that have a __name__ attribute."""

    __name__: str


F = TypeVar("F", bound=Callable[..., Any])


class ResilientErrorHandler:
    """Encapsulates error handling logic for the resilient decorator."""

    def xǁResilientErrorHandlerǁ__init____mutmut_orig(
        self,
        fallback: Any = None,
        log_errors: bool = True,
        context_provider: Callable[[], dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
        error_mapper: Callable[[Exception], Exception] | None = None,
        suppress: tuple[type[Exception], ...] | None = None,
        reraise: bool = True,
    ) -> None:
        self.fallback = fallback
        self.log_errors = log_errors
        self.context_provider = context_provider
        self.context = context
        self.error_mapper = error_mapper
        self.suppress = suppress
        self.reraise = reraise

    def xǁResilientErrorHandlerǁ__init____mutmut_1(
        self,
        fallback: Any = None,
        log_errors: bool = False,
        context_provider: Callable[[], dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
        error_mapper: Callable[[Exception], Exception] | None = None,
        suppress: tuple[type[Exception], ...] | None = None,
        reraise: bool = True,
    ) -> None:
        self.fallback = fallback
        self.log_errors = log_errors
        self.context_provider = context_provider
        self.context = context
        self.error_mapper = error_mapper
        self.suppress = suppress
        self.reraise = reraise

    def xǁResilientErrorHandlerǁ__init____mutmut_2(
        self,
        fallback: Any = None,
        log_errors: bool = True,
        context_provider: Callable[[], dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
        error_mapper: Callable[[Exception], Exception] | None = None,
        suppress: tuple[type[Exception], ...] | None = None,
        reraise: bool = False,
    ) -> None:
        self.fallback = fallback
        self.log_errors = log_errors
        self.context_provider = context_provider
        self.context = context
        self.error_mapper = error_mapper
        self.suppress = suppress
        self.reraise = reraise

    def xǁResilientErrorHandlerǁ__init____mutmut_3(
        self,
        fallback: Any = None,
        log_errors: bool = True,
        context_provider: Callable[[], dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
        error_mapper: Callable[[Exception], Exception] | None = None,
        suppress: tuple[type[Exception], ...] | None = None,
        reraise: bool = True,
    ) -> None:
        self.fallback = None
        self.log_errors = log_errors
        self.context_provider = context_provider
        self.context = context
        self.error_mapper = error_mapper
        self.suppress = suppress
        self.reraise = reraise

    def xǁResilientErrorHandlerǁ__init____mutmut_4(
        self,
        fallback: Any = None,
        log_errors: bool = True,
        context_provider: Callable[[], dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
        error_mapper: Callable[[Exception], Exception] | None = None,
        suppress: tuple[type[Exception], ...] | None = None,
        reraise: bool = True,
    ) -> None:
        self.fallback = fallback
        self.log_errors = None
        self.context_provider = context_provider
        self.context = context
        self.error_mapper = error_mapper
        self.suppress = suppress
        self.reraise = reraise

    def xǁResilientErrorHandlerǁ__init____mutmut_5(
        self,
        fallback: Any = None,
        log_errors: bool = True,
        context_provider: Callable[[], dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
        error_mapper: Callable[[Exception], Exception] | None = None,
        suppress: tuple[type[Exception], ...] | None = None,
        reraise: bool = True,
    ) -> None:
        self.fallback = fallback
        self.log_errors = log_errors
        self.context_provider = None
        self.context = context
        self.error_mapper = error_mapper
        self.suppress = suppress
        self.reraise = reraise

    def xǁResilientErrorHandlerǁ__init____mutmut_6(
        self,
        fallback: Any = None,
        log_errors: bool = True,
        context_provider: Callable[[], dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
        error_mapper: Callable[[Exception], Exception] | None = None,
        suppress: tuple[type[Exception], ...] | None = None,
        reraise: bool = True,
    ) -> None:
        self.fallback = fallback
        self.log_errors = log_errors
        self.context_provider = context_provider
        self.context = None
        self.error_mapper = error_mapper
        self.suppress = suppress
        self.reraise = reraise

    def xǁResilientErrorHandlerǁ__init____mutmut_7(
        self,
        fallback: Any = None,
        log_errors: bool = True,
        context_provider: Callable[[], dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
        error_mapper: Callable[[Exception], Exception] | None = None,
        suppress: tuple[type[Exception], ...] | None = None,
        reraise: bool = True,
    ) -> None:
        self.fallback = fallback
        self.log_errors = log_errors
        self.context_provider = context_provider
        self.context = context
        self.error_mapper = None
        self.suppress = suppress
        self.reraise = reraise

    def xǁResilientErrorHandlerǁ__init____mutmut_8(
        self,
        fallback: Any = None,
        log_errors: bool = True,
        context_provider: Callable[[], dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
        error_mapper: Callable[[Exception], Exception] | None = None,
        suppress: tuple[type[Exception], ...] | None = None,
        reraise: bool = True,
    ) -> None:
        self.fallback = fallback
        self.log_errors = log_errors
        self.context_provider = context_provider
        self.context = context
        self.error_mapper = error_mapper
        self.suppress = None
        self.reraise = reraise

    def xǁResilientErrorHandlerǁ__init____mutmut_9(
        self,
        fallback: Any = None,
        log_errors: bool = True,
        context_provider: Callable[[], dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
        error_mapper: Callable[[Exception], Exception] | None = None,
        suppress: tuple[type[Exception], ...] | None = None,
        reraise: bool = True,
    ) -> None:
        self.fallback = fallback
        self.log_errors = log_errors
        self.context_provider = context_provider
        self.context = context
        self.error_mapper = error_mapper
        self.suppress = suppress
        self.reraise = None
    
    xǁResilientErrorHandlerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁResilientErrorHandlerǁ__init____mutmut_1': xǁResilientErrorHandlerǁ__init____mutmut_1, 
        'xǁResilientErrorHandlerǁ__init____mutmut_2': xǁResilientErrorHandlerǁ__init____mutmut_2, 
        'xǁResilientErrorHandlerǁ__init____mutmut_3': xǁResilientErrorHandlerǁ__init____mutmut_3, 
        'xǁResilientErrorHandlerǁ__init____mutmut_4': xǁResilientErrorHandlerǁ__init____mutmut_4, 
        'xǁResilientErrorHandlerǁ__init____mutmut_5': xǁResilientErrorHandlerǁ__init____mutmut_5, 
        'xǁResilientErrorHandlerǁ__init____mutmut_6': xǁResilientErrorHandlerǁ__init____mutmut_6, 
        'xǁResilientErrorHandlerǁ__init____mutmut_7': xǁResilientErrorHandlerǁ__init____mutmut_7, 
        'xǁResilientErrorHandlerǁ__init____mutmut_8': xǁResilientErrorHandlerǁ__init____mutmut_8, 
        'xǁResilientErrorHandlerǁ__init____mutmut_9': xǁResilientErrorHandlerǁ__init____mutmut_9
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁResilientErrorHandlerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁResilientErrorHandlerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁResilientErrorHandlerǁ__init____mutmut_orig)
    xǁResilientErrorHandlerǁ__init____mutmut_orig.__name__ = 'xǁResilientErrorHandlerǁ__init__'

    def xǁResilientErrorHandlerǁbuild_context__mutmut_orig(self) -> dict[str, Any]:
        """Build logging context from provider and static context."""
        log_context = {}
        if self.context_provider:
            log_context.update(self.context_provider())
        if self.context:
            log_context.update(self.context)
        return log_context

    def xǁResilientErrorHandlerǁbuild_context__mutmut_1(self) -> dict[str, Any]:
        """Build logging context from provider and static context."""
        log_context = None
        if self.context_provider:
            log_context.update(self.context_provider())
        if self.context:
            log_context.update(self.context)
        return log_context

    def xǁResilientErrorHandlerǁbuild_context__mutmut_2(self) -> dict[str, Any]:
        """Build logging context from provider and static context."""
        log_context = {}
        if self.context_provider:
            log_context.update(None)
        if self.context:
            log_context.update(self.context)
        return log_context

    def xǁResilientErrorHandlerǁbuild_context__mutmut_3(self) -> dict[str, Any]:
        """Build logging context from provider and static context."""
        log_context = {}
        if self.context_provider:
            log_context.update(self.context_provider())
        if self.context:
            log_context.update(None)
        return log_context
    
    xǁResilientErrorHandlerǁbuild_context__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁResilientErrorHandlerǁbuild_context__mutmut_1': xǁResilientErrorHandlerǁbuild_context__mutmut_1, 
        'xǁResilientErrorHandlerǁbuild_context__mutmut_2': xǁResilientErrorHandlerǁbuild_context__mutmut_2, 
        'xǁResilientErrorHandlerǁbuild_context__mutmut_3': xǁResilientErrorHandlerǁbuild_context__mutmut_3
    }
    
    def build_context(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁResilientErrorHandlerǁbuild_context__mutmut_orig"), object.__getattribute__(self, "xǁResilientErrorHandlerǁbuild_context__mutmut_mutants"), args, kwargs, self)
        return result 
    
    build_context.__signature__ = _mutmut_signature(xǁResilientErrorHandlerǁbuild_context__mutmut_orig)
    xǁResilientErrorHandlerǁbuild_context__mutmut_orig.__name__ = 'xǁResilientErrorHandlerǁbuild_context'

    def xǁResilientErrorHandlerǁshould_suppress__mutmut_orig(self, exception: Exception) -> bool:
        """Check if the error should be suppressed."""
        return self.suppress is not None and isinstance(exception, self.suppress)

    def xǁResilientErrorHandlerǁshould_suppress__mutmut_1(self, exception: Exception) -> bool:
        """Check if the error should be suppressed."""
        return self.suppress is not None or isinstance(exception, self.suppress)

    def xǁResilientErrorHandlerǁshould_suppress__mutmut_2(self, exception: Exception) -> bool:
        """Check if the error should be suppressed."""
        return self.suppress is None and isinstance(exception, self.suppress)
    
    xǁResilientErrorHandlerǁshould_suppress__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁResilientErrorHandlerǁshould_suppress__mutmut_1': xǁResilientErrorHandlerǁshould_suppress__mutmut_1, 
        'xǁResilientErrorHandlerǁshould_suppress__mutmut_2': xǁResilientErrorHandlerǁshould_suppress__mutmut_2
    }
    
    def should_suppress(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁResilientErrorHandlerǁshould_suppress__mutmut_orig"), object.__getattribute__(self, "xǁResilientErrorHandlerǁshould_suppress__mutmut_mutants"), args, kwargs, self)
        return result 
    
    should_suppress.__signature__ = _mutmut_signature(xǁResilientErrorHandlerǁshould_suppress__mutmut_orig)
    xǁResilientErrorHandlerǁshould_suppress__mutmut_orig.__name__ = 'xǁResilientErrorHandlerǁshould_suppress'

    def xǁResilientErrorHandlerǁlog_suppressed__mutmut_orig(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log a suppressed error."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            f"Suppressed {type(exception).__name__} in {func_name}",
            function=func_name,
            error=str(exception),
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_suppressed__mutmut_1(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log a suppressed error."""
        if self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            f"Suppressed {type(exception).__name__} in {func_name}",
            function=func_name,
            error=str(exception),
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_suppressed__mutmut_2(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log a suppressed error."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            None,
            function=func_name,
            error=str(exception),
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_suppressed__mutmut_3(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log a suppressed error."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            f"Suppressed {type(exception).__name__} in {func_name}",
            function=None,
            error=str(exception),
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_suppressed__mutmut_4(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log a suppressed error."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            f"Suppressed {type(exception).__name__} in {func_name}",
            function=func_name,
            error=None,
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_suppressed__mutmut_5(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log a suppressed error."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            function=func_name,
            error=str(exception),
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_suppressed__mutmut_6(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log a suppressed error."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            f"Suppressed {type(exception).__name__} in {func_name}",
            error=str(exception),
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_suppressed__mutmut_7(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log a suppressed error."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            f"Suppressed {type(exception).__name__} in {func_name}",
            function=func_name,
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_suppressed__mutmut_8(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log a suppressed error."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            f"Suppressed {type(exception).__name__} in {func_name}",
            function=func_name,
            error=str(exception),
            )

    def xǁResilientErrorHandlerǁlog_suppressed__mutmut_9(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log a suppressed error."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            f"Suppressed {type(None).__name__} in {func_name}",
            function=func_name,
            error=str(exception),
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_suppressed__mutmut_10(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log a suppressed error."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            f"Suppressed {type(exception).__name__} in {func_name}",
            function=func_name,
            error=str(None),
            **log_context,
        )
    
    xǁResilientErrorHandlerǁlog_suppressed__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁResilientErrorHandlerǁlog_suppressed__mutmut_1': xǁResilientErrorHandlerǁlog_suppressed__mutmut_1, 
        'xǁResilientErrorHandlerǁlog_suppressed__mutmut_2': xǁResilientErrorHandlerǁlog_suppressed__mutmut_2, 
        'xǁResilientErrorHandlerǁlog_suppressed__mutmut_3': xǁResilientErrorHandlerǁlog_suppressed__mutmut_3, 
        'xǁResilientErrorHandlerǁlog_suppressed__mutmut_4': xǁResilientErrorHandlerǁlog_suppressed__mutmut_4, 
        'xǁResilientErrorHandlerǁlog_suppressed__mutmut_5': xǁResilientErrorHandlerǁlog_suppressed__mutmut_5, 
        'xǁResilientErrorHandlerǁlog_suppressed__mutmut_6': xǁResilientErrorHandlerǁlog_suppressed__mutmut_6, 
        'xǁResilientErrorHandlerǁlog_suppressed__mutmut_7': xǁResilientErrorHandlerǁlog_suppressed__mutmut_7, 
        'xǁResilientErrorHandlerǁlog_suppressed__mutmut_8': xǁResilientErrorHandlerǁlog_suppressed__mutmut_8, 
        'xǁResilientErrorHandlerǁlog_suppressed__mutmut_9': xǁResilientErrorHandlerǁlog_suppressed__mutmut_9, 
        'xǁResilientErrorHandlerǁlog_suppressed__mutmut_10': xǁResilientErrorHandlerǁlog_suppressed__mutmut_10
    }
    
    def log_suppressed(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁResilientErrorHandlerǁlog_suppressed__mutmut_orig"), object.__getattribute__(self, "xǁResilientErrorHandlerǁlog_suppressed__mutmut_mutants"), args, kwargs, self)
        return result 
    
    log_suppressed.__signature__ = _mutmut_signature(xǁResilientErrorHandlerǁlog_suppressed__mutmut_orig)
    xǁResilientErrorHandlerǁlog_suppressed__mutmut_orig.__name__ = 'xǁResilientErrorHandlerǁlog_suppressed'

    def xǁResilientErrorHandlerǁlog_error__mutmut_orig(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log an error with full details."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(
            f"Error in {func_name}: {exception}",
            exc_info=True,
            function=func_name,
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_error__mutmut_1(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log an error with full details."""
        if self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(
            f"Error in {func_name}: {exception}",
            exc_info=True,
            function=func_name,
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_error__mutmut_2(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log an error with full details."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(
            None,
            exc_info=True,
            function=func_name,
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_error__mutmut_3(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log an error with full details."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(
            f"Error in {func_name}: {exception}",
            exc_info=None,
            function=func_name,
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_error__mutmut_4(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log an error with full details."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(
            f"Error in {func_name}: {exception}",
            exc_info=True,
            function=None,
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_error__mutmut_5(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log an error with full details."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(
            exc_info=True,
            function=func_name,
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_error__mutmut_6(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log an error with full details."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(
            f"Error in {func_name}: {exception}",
            function=func_name,
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_error__mutmut_7(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log an error with full details."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(
            f"Error in {func_name}: {exception}",
            exc_info=True,
            **log_context,
        )

    def xǁResilientErrorHandlerǁlog_error__mutmut_8(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log an error with full details."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(
            f"Error in {func_name}: {exception}",
            exc_info=True,
            function=func_name,
            )

    def xǁResilientErrorHandlerǁlog_error__mutmut_9(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log an error with full details."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(
            f"Error in {func_name}: {exception}",
            exc_info=False,
            function=func_name,
            **log_context,
        )
    
    xǁResilientErrorHandlerǁlog_error__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁResilientErrorHandlerǁlog_error__mutmut_1': xǁResilientErrorHandlerǁlog_error__mutmut_1, 
        'xǁResilientErrorHandlerǁlog_error__mutmut_2': xǁResilientErrorHandlerǁlog_error__mutmut_2, 
        'xǁResilientErrorHandlerǁlog_error__mutmut_3': xǁResilientErrorHandlerǁlog_error__mutmut_3, 
        'xǁResilientErrorHandlerǁlog_error__mutmut_4': xǁResilientErrorHandlerǁlog_error__mutmut_4, 
        'xǁResilientErrorHandlerǁlog_error__mutmut_5': xǁResilientErrorHandlerǁlog_error__mutmut_5, 
        'xǁResilientErrorHandlerǁlog_error__mutmut_6': xǁResilientErrorHandlerǁlog_error__mutmut_6, 
        'xǁResilientErrorHandlerǁlog_error__mutmut_7': xǁResilientErrorHandlerǁlog_error__mutmut_7, 
        'xǁResilientErrorHandlerǁlog_error__mutmut_8': xǁResilientErrorHandlerǁlog_error__mutmut_8, 
        'xǁResilientErrorHandlerǁlog_error__mutmut_9': xǁResilientErrorHandlerǁlog_error__mutmut_9
    }
    
    def log_error(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁResilientErrorHandlerǁlog_error__mutmut_orig"), object.__getattribute__(self, "xǁResilientErrorHandlerǁlog_error__mutmut_mutants"), args, kwargs, self)
        return result 
    
    log_error.__signature__ = _mutmut_signature(xǁResilientErrorHandlerǁlog_error__mutmut_orig)
    xǁResilientErrorHandlerǁlog_error__mutmut_orig.__name__ = 'xǁResilientErrorHandlerǁlog_error'

    def xǁResilientErrorHandlerǁmap_error__mutmut_orig(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(exception)
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() and exception.code != exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if not mapped.cause and exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def xǁResilientErrorHandlerǁmap_error__mutmut_1(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = None
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() and exception.code != exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if not mapped.cause and exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def xǁResilientErrorHandlerǁmap_error__mutmut_2(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(None)
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() and exception.code != exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if not mapped.cause and exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def xǁResilientErrorHandlerǁmap_error__mutmut_3(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(exception)
            if mapped is exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() and exception.code != exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if not mapped.cause and exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def xǁResilientErrorHandlerǁmap_error__mutmut_4(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(exception)
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) or isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() and exception.code != exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if not mapped.cause and exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def xǁResilientErrorHandlerǁmap_error__mutmut_5(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(exception)
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() or exception.code != exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if not mapped.cause and exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def xǁResilientErrorHandlerǁmap_error__mutmut_6(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(exception)
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code != mapped._default_code() and exception.code != exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if not mapped.cause and exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def xǁResilientErrorHandlerǁmap_error__mutmut_7(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(exception)
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() and exception.code == exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if not mapped.cause and exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def xǁResilientErrorHandlerǁmap_error__mutmut_8(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(exception)
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() and exception.code != exception._default_code():
                        mapped.code = None

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if not mapped.cause and exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def xǁResilientErrorHandlerǁmap_error__mutmut_9(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(exception)
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() and exception.code != exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = None
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if not mapped.cause and exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def xǁResilientErrorHandlerǁmap_error__mutmut_10(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(exception)
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() and exception.code != exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = None

                    # Preserve cause chain if not already set
                    if not mapped.cause and exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def xǁResilientErrorHandlerǁmap_error__mutmut_11(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(exception)
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() and exception.code != exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if not mapped.cause or exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def xǁResilientErrorHandlerǁmap_error__mutmut_12(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(exception)
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() and exception.code != exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if mapped.cause and exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def xǁResilientErrorHandlerǁmap_error__mutmut_13(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(exception)
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() and exception.code != exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if not mapped.cause and exception.cause:
                        mapped.cause = None
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def xǁResilientErrorHandlerǁmap_error__mutmut_14(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(exception)
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() and exception.code != exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if not mapped.cause and exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = None

                return mapped
        return exception
    
    xǁResilientErrorHandlerǁmap_error__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁResilientErrorHandlerǁmap_error__mutmut_1': xǁResilientErrorHandlerǁmap_error__mutmut_1, 
        'xǁResilientErrorHandlerǁmap_error__mutmut_2': xǁResilientErrorHandlerǁmap_error__mutmut_2, 
        'xǁResilientErrorHandlerǁmap_error__mutmut_3': xǁResilientErrorHandlerǁmap_error__mutmut_3, 
        'xǁResilientErrorHandlerǁmap_error__mutmut_4': xǁResilientErrorHandlerǁmap_error__mutmut_4, 
        'xǁResilientErrorHandlerǁmap_error__mutmut_5': xǁResilientErrorHandlerǁmap_error__mutmut_5, 
        'xǁResilientErrorHandlerǁmap_error__mutmut_6': xǁResilientErrorHandlerǁmap_error__mutmut_6, 
        'xǁResilientErrorHandlerǁmap_error__mutmut_7': xǁResilientErrorHandlerǁmap_error__mutmut_7, 
        'xǁResilientErrorHandlerǁmap_error__mutmut_8': xǁResilientErrorHandlerǁmap_error__mutmut_8, 
        'xǁResilientErrorHandlerǁmap_error__mutmut_9': xǁResilientErrorHandlerǁmap_error__mutmut_9, 
        'xǁResilientErrorHandlerǁmap_error__mutmut_10': xǁResilientErrorHandlerǁmap_error__mutmut_10, 
        'xǁResilientErrorHandlerǁmap_error__mutmut_11': xǁResilientErrorHandlerǁmap_error__mutmut_11, 
        'xǁResilientErrorHandlerǁmap_error__mutmut_12': xǁResilientErrorHandlerǁmap_error__mutmut_12, 
        'xǁResilientErrorHandlerǁmap_error__mutmut_13': xǁResilientErrorHandlerǁmap_error__mutmut_13, 
        'xǁResilientErrorHandlerǁmap_error__mutmut_14': xǁResilientErrorHandlerǁmap_error__mutmut_14
    }
    
    def map_error(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁResilientErrorHandlerǁmap_error__mutmut_orig"), object.__getattribute__(self, "xǁResilientErrorHandlerǁmap_error__mutmut_mutants"), args, kwargs, self)
        return result 
    
    map_error.__signature__ = _mutmut_signature(xǁResilientErrorHandlerǁmap_error__mutmut_orig)
    xǁResilientErrorHandlerǁmap_error__mutmut_orig.__name__ = 'xǁResilientErrorHandlerǁmap_error'

    def xǁResilientErrorHandlerǁprocess_error__mutmut_orig(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_1(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = None

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_2(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(None):
            self.log_suppressed(exception, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_3(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(None, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_4(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, None, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_5(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, None)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_6(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_7(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_8(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, )
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_9(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(None, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_10(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, None, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_11(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, None)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_12(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_13(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_14(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, )

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_15(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_16(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = None
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_17(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(None)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def xǁResilientErrorHandlerǁprocess_error__mutmut_18(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception
    
    xǁResilientErrorHandlerǁprocess_error__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁResilientErrorHandlerǁprocess_error__mutmut_1': xǁResilientErrorHandlerǁprocess_error__mutmut_1, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_2': xǁResilientErrorHandlerǁprocess_error__mutmut_2, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_3': xǁResilientErrorHandlerǁprocess_error__mutmut_3, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_4': xǁResilientErrorHandlerǁprocess_error__mutmut_4, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_5': xǁResilientErrorHandlerǁprocess_error__mutmut_5, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_6': xǁResilientErrorHandlerǁprocess_error__mutmut_6, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_7': xǁResilientErrorHandlerǁprocess_error__mutmut_7, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_8': xǁResilientErrorHandlerǁprocess_error__mutmut_8, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_9': xǁResilientErrorHandlerǁprocess_error__mutmut_9, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_10': xǁResilientErrorHandlerǁprocess_error__mutmut_10, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_11': xǁResilientErrorHandlerǁprocess_error__mutmut_11, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_12': xǁResilientErrorHandlerǁprocess_error__mutmut_12, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_13': xǁResilientErrorHandlerǁprocess_error__mutmut_13, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_14': xǁResilientErrorHandlerǁprocess_error__mutmut_14, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_15': xǁResilientErrorHandlerǁprocess_error__mutmut_15, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_16': xǁResilientErrorHandlerǁprocess_error__mutmut_16, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_17': xǁResilientErrorHandlerǁprocess_error__mutmut_17, 
        'xǁResilientErrorHandlerǁprocess_error__mutmut_18': xǁResilientErrorHandlerǁprocess_error__mutmut_18
    }
    
    def process_error(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁResilientErrorHandlerǁprocess_error__mutmut_orig"), object.__getattribute__(self, "xǁResilientErrorHandlerǁprocess_error__mutmut_mutants"), args, kwargs, self)
        return result 
    
    process_error.__signature__ = _mutmut_signature(xǁResilientErrorHandlerǁprocess_error__mutmut_orig)
    xǁResilientErrorHandlerǁprocess_error__mutmut_orig.__name__ = 'xǁResilientErrorHandlerǁprocess_error'


def _create_async_wrapper(func: F, handler: ResilientErrorHandler) -> F:
    """Create an async wrapper for error handling."""

    @functools.wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return handler.process_error(e, getattr(func, "__name__", "<anonymous>"))

    return async_wrapper  # type: ignore


def _create_sync_wrapper(func: F, handler: ResilientErrorHandler) -> F:
    """Create a sync wrapper for error handling."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return handler.process_error(e, getattr(func, "__name__", "<anonymous>"))

    return wrapper  # type: ignore


@overload
def resilient(
    func: F,
) -> F: ...


@overload
def resilient(
    func: None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F]: ...


def x_resilient__mutmut_orig(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_1(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = False,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_2(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = False,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_3(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = None

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_4(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=None,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_5(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=None,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_6(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=None,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_7(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=None,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_8(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=None,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_9(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=None,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_10(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=None,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_11(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_12(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_13(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_14(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_15(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_16(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_17(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_18(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(None):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_19(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(None, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_20(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, None)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_21(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_22(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, )
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_23(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(None, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_24(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, None)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_25(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_26(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, )

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_27(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is not None:
        return decorator
    return decorator(func)


def x_resilient__mutmut_28(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(None)

x_resilient__mutmut_mutants : ClassVar[MutantDict] = {
'x_resilient__mutmut_1': x_resilient__mutmut_1, 
    'x_resilient__mutmut_2': x_resilient__mutmut_2, 
    'x_resilient__mutmut_3': x_resilient__mutmut_3, 
    'x_resilient__mutmut_4': x_resilient__mutmut_4, 
    'x_resilient__mutmut_5': x_resilient__mutmut_5, 
    'x_resilient__mutmut_6': x_resilient__mutmut_6, 
    'x_resilient__mutmut_7': x_resilient__mutmut_7, 
    'x_resilient__mutmut_8': x_resilient__mutmut_8, 
    'x_resilient__mutmut_9': x_resilient__mutmut_9, 
    'x_resilient__mutmut_10': x_resilient__mutmut_10, 
    'x_resilient__mutmut_11': x_resilient__mutmut_11, 
    'x_resilient__mutmut_12': x_resilient__mutmut_12, 
    'x_resilient__mutmut_13': x_resilient__mutmut_13, 
    'x_resilient__mutmut_14': x_resilient__mutmut_14, 
    'x_resilient__mutmut_15': x_resilient__mutmut_15, 
    'x_resilient__mutmut_16': x_resilient__mutmut_16, 
    'x_resilient__mutmut_17': x_resilient__mutmut_17, 
    'x_resilient__mutmut_18': x_resilient__mutmut_18, 
    'x_resilient__mutmut_19': x_resilient__mutmut_19, 
    'x_resilient__mutmut_20': x_resilient__mutmut_20, 
    'x_resilient__mutmut_21': x_resilient__mutmut_21, 
    'x_resilient__mutmut_22': x_resilient__mutmut_22, 
    'x_resilient__mutmut_23': x_resilient__mutmut_23, 
    'x_resilient__mutmut_24': x_resilient__mutmut_24, 
    'x_resilient__mutmut_25': x_resilient__mutmut_25, 
    'x_resilient__mutmut_26': x_resilient__mutmut_26, 
    'x_resilient__mutmut_27': x_resilient__mutmut_27, 
    'x_resilient__mutmut_28': x_resilient__mutmut_28
}

def resilient(*args, **kwargs):
    result = _mutmut_trampoline(x_resilient__mutmut_orig, x_resilient__mutmut_mutants, args, kwargs)
    return result 

resilient.__signature__ = _mutmut_signature(x_resilient__mutmut_orig)
x_resilient__mutmut_orig.__name__ = 'x_resilient'


def x_suppress_and_log__mutmut_orig(
    *exceptions: type[Exception],
    fallback: Any = None,
    log_level: str = "warning",
) -> Callable[[F], F]:
    """Decorator to suppress specific exceptions and log them.

    Args:
        *exceptions: Exception types to suppress.
        fallback: Value to return when exception is suppressed.
        log_level: Log level to use ('debug', 'info', 'warning', 'error').

    Returns:
        Decorated function.

    Examples:
        >>> @suppress_and_log(KeyError, AttributeError, fallback={})
        ... def get_nested_value(data):
        ...     return data["key"].attribute

    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                # Get appropriate log method
                from provide.foundation.hub.foundation import get_foundation_logger

                if log_level in ("debug", "info", "warning", "error", "critical"):
                    log_method = getattr(get_foundation_logger(), log_level)
                else:
                    log_method = get_foundation_logger().warning

                log_method(
                    f"Suppressed {type(e).__name__} in {getattr(func, '__name__', '<anonymous>')}: {e}",
                    function=getattr(func, "__name__", "<anonymous>"),
                    error_type=type(e).__name__,
                    error=str(e),
                    fallback=fallback,
                )

                return fallback

        return wrapper  # type: ignore

    return decorator


def x_suppress_and_log__mutmut_1(
    *exceptions: type[Exception],
    fallback: Any = None,
    log_level: str = "XXwarningXX",
) -> Callable[[F], F]:
    """Decorator to suppress specific exceptions and log them.

    Args:
        *exceptions: Exception types to suppress.
        fallback: Value to return when exception is suppressed.
        log_level: Log level to use ('debug', 'info', 'warning', 'error').

    Returns:
        Decorated function.

    Examples:
        >>> @suppress_and_log(KeyError, AttributeError, fallback={})
        ... def get_nested_value(data):
        ...     return data["key"].attribute

    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                # Get appropriate log method
                from provide.foundation.hub.foundation import get_foundation_logger

                if log_level in ("debug", "info", "warning", "error", "critical"):
                    log_method = getattr(get_foundation_logger(), log_level)
                else:
                    log_method = get_foundation_logger().warning

                log_method(
                    f"Suppressed {type(e).__name__} in {getattr(func, '__name__', '<anonymous>')}: {e}",
                    function=getattr(func, "__name__", "<anonymous>"),
                    error_type=type(e).__name__,
                    error=str(e),
                    fallback=fallback,
                )

                return fallback

        return wrapper  # type: ignore

    return decorator


def x_suppress_and_log__mutmut_2(
    *exceptions: type[Exception],
    fallback: Any = None,
    log_level: str = "WARNING",
) -> Callable[[F], F]:
    """Decorator to suppress specific exceptions and log them.

    Args:
        *exceptions: Exception types to suppress.
        fallback: Value to return when exception is suppressed.
        log_level: Log level to use ('debug', 'info', 'warning', 'error').

    Returns:
        Decorated function.

    Examples:
        >>> @suppress_and_log(KeyError, AttributeError, fallback={})
        ... def get_nested_value(data):
        ...     return data["key"].attribute

    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                # Get appropriate log method
                from provide.foundation.hub.foundation import get_foundation_logger

                if log_level in ("debug", "info", "warning", "error", "critical"):
                    log_method = getattr(get_foundation_logger(), log_level)
                else:
                    log_method = get_foundation_logger().warning

                log_method(
                    f"Suppressed {type(e).__name__} in {getattr(func, '__name__', '<anonymous>')}: {e}",
                    function=getattr(func, "__name__", "<anonymous>"),
                    error_type=type(e).__name__,
                    error=str(e),
                    fallback=fallback,
                )

                return fallback

        return wrapper  # type: ignore

    return decorator

x_suppress_and_log__mutmut_mutants : ClassVar[MutantDict] = {
'x_suppress_and_log__mutmut_1': x_suppress_and_log__mutmut_1, 
    'x_suppress_and_log__mutmut_2': x_suppress_and_log__mutmut_2
}

def suppress_and_log(*args, **kwargs):
    result = _mutmut_trampoline(x_suppress_and_log__mutmut_orig, x_suppress_and_log__mutmut_mutants, args, kwargs)
    return result 

suppress_and_log.__signature__ = _mutmut_signature(x_suppress_and_log__mutmut_orig)
x_suppress_and_log__mutmut_orig.__name__ = 'x_suppress_and_log'


def x_fallback_on_error__mutmut_orig(
    fallback_func: Callable[..., Any],
    *exceptions: type[Exception],
    log_errors: bool = True,
) -> Callable[[F], F]:
    """Decorator to call a fallback function when errors occur.

    Args:
        fallback_func: Function to call when an error occurs.
        *exceptions: Specific exception types to handle (all if empty).
        log_errors: Whether to log errors before calling fallback.

    Returns:
        Decorated function.

    Examples:
        >>> def use_cache():
        ...     return cached_value
        ...
        >>> @fallback_on_error(use_cache, NetworkError)
        ... def fetch_from_api():
        ...     return api_call()

    """
    catch_types = exceptions if exceptions else (Exception,)

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except catch_types as e:
                if log_errors:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().warning(
                        f"Using fallback for {getattr(func, '__name__', '<anonymous>')} due to {type(e).__name__}",
                        function=getattr(func, "__name__", "<anonymous>"),
                        error_type=type(e).__name__,
                        error=str(e),
                        fallback=getattr(fallback_func, "__name__", "<anonymous>"),
                    )

                # Call fallback with same arguments
                try:
                    return fallback_func(*args, **kwargs)
                except Exception as fallback_error:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"Fallback function {getattr(fallback_func, '__name__', '<anonymous>')} also failed",
                        exc_info=True,
                        original_error=str(e),
                        fallback_error=str(fallback_error),
                    )
                    # Re-raise the fallback error
                    raise fallback_error from e

        return wrapper  # type: ignore

    return decorator


def x_fallback_on_error__mutmut_1(
    fallback_func: Callable[..., Any],
    *exceptions: type[Exception],
    log_errors: bool = False,
) -> Callable[[F], F]:
    """Decorator to call a fallback function when errors occur.

    Args:
        fallback_func: Function to call when an error occurs.
        *exceptions: Specific exception types to handle (all if empty).
        log_errors: Whether to log errors before calling fallback.

    Returns:
        Decorated function.

    Examples:
        >>> def use_cache():
        ...     return cached_value
        ...
        >>> @fallback_on_error(use_cache, NetworkError)
        ... def fetch_from_api():
        ...     return api_call()

    """
    catch_types = exceptions if exceptions else (Exception,)

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except catch_types as e:
                if log_errors:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().warning(
                        f"Using fallback for {getattr(func, '__name__', '<anonymous>')} due to {type(e).__name__}",
                        function=getattr(func, "__name__", "<anonymous>"),
                        error_type=type(e).__name__,
                        error=str(e),
                        fallback=getattr(fallback_func, "__name__", "<anonymous>"),
                    )

                # Call fallback with same arguments
                try:
                    return fallback_func(*args, **kwargs)
                except Exception as fallback_error:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"Fallback function {getattr(fallback_func, '__name__', '<anonymous>')} also failed",
                        exc_info=True,
                        original_error=str(e),
                        fallback_error=str(fallback_error),
                    )
                    # Re-raise the fallback error
                    raise fallback_error from e

        return wrapper  # type: ignore

    return decorator


def x_fallback_on_error__mutmut_2(
    fallback_func: Callable[..., Any],
    *exceptions: type[Exception],
    log_errors: bool = True,
) -> Callable[[F], F]:
    """Decorator to call a fallback function when errors occur.

    Args:
        fallback_func: Function to call when an error occurs.
        *exceptions: Specific exception types to handle (all if empty).
        log_errors: Whether to log errors before calling fallback.

    Returns:
        Decorated function.

    Examples:
        >>> def use_cache():
        ...     return cached_value
        ...
        >>> @fallback_on_error(use_cache, NetworkError)
        ... def fetch_from_api():
        ...     return api_call()

    """
    catch_types = None

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except catch_types as e:
                if log_errors:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().warning(
                        f"Using fallback for {getattr(func, '__name__', '<anonymous>')} due to {type(e).__name__}",
                        function=getattr(func, "__name__", "<anonymous>"),
                        error_type=type(e).__name__,
                        error=str(e),
                        fallback=getattr(fallback_func, "__name__", "<anonymous>"),
                    )

                # Call fallback with same arguments
                try:
                    return fallback_func(*args, **kwargs)
                except Exception as fallback_error:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"Fallback function {getattr(fallback_func, '__name__', '<anonymous>')} also failed",
                        exc_info=True,
                        original_error=str(e),
                        fallback_error=str(fallback_error),
                    )
                    # Re-raise the fallback error
                    raise fallback_error from e

        return wrapper  # type: ignore

    return decorator

x_fallback_on_error__mutmut_mutants : ClassVar[MutantDict] = {
'x_fallback_on_error__mutmut_1': x_fallback_on_error__mutmut_1, 
    'x_fallback_on_error__mutmut_2': x_fallback_on_error__mutmut_2
}

def fallback_on_error(*args, **kwargs):
    result = _mutmut_trampoline(x_fallback_on_error__mutmut_orig, x_fallback_on_error__mutmut_mutants, args, kwargs)
    return result 

fallback_on_error.__signature__ = _mutmut_signature(x_fallback_on_error__mutmut_orig)
x_fallback_on_error__mutmut_orig.__name__ = 'x_fallback_on_error'


# <3 🧱🤝🐛🪄
