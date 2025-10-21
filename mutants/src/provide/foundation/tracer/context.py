# provide/foundation/tracer/context.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# context.py
#
import contextvars
from typing import Any

from provide.foundation.tracer.spans import Span

"""Trace context management for Foundation tracer.
Manages trace context and span hierarchy.
"""

_current_span: contextvars.ContextVar[Span | None] = contextvars.ContextVar("current_span")

# Context variable to track the current trace ID
_current_trace_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("current_trace_id")
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


def get_current_span() -> Span | None:
    """Get the currently active span."""
    return _current_span.get(None)


def get_current_trace_id() -> str | None:
    """Get the current trace ID."""
    return _current_trace_id.get(None)


def x_set_current_span__mutmut_orig(span: Span | None) -> None:
    """Set the current active span."""
    _current_span.set(span)
    if span:
        _current_trace_id.set(span.trace_id)


def x_set_current_span__mutmut_1(span: Span | None) -> None:
    """Set the current active span."""
    _current_span.set(None)
    if span:
        _current_trace_id.set(span.trace_id)


def x_set_current_span__mutmut_2(span: Span | None) -> None:
    """Set the current active span."""
    _current_span.set(span)
    if span:
        _current_trace_id.set(None)

x_set_current_span__mutmut_mutants : ClassVar[MutantDict] = {
'x_set_current_span__mutmut_1': x_set_current_span__mutmut_1, 
    'x_set_current_span__mutmut_2': x_set_current_span__mutmut_2
}

def set_current_span(*args, **kwargs):
    result = _mutmut_trampoline(x_set_current_span__mutmut_orig, x_set_current_span__mutmut_mutants, args, kwargs)
    return result 

set_current_span.__signature__ = _mutmut_signature(x_set_current_span__mutmut_orig)
x_set_current_span__mutmut_orig.__name__ = 'x_set_current_span'


def x_create_child_span__mutmut_orig(name: str, parent: Span | None = None) -> Span:
    """Create a child span.

    Args:
        name: Name of the span
        parent: Parent span, defaults to current span

    Returns:
        New child span

    """
    if parent is None:
        parent = get_current_span()

    if parent:
        return Span(name=name, parent_id=parent.span_id, trace_id=parent.trace_id)
    return Span(name=name)


def x_create_child_span__mutmut_1(name: str, parent: Span | None = None) -> Span:
    """Create a child span.

    Args:
        name: Name of the span
        parent: Parent span, defaults to current span

    Returns:
        New child span

    """
    if parent is not None:
        parent = get_current_span()

    if parent:
        return Span(name=name, parent_id=parent.span_id, trace_id=parent.trace_id)
    return Span(name=name)


def x_create_child_span__mutmut_2(name: str, parent: Span | None = None) -> Span:
    """Create a child span.

    Args:
        name: Name of the span
        parent: Parent span, defaults to current span

    Returns:
        New child span

    """
    if parent is None:
        parent = None

    if parent:
        return Span(name=name, parent_id=parent.span_id, trace_id=parent.trace_id)
    return Span(name=name)


def x_create_child_span__mutmut_3(name: str, parent: Span | None = None) -> Span:
    """Create a child span.

    Args:
        name: Name of the span
        parent: Parent span, defaults to current span

    Returns:
        New child span

    """
    if parent is None:
        parent = get_current_span()

    if parent:
        return Span(name=None, parent_id=parent.span_id, trace_id=parent.trace_id)
    return Span(name=name)


def x_create_child_span__mutmut_4(name: str, parent: Span | None = None) -> Span:
    """Create a child span.

    Args:
        name: Name of the span
        parent: Parent span, defaults to current span

    Returns:
        New child span

    """
    if parent is None:
        parent = get_current_span()

    if parent:
        return Span(name=name, parent_id=None, trace_id=parent.trace_id)
    return Span(name=name)


def x_create_child_span__mutmut_5(name: str, parent: Span | None = None) -> Span:
    """Create a child span.

    Args:
        name: Name of the span
        parent: Parent span, defaults to current span

    Returns:
        New child span

    """
    if parent is None:
        parent = get_current_span()

    if parent:
        return Span(name=name, parent_id=parent.span_id, trace_id=None)
    return Span(name=name)


def x_create_child_span__mutmut_6(name: str, parent: Span | None = None) -> Span:
    """Create a child span.

    Args:
        name: Name of the span
        parent: Parent span, defaults to current span

    Returns:
        New child span

    """
    if parent is None:
        parent = get_current_span()

    if parent:
        return Span(parent_id=parent.span_id, trace_id=parent.trace_id)
    return Span(name=name)


def x_create_child_span__mutmut_7(name: str, parent: Span | None = None) -> Span:
    """Create a child span.

    Args:
        name: Name of the span
        parent: Parent span, defaults to current span

    Returns:
        New child span

    """
    if parent is None:
        parent = get_current_span()

    if parent:
        return Span(name=name, trace_id=parent.trace_id)
    return Span(name=name)


def x_create_child_span__mutmut_8(name: str, parent: Span | None = None) -> Span:
    """Create a child span.

    Args:
        name: Name of the span
        parent: Parent span, defaults to current span

    Returns:
        New child span

    """
    if parent is None:
        parent = get_current_span()

    if parent:
        return Span(name=name, parent_id=parent.span_id, )
    return Span(name=name)


def x_create_child_span__mutmut_9(name: str, parent: Span | None = None) -> Span:
    """Create a child span.

    Args:
        name: Name of the span
        parent: Parent span, defaults to current span

    Returns:
        New child span

    """
    if parent is None:
        parent = get_current_span()

    if parent:
        return Span(name=name, parent_id=parent.span_id, trace_id=parent.trace_id)
    return Span(name=None)

x_create_child_span__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_child_span__mutmut_1': x_create_child_span__mutmut_1, 
    'x_create_child_span__mutmut_2': x_create_child_span__mutmut_2, 
    'x_create_child_span__mutmut_3': x_create_child_span__mutmut_3, 
    'x_create_child_span__mutmut_4': x_create_child_span__mutmut_4, 
    'x_create_child_span__mutmut_5': x_create_child_span__mutmut_5, 
    'x_create_child_span__mutmut_6': x_create_child_span__mutmut_6, 
    'x_create_child_span__mutmut_7': x_create_child_span__mutmut_7, 
    'x_create_child_span__mutmut_8': x_create_child_span__mutmut_8, 
    'x_create_child_span__mutmut_9': x_create_child_span__mutmut_9
}

def create_child_span(*args, **kwargs):
    result = _mutmut_trampoline(x_create_child_span__mutmut_orig, x_create_child_span__mutmut_mutants, args, kwargs)
    return result 

create_child_span.__signature__ = _mutmut_signature(x_create_child_span__mutmut_orig)
x_create_child_span__mutmut_orig.__name__ = 'x_create_child_span'


class SpanContext:
    """Context manager for managing span lifecycle.

    Automatically sets and clears the current span.
    """

    def xǁSpanContextǁ__init____mutmut_orig(self, span: Span) -> None:
        self.span = span
        self.previous_span: Span | None = None

    def xǁSpanContextǁ__init____mutmut_1(self, span: Span) -> None:
        self.span = None
        self.previous_span: Span | None = None

    def xǁSpanContextǁ__init____mutmut_2(self, span: Span) -> None:
        self.span = span
        self.previous_span: Span | None = ""
    
    xǁSpanContextǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSpanContextǁ__init____mutmut_1': xǁSpanContextǁ__init____mutmut_1, 
        'xǁSpanContextǁ__init____mutmut_2': xǁSpanContextǁ__init____mutmut_2
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSpanContextǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSpanContextǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSpanContextǁ__init____mutmut_orig)
    xǁSpanContextǁ__init____mutmut_orig.__name__ = 'xǁSpanContextǁ__init__'

    def xǁSpanContextǁ__enter____mutmut_orig(self) -> Span:
        """Enter the span context."""
        self.previous_span = get_current_span()
        set_current_span(self.span)
        return self.span

    def xǁSpanContextǁ__enter____mutmut_1(self) -> Span:
        """Enter the span context."""
        self.previous_span = None
        set_current_span(self.span)
        return self.span

    def xǁSpanContextǁ__enter____mutmut_2(self) -> Span:
        """Enter the span context."""
        self.previous_span = get_current_span()
        set_current_span(None)
        return self.span
    
    xǁSpanContextǁ__enter____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSpanContextǁ__enter____mutmut_1': xǁSpanContextǁ__enter____mutmut_1, 
        'xǁSpanContextǁ__enter____mutmut_2': xǁSpanContextǁ__enter____mutmut_2
    }
    
    def __enter__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSpanContextǁ__enter____mutmut_orig"), object.__getattribute__(self, "xǁSpanContextǁ__enter____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __enter__.__signature__ = _mutmut_signature(xǁSpanContextǁ__enter____mutmut_orig)
    xǁSpanContextǁ__enter____mutmut_orig.__name__ = 'xǁSpanContextǁ__enter__'

    def xǁSpanContextǁ__exit____mutmut_orig(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any
    ) -> None:
        """Exit the span context."""
        if exc_type is not None:
            self.span.set_error(f"{exc_type.__name__}: {exc_val}")
        self.span.finish()
        set_current_span(self.previous_span)

    def xǁSpanContextǁ__exit____mutmut_1(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any
    ) -> None:
        """Exit the span context."""
        if exc_type is None:
            self.span.set_error(f"{exc_type.__name__}: {exc_val}")
        self.span.finish()
        set_current_span(self.previous_span)

    def xǁSpanContextǁ__exit____mutmut_2(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any
    ) -> None:
        """Exit the span context."""
        if exc_type is not None:
            self.span.set_error(None)
        self.span.finish()
        set_current_span(self.previous_span)

    def xǁSpanContextǁ__exit____mutmut_3(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any
    ) -> None:
        """Exit the span context."""
        if exc_type is not None:
            self.span.set_error(f"{exc_type.__name__}: {exc_val}")
        self.span.finish()
        set_current_span(None)
    
    xǁSpanContextǁ__exit____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSpanContextǁ__exit____mutmut_1': xǁSpanContextǁ__exit____mutmut_1, 
        'xǁSpanContextǁ__exit____mutmut_2': xǁSpanContextǁ__exit____mutmut_2, 
        'xǁSpanContextǁ__exit____mutmut_3': xǁSpanContextǁ__exit____mutmut_3
    }
    
    def __exit__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSpanContextǁ__exit____mutmut_orig"), object.__getattribute__(self, "xǁSpanContextǁ__exit____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __exit__.__signature__ = _mutmut_signature(xǁSpanContextǁ__exit____mutmut_orig)
    xǁSpanContextǁ__exit____mutmut_orig.__name__ = 'xǁSpanContextǁ__exit__'


def x_with_span__mutmut_orig(name: str) -> SpanContext:
    """Create a new span context.

    Args:
        name: Name of the span

    Returns:
        SpanContext that can be used as a context manager

    """
    span = create_child_span(name)
    return SpanContext(span)


def x_with_span__mutmut_1(name: str) -> SpanContext:
    """Create a new span context.

    Args:
        name: Name of the span

    Returns:
        SpanContext that can be used as a context manager

    """
    span = None
    return SpanContext(span)


def x_with_span__mutmut_2(name: str) -> SpanContext:
    """Create a new span context.

    Args:
        name: Name of the span

    Returns:
        SpanContext that can be used as a context manager

    """
    span = create_child_span(None)
    return SpanContext(span)


def x_with_span__mutmut_3(name: str) -> SpanContext:
    """Create a new span context.

    Args:
        name: Name of the span

    Returns:
        SpanContext that can be used as a context manager

    """
    span = create_child_span(name)
    return SpanContext(None)

x_with_span__mutmut_mutants : ClassVar[MutantDict] = {
'x_with_span__mutmut_1': x_with_span__mutmut_1, 
    'x_with_span__mutmut_2': x_with_span__mutmut_2, 
    'x_with_span__mutmut_3': x_with_span__mutmut_3
}

def with_span(*args, **kwargs):
    result = _mutmut_trampoline(x_with_span__mutmut_orig, x_with_span__mutmut_mutants, args, kwargs)
    return result 

with_span.__signature__ = _mutmut_signature(x_with_span__mutmut_orig)
x_with_span__mutmut_orig.__name__ = 'x_with_span'


def x_get_trace_context__mutmut_orig() -> dict[str, Any]:
    """Get the current trace context information.

    Returns:
        Dictionary with trace context information

    """
    current_span = get_current_span()
    trace_id = get_current_trace_id()

    return {
        "trace_id": trace_id,
        "span_id": current_span.span_id if current_span else None,
        "span_name": current_span.name if current_span else None,
    }


def x_get_trace_context__mutmut_1() -> dict[str, Any]:
    """Get the current trace context information.

    Returns:
        Dictionary with trace context information

    """
    current_span = None
    trace_id = get_current_trace_id()

    return {
        "trace_id": trace_id,
        "span_id": current_span.span_id if current_span else None,
        "span_name": current_span.name if current_span else None,
    }


def x_get_trace_context__mutmut_2() -> dict[str, Any]:
    """Get the current trace context information.

    Returns:
        Dictionary with trace context information

    """
    current_span = get_current_span()
    trace_id = None

    return {
        "trace_id": trace_id,
        "span_id": current_span.span_id if current_span else None,
        "span_name": current_span.name if current_span else None,
    }


def x_get_trace_context__mutmut_3() -> dict[str, Any]:
    """Get the current trace context information.

    Returns:
        Dictionary with trace context information

    """
    current_span = get_current_span()
    trace_id = get_current_trace_id()

    return {
        "XXtrace_idXX": trace_id,
        "span_id": current_span.span_id if current_span else None,
        "span_name": current_span.name if current_span else None,
    }


def x_get_trace_context__mutmut_4() -> dict[str, Any]:
    """Get the current trace context information.

    Returns:
        Dictionary with trace context information

    """
    current_span = get_current_span()
    trace_id = get_current_trace_id()

    return {
        "TRACE_ID": trace_id,
        "span_id": current_span.span_id if current_span else None,
        "span_name": current_span.name if current_span else None,
    }


def x_get_trace_context__mutmut_5() -> dict[str, Any]:
    """Get the current trace context information.

    Returns:
        Dictionary with trace context information

    """
    current_span = get_current_span()
    trace_id = get_current_trace_id()

    return {
        "trace_id": trace_id,
        "XXspan_idXX": current_span.span_id if current_span else None,
        "span_name": current_span.name if current_span else None,
    }


def x_get_trace_context__mutmut_6() -> dict[str, Any]:
    """Get the current trace context information.

    Returns:
        Dictionary with trace context information

    """
    current_span = get_current_span()
    trace_id = get_current_trace_id()

    return {
        "trace_id": trace_id,
        "SPAN_ID": current_span.span_id if current_span else None,
        "span_name": current_span.name if current_span else None,
    }


def x_get_trace_context__mutmut_7() -> dict[str, Any]:
    """Get the current trace context information.

    Returns:
        Dictionary with trace context information

    """
    current_span = get_current_span()
    trace_id = get_current_trace_id()

    return {
        "trace_id": trace_id,
        "span_id": current_span.span_id if current_span else None,
        "XXspan_nameXX": current_span.name if current_span else None,
    }


def x_get_trace_context__mutmut_8() -> dict[str, Any]:
    """Get the current trace context information.

    Returns:
        Dictionary with trace context information

    """
    current_span = get_current_span()
    trace_id = get_current_trace_id()

    return {
        "trace_id": trace_id,
        "span_id": current_span.span_id if current_span else None,
        "SPAN_NAME": current_span.name if current_span else None,
    }

x_get_trace_context__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_trace_context__mutmut_1': x_get_trace_context__mutmut_1, 
    'x_get_trace_context__mutmut_2': x_get_trace_context__mutmut_2, 
    'x_get_trace_context__mutmut_3': x_get_trace_context__mutmut_3, 
    'x_get_trace_context__mutmut_4': x_get_trace_context__mutmut_4, 
    'x_get_trace_context__mutmut_5': x_get_trace_context__mutmut_5, 
    'x_get_trace_context__mutmut_6': x_get_trace_context__mutmut_6, 
    'x_get_trace_context__mutmut_7': x_get_trace_context__mutmut_7, 
    'x_get_trace_context__mutmut_8': x_get_trace_context__mutmut_8
}

def get_trace_context(*args, **kwargs):
    result = _mutmut_trampoline(x_get_trace_context__mutmut_orig, x_get_trace_context__mutmut_mutants, args, kwargs)
    return result 

get_trace_context.__signature__ = _mutmut_signature(x_get_trace_context__mutmut_orig)
x_get_trace_context__mutmut_orig.__name__ = 'x_get_trace_context'


# <3 🧱🤝👣🪄
