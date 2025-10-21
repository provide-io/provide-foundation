# provide/foundation/hub/events.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Callable
import threading
from typing import Any
import weakref

from attrs import define, field

"""Event system for decoupled component communication.

Provides a lightweight event system to break circular dependencies
between components, particularly between registry and logger.
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


@define(frozen=True, slots=True)
class Event:
    """Base event class for all system events."""

    name: str
    data: dict[str, Any] = field(factory=dict)
    source: str | None = None


@define(frozen=True, slots=True)
class RegistryEvent:
    """Events emitted by the registry system."""

    name: str
    operation: str
    item_name: str
    dimension: str
    data: dict[str, Any] = field(factory=dict)
    source: str | None = None

    def __attrs_post_init__(self) -> None:
        """Set event name from operation."""
        if not self.name:
            object.__setattr__(self, "name", f"registry.{self.operation}")


class EventBus:
    """Thread-safe event bus for decoupled component communication.

    Uses weak references to prevent memory leaks from event handlers.
    """

    def xǁEventBusǁ__init____mutmut_orig(self) -> None:
        """Initialize empty event bus."""
        self._handlers: dict[str, list[weakref.ReferenceType]] = {}
        self._cleanup_threshold = 10  # Clean up after this many operations
        self._operation_count = 0
        self._lock = threading.RLock()  # RLock for thread safety
        self._failed_handler_count = 0  # Track handler failures for monitoring
        self._last_errors: list[dict[str, Any]] = []  # Recent errors (max 10)

    def xǁEventBusǁ__init____mutmut_1(self) -> None:
        """Initialize empty event bus."""
        self._handlers: dict[str, list[weakref.ReferenceType]] = None
        self._cleanup_threshold = 10  # Clean up after this many operations
        self._operation_count = 0
        self._lock = threading.RLock()  # RLock for thread safety
        self._failed_handler_count = 0  # Track handler failures for monitoring
        self._last_errors: list[dict[str, Any]] = []  # Recent errors (max 10)

    def xǁEventBusǁ__init____mutmut_2(self) -> None:
        """Initialize empty event bus."""
        self._handlers: dict[str, list[weakref.ReferenceType]] = {}
        self._cleanup_threshold = None  # Clean up after this many operations
        self._operation_count = 0
        self._lock = threading.RLock()  # RLock for thread safety
        self._failed_handler_count = 0  # Track handler failures for monitoring
        self._last_errors: list[dict[str, Any]] = []  # Recent errors (max 10)

    def xǁEventBusǁ__init____mutmut_3(self) -> None:
        """Initialize empty event bus."""
        self._handlers: dict[str, list[weakref.ReferenceType]] = {}
        self._cleanup_threshold = 11  # Clean up after this many operations
        self._operation_count = 0
        self._lock = threading.RLock()  # RLock for thread safety
        self._failed_handler_count = 0  # Track handler failures for monitoring
        self._last_errors: list[dict[str, Any]] = []  # Recent errors (max 10)

    def xǁEventBusǁ__init____mutmut_4(self) -> None:
        """Initialize empty event bus."""
        self._handlers: dict[str, list[weakref.ReferenceType]] = {}
        self._cleanup_threshold = 10  # Clean up after this many operations
        self._operation_count = None
        self._lock = threading.RLock()  # RLock for thread safety
        self._failed_handler_count = 0  # Track handler failures for monitoring
        self._last_errors: list[dict[str, Any]] = []  # Recent errors (max 10)

    def xǁEventBusǁ__init____mutmut_5(self) -> None:
        """Initialize empty event bus."""
        self._handlers: dict[str, list[weakref.ReferenceType]] = {}
        self._cleanup_threshold = 10  # Clean up after this many operations
        self._operation_count = 1
        self._lock = threading.RLock()  # RLock for thread safety
        self._failed_handler_count = 0  # Track handler failures for monitoring
        self._last_errors: list[dict[str, Any]] = []  # Recent errors (max 10)

    def xǁEventBusǁ__init____mutmut_6(self) -> None:
        """Initialize empty event bus."""
        self._handlers: dict[str, list[weakref.ReferenceType]] = {}
        self._cleanup_threshold = 10  # Clean up after this many operations
        self._operation_count = 0
        self._lock = None  # RLock for thread safety
        self._failed_handler_count = 0  # Track handler failures for monitoring
        self._last_errors: list[dict[str, Any]] = []  # Recent errors (max 10)

    def xǁEventBusǁ__init____mutmut_7(self) -> None:
        """Initialize empty event bus."""
        self._handlers: dict[str, list[weakref.ReferenceType]] = {}
        self._cleanup_threshold = 10  # Clean up after this many operations
        self._operation_count = 0
        self._lock = threading.RLock()  # RLock for thread safety
        self._failed_handler_count = None  # Track handler failures for monitoring
        self._last_errors: list[dict[str, Any]] = []  # Recent errors (max 10)

    def xǁEventBusǁ__init____mutmut_8(self) -> None:
        """Initialize empty event bus."""
        self._handlers: dict[str, list[weakref.ReferenceType]] = {}
        self._cleanup_threshold = 10  # Clean up after this many operations
        self._operation_count = 0
        self._lock = threading.RLock()  # RLock for thread safety
        self._failed_handler_count = 1  # Track handler failures for monitoring
        self._last_errors: list[dict[str, Any]] = []  # Recent errors (max 10)

    def xǁEventBusǁ__init____mutmut_9(self) -> None:
        """Initialize empty event bus."""
        self._handlers: dict[str, list[weakref.ReferenceType]] = {}
        self._cleanup_threshold = 10  # Clean up after this many operations
        self._operation_count = 0
        self._lock = threading.RLock()  # RLock for thread safety
        self._failed_handler_count = 0  # Track handler failures for monitoring
        self._last_errors: list[dict[str, Any]] = None  # Recent errors (max 10)
    
    xǁEventBusǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEventBusǁ__init____mutmut_1': xǁEventBusǁ__init____mutmut_1, 
        'xǁEventBusǁ__init____mutmut_2': xǁEventBusǁ__init____mutmut_2, 
        'xǁEventBusǁ__init____mutmut_3': xǁEventBusǁ__init____mutmut_3, 
        'xǁEventBusǁ__init____mutmut_4': xǁEventBusǁ__init____mutmut_4, 
        'xǁEventBusǁ__init____mutmut_5': xǁEventBusǁ__init____mutmut_5, 
        'xǁEventBusǁ__init____mutmut_6': xǁEventBusǁ__init____mutmut_6, 
        'xǁEventBusǁ__init____mutmut_7': xǁEventBusǁ__init____mutmut_7, 
        'xǁEventBusǁ__init____mutmut_8': xǁEventBusǁ__init____mutmut_8, 
        'xǁEventBusǁ__init____mutmut_9': xǁEventBusǁ__init____mutmut_9
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEventBusǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁEventBusǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁEventBusǁ__init____mutmut_orig)
    xǁEventBusǁ__init____mutmut_orig.__name__ = 'xǁEventBusǁ__init__'

    def xǁEventBusǁsubscribe__mutmut_orig(self, event_name: str, handler: Callable[[Event], None]) -> None:
        """Subscribe to events by name.

        Args:
            event_name: Name of event to subscribe to
            handler: Function to call when event occurs
        """
        with self._lock:
            if event_name not in self._handlers:
                self._handlers[event_name] = []

            # Use weak reference to prevent memory leaks
            weak_handler = weakref.ref(handler)
            self._handlers[event_name].append(weak_handler)

    def xǁEventBusǁsubscribe__mutmut_1(self, event_name: str, handler: Callable[[Event], None]) -> None:
        """Subscribe to events by name.

        Args:
            event_name: Name of event to subscribe to
            handler: Function to call when event occurs
        """
        with self._lock:
            if event_name in self._handlers:
                self._handlers[event_name] = []

            # Use weak reference to prevent memory leaks
            weak_handler = weakref.ref(handler)
            self._handlers[event_name].append(weak_handler)

    def xǁEventBusǁsubscribe__mutmut_2(self, event_name: str, handler: Callable[[Event], None]) -> None:
        """Subscribe to events by name.

        Args:
            event_name: Name of event to subscribe to
            handler: Function to call when event occurs
        """
        with self._lock:
            if event_name not in self._handlers:
                self._handlers[event_name] = None

            # Use weak reference to prevent memory leaks
            weak_handler = weakref.ref(handler)
            self._handlers[event_name].append(weak_handler)

    def xǁEventBusǁsubscribe__mutmut_3(self, event_name: str, handler: Callable[[Event], None]) -> None:
        """Subscribe to events by name.

        Args:
            event_name: Name of event to subscribe to
            handler: Function to call when event occurs
        """
        with self._lock:
            if event_name not in self._handlers:
                self._handlers[event_name] = []

            # Use weak reference to prevent memory leaks
            weak_handler = None
            self._handlers[event_name].append(weak_handler)

    def xǁEventBusǁsubscribe__mutmut_4(self, event_name: str, handler: Callable[[Event], None]) -> None:
        """Subscribe to events by name.

        Args:
            event_name: Name of event to subscribe to
            handler: Function to call when event occurs
        """
        with self._lock:
            if event_name not in self._handlers:
                self._handlers[event_name] = []

            # Use weak reference to prevent memory leaks
            weak_handler = weakref.ref(None)
            self._handlers[event_name].append(weak_handler)

    def xǁEventBusǁsubscribe__mutmut_5(self, event_name: str, handler: Callable[[Event], None]) -> None:
        """Subscribe to events by name.

        Args:
            event_name: Name of event to subscribe to
            handler: Function to call when event occurs
        """
        with self._lock:
            if event_name not in self._handlers:
                self._handlers[event_name] = []

            # Use weak reference to prevent memory leaks
            weak_handler = weakref.ref(handler)
            self._handlers[event_name].append(None)
    
    xǁEventBusǁsubscribe__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEventBusǁsubscribe__mutmut_1': xǁEventBusǁsubscribe__mutmut_1, 
        'xǁEventBusǁsubscribe__mutmut_2': xǁEventBusǁsubscribe__mutmut_2, 
        'xǁEventBusǁsubscribe__mutmut_3': xǁEventBusǁsubscribe__mutmut_3, 
        'xǁEventBusǁsubscribe__mutmut_4': xǁEventBusǁsubscribe__mutmut_4, 
        'xǁEventBusǁsubscribe__mutmut_5': xǁEventBusǁsubscribe__mutmut_5
    }
    
    def subscribe(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEventBusǁsubscribe__mutmut_orig"), object.__getattribute__(self, "xǁEventBusǁsubscribe__mutmut_mutants"), args, kwargs, self)
        return result 
    
    subscribe.__signature__ = _mutmut_signature(xǁEventBusǁsubscribe__mutmut_orig)
    xǁEventBusǁsubscribe__mutmut_orig.__name__ = 'xǁEventBusǁsubscribe'

    def xǁEventBusǁemit__mutmut_orig(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_1(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_2(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = None
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_3(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = None
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_4(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_5(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(None)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_6(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(None)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_7(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(None, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_8(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, None, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_9(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, None)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_10(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_11(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_12(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, )

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_13(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = None

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_14(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count = 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_15(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count -= 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_16(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 2
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_17(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count > self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 0

    def xǁEventBusǁemit__mutmut_18(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = None

    def xǁEventBusǁemit__mutmut_19(self, event: Event | RegistryEvent) -> None:
        """Emit an event to all subscribers.

        Handler errors are logged but do not prevent other handlers from running.
        This ensures isolation - one failing handler doesn't break the entire event system.

        Args:
            event: Event to emit
        """
        with self._lock:
            if event.name not in self._handlers:
                return

            # Clean up dead references and call live handlers
            live_handlers = []
            for weak_handler in self._handlers[event.name]:
                handler = weak_handler()
                if handler is not None:
                    live_handlers.append(weak_handler)
                    try:
                        handler(event)
                    except Exception as e:
                        # Log error but continue processing other handlers
                        self._handle_handler_error(event, handler, e)

            # Update handler list with only live references
            self._handlers[event.name] = live_handlers

            # Periodic cleanup of all dead references
            self._operation_count += 1
            if self._operation_count >= self._cleanup_threshold:
                self._cleanup_dead_references()
                self._operation_count = 1
    
    xǁEventBusǁemit__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEventBusǁemit__mutmut_1': xǁEventBusǁemit__mutmut_1, 
        'xǁEventBusǁemit__mutmut_2': xǁEventBusǁemit__mutmut_2, 
        'xǁEventBusǁemit__mutmut_3': xǁEventBusǁemit__mutmut_3, 
        'xǁEventBusǁemit__mutmut_4': xǁEventBusǁemit__mutmut_4, 
        'xǁEventBusǁemit__mutmut_5': xǁEventBusǁemit__mutmut_5, 
        'xǁEventBusǁemit__mutmut_6': xǁEventBusǁemit__mutmut_6, 
        'xǁEventBusǁemit__mutmut_7': xǁEventBusǁemit__mutmut_7, 
        'xǁEventBusǁemit__mutmut_8': xǁEventBusǁemit__mutmut_8, 
        'xǁEventBusǁemit__mutmut_9': xǁEventBusǁemit__mutmut_9, 
        'xǁEventBusǁemit__mutmut_10': xǁEventBusǁemit__mutmut_10, 
        'xǁEventBusǁemit__mutmut_11': xǁEventBusǁemit__mutmut_11, 
        'xǁEventBusǁemit__mutmut_12': xǁEventBusǁemit__mutmut_12, 
        'xǁEventBusǁemit__mutmut_13': xǁEventBusǁemit__mutmut_13, 
        'xǁEventBusǁemit__mutmut_14': xǁEventBusǁemit__mutmut_14, 
        'xǁEventBusǁemit__mutmut_15': xǁEventBusǁemit__mutmut_15, 
        'xǁEventBusǁemit__mutmut_16': xǁEventBusǁemit__mutmut_16, 
        'xǁEventBusǁemit__mutmut_17': xǁEventBusǁemit__mutmut_17, 
        'xǁEventBusǁemit__mutmut_18': xǁEventBusǁemit__mutmut_18, 
        'xǁEventBusǁemit__mutmut_19': xǁEventBusǁemit__mutmut_19
    }
    
    def emit(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEventBusǁemit__mutmut_orig"), object.__getattribute__(self, "xǁEventBusǁemit__mutmut_mutants"), args, kwargs, self)
        return result 
    
    emit.__signature__ = _mutmut_signature(xǁEventBusǁemit__mutmut_orig)
    xǁEventBusǁemit__mutmut_orig.__name__ = 'xǁEventBusǁemit'

    def xǁEventBusǁ_handle_handler_error__mutmut_orig(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_1(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count = 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_2(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count -= 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_3(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 2

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_4(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = None

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_5(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(None, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_6(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, None, repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_7(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", None)

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_8(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr("__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_9(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_10(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", )

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_11(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "XX__name__XX", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_12(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__NAME__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_13(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(None))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_14(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = None

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_15(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "XXevent_nameXX": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_16(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "EVENT_NAME": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_17(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "XXhandlerXX": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_18(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "HANDLER": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_19(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "XXerror_typeXX": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_20(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "ERROR_TYPE": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_21(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(None).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_22(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "XXerror_messageXX": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_23(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "ERROR_MESSAGE": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_24(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(None),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_25(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "XXevent_sourceXX": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_26(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "EVENT_SOURCE": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_27(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(None, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_28(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, None, None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_29(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr("source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_30(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_31(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", ),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_32(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "XXsourceXX", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_33(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "SOURCE", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_34(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(None)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_35(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) >= 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_36(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 11:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_37(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(None)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_38(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(1)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_39(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            None
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_40(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(None).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=sys.stderr)

    def xǁEventBusǁ_handle_handler_error__mutmut_41(self, event: Event | RegistryEvent, handler: Callable, error: Exception) -> None:
        """Handle and log event handler errors.

        Args:
            event: The event being processed
            handler: The handler that failed
            error: The exception that occurred
        """
        self._failed_handler_count += 1

        # Get handler name for logging
        handler_name = getattr(handler, "__name__", repr(handler))

        # Record error details (keep last 10)
        error_record = {
            "event_name": event.name,
            "handler": handler_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "event_source": getattr(event, "source", None),
        }

        self._last_errors.append(error_record)
        if len(self._last_errors) > 10:
            self._last_errors.pop(0)

        # Log the error with full context
        # Use print to stderr to avoid circular dependency on logger
        # (EventBus is used BY the logger system, so we can't use logger here)
        import sys
        import traceback

        sys.stderr.write(
            f"ERROR: Event handler failed\n"
            f"  Event: {event.name}\n"
            f"  Handler: {handler_name}\n"
            f"  Error: {type(error).__name__}: {error}\n"
        )
        # Print traceback for debugging
        traceback.print_exc(file=None)
    
    xǁEventBusǁ_handle_handler_error__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEventBusǁ_handle_handler_error__mutmut_1': xǁEventBusǁ_handle_handler_error__mutmut_1, 
        'xǁEventBusǁ_handle_handler_error__mutmut_2': xǁEventBusǁ_handle_handler_error__mutmut_2, 
        'xǁEventBusǁ_handle_handler_error__mutmut_3': xǁEventBusǁ_handle_handler_error__mutmut_3, 
        'xǁEventBusǁ_handle_handler_error__mutmut_4': xǁEventBusǁ_handle_handler_error__mutmut_4, 
        'xǁEventBusǁ_handle_handler_error__mutmut_5': xǁEventBusǁ_handle_handler_error__mutmut_5, 
        'xǁEventBusǁ_handle_handler_error__mutmut_6': xǁEventBusǁ_handle_handler_error__mutmut_6, 
        'xǁEventBusǁ_handle_handler_error__mutmut_7': xǁEventBusǁ_handle_handler_error__mutmut_7, 
        'xǁEventBusǁ_handle_handler_error__mutmut_8': xǁEventBusǁ_handle_handler_error__mutmut_8, 
        'xǁEventBusǁ_handle_handler_error__mutmut_9': xǁEventBusǁ_handle_handler_error__mutmut_9, 
        'xǁEventBusǁ_handle_handler_error__mutmut_10': xǁEventBusǁ_handle_handler_error__mutmut_10, 
        'xǁEventBusǁ_handle_handler_error__mutmut_11': xǁEventBusǁ_handle_handler_error__mutmut_11, 
        'xǁEventBusǁ_handle_handler_error__mutmut_12': xǁEventBusǁ_handle_handler_error__mutmut_12, 
        'xǁEventBusǁ_handle_handler_error__mutmut_13': xǁEventBusǁ_handle_handler_error__mutmut_13, 
        'xǁEventBusǁ_handle_handler_error__mutmut_14': xǁEventBusǁ_handle_handler_error__mutmut_14, 
        'xǁEventBusǁ_handle_handler_error__mutmut_15': xǁEventBusǁ_handle_handler_error__mutmut_15, 
        'xǁEventBusǁ_handle_handler_error__mutmut_16': xǁEventBusǁ_handle_handler_error__mutmut_16, 
        'xǁEventBusǁ_handle_handler_error__mutmut_17': xǁEventBusǁ_handle_handler_error__mutmut_17, 
        'xǁEventBusǁ_handle_handler_error__mutmut_18': xǁEventBusǁ_handle_handler_error__mutmut_18, 
        'xǁEventBusǁ_handle_handler_error__mutmut_19': xǁEventBusǁ_handle_handler_error__mutmut_19, 
        'xǁEventBusǁ_handle_handler_error__mutmut_20': xǁEventBusǁ_handle_handler_error__mutmut_20, 
        'xǁEventBusǁ_handle_handler_error__mutmut_21': xǁEventBusǁ_handle_handler_error__mutmut_21, 
        'xǁEventBusǁ_handle_handler_error__mutmut_22': xǁEventBusǁ_handle_handler_error__mutmut_22, 
        'xǁEventBusǁ_handle_handler_error__mutmut_23': xǁEventBusǁ_handle_handler_error__mutmut_23, 
        'xǁEventBusǁ_handle_handler_error__mutmut_24': xǁEventBusǁ_handle_handler_error__mutmut_24, 
        'xǁEventBusǁ_handle_handler_error__mutmut_25': xǁEventBusǁ_handle_handler_error__mutmut_25, 
        'xǁEventBusǁ_handle_handler_error__mutmut_26': xǁEventBusǁ_handle_handler_error__mutmut_26, 
        'xǁEventBusǁ_handle_handler_error__mutmut_27': xǁEventBusǁ_handle_handler_error__mutmut_27, 
        'xǁEventBusǁ_handle_handler_error__mutmut_28': xǁEventBusǁ_handle_handler_error__mutmut_28, 
        'xǁEventBusǁ_handle_handler_error__mutmut_29': xǁEventBusǁ_handle_handler_error__mutmut_29, 
        'xǁEventBusǁ_handle_handler_error__mutmut_30': xǁEventBusǁ_handle_handler_error__mutmut_30, 
        'xǁEventBusǁ_handle_handler_error__mutmut_31': xǁEventBusǁ_handle_handler_error__mutmut_31, 
        'xǁEventBusǁ_handle_handler_error__mutmut_32': xǁEventBusǁ_handle_handler_error__mutmut_32, 
        'xǁEventBusǁ_handle_handler_error__mutmut_33': xǁEventBusǁ_handle_handler_error__mutmut_33, 
        'xǁEventBusǁ_handle_handler_error__mutmut_34': xǁEventBusǁ_handle_handler_error__mutmut_34, 
        'xǁEventBusǁ_handle_handler_error__mutmut_35': xǁEventBusǁ_handle_handler_error__mutmut_35, 
        'xǁEventBusǁ_handle_handler_error__mutmut_36': xǁEventBusǁ_handle_handler_error__mutmut_36, 
        'xǁEventBusǁ_handle_handler_error__mutmut_37': xǁEventBusǁ_handle_handler_error__mutmut_37, 
        'xǁEventBusǁ_handle_handler_error__mutmut_38': xǁEventBusǁ_handle_handler_error__mutmut_38, 
        'xǁEventBusǁ_handle_handler_error__mutmut_39': xǁEventBusǁ_handle_handler_error__mutmut_39, 
        'xǁEventBusǁ_handle_handler_error__mutmut_40': xǁEventBusǁ_handle_handler_error__mutmut_40, 
        'xǁEventBusǁ_handle_handler_error__mutmut_41': xǁEventBusǁ_handle_handler_error__mutmut_41
    }
    
    def _handle_handler_error(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEventBusǁ_handle_handler_error__mutmut_orig"), object.__getattribute__(self, "xǁEventBusǁ_handle_handler_error__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _handle_handler_error.__signature__ = _mutmut_signature(xǁEventBusǁ_handle_handler_error__mutmut_orig)
    xǁEventBusǁ_handle_handler_error__mutmut_orig.__name__ = 'xǁEventBusǁ_handle_handler_error'

    def xǁEventBusǁunsubscribe__mutmut_orig(self, event_name: str, handler: Callable[[Event], None]) -> None:
        """Unsubscribe from events.

        Args:
            event_name: Name of event to unsubscribe from
            handler: Handler function to remove
        """
        with self._lock:
            if event_name not in self._handlers:
                return

            # Remove handler by comparing actual functions
            self._handlers[event_name] = [
                weak_ref for weak_ref in self._handlers[event_name] if weak_ref() is not handler
            ]

    def xǁEventBusǁunsubscribe__mutmut_1(self, event_name: str, handler: Callable[[Event], None]) -> None:
        """Unsubscribe from events.

        Args:
            event_name: Name of event to unsubscribe from
            handler: Handler function to remove
        """
        with self._lock:
            if event_name in self._handlers:
                return

            # Remove handler by comparing actual functions
            self._handlers[event_name] = [
                weak_ref for weak_ref in self._handlers[event_name] if weak_ref() is not handler
            ]

    def xǁEventBusǁunsubscribe__mutmut_2(self, event_name: str, handler: Callable[[Event], None]) -> None:
        """Unsubscribe from events.

        Args:
            event_name: Name of event to unsubscribe from
            handler: Handler function to remove
        """
        with self._lock:
            if event_name not in self._handlers:
                return

            # Remove handler by comparing actual functions
            self._handlers[event_name] = None

    def xǁEventBusǁunsubscribe__mutmut_3(self, event_name: str, handler: Callable[[Event], None]) -> None:
        """Unsubscribe from events.

        Args:
            event_name: Name of event to unsubscribe from
            handler: Handler function to remove
        """
        with self._lock:
            if event_name not in self._handlers:
                return

            # Remove handler by comparing actual functions
            self._handlers[event_name] = [
                weak_ref for weak_ref in self._handlers[event_name] if weak_ref() is handler
            ]
    
    xǁEventBusǁunsubscribe__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEventBusǁunsubscribe__mutmut_1': xǁEventBusǁunsubscribe__mutmut_1, 
        'xǁEventBusǁunsubscribe__mutmut_2': xǁEventBusǁunsubscribe__mutmut_2, 
        'xǁEventBusǁunsubscribe__mutmut_3': xǁEventBusǁunsubscribe__mutmut_3
    }
    
    def unsubscribe(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEventBusǁunsubscribe__mutmut_orig"), object.__getattribute__(self, "xǁEventBusǁunsubscribe__mutmut_mutants"), args, kwargs, self)
        return result 
    
    unsubscribe.__signature__ = _mutmut_signature(xǁEventBusǁunsubscribe__mutmut_orig)
    xǁEventBusǁunsubscribe__mutmut_orig.__name__ = 'xǁEventBusǁunsubscribe'

    def xǁEventBusǁ_cleanup_dead_references__mutmut_orig(self) -> None:
        """Clean up all dead weak references across all event types."""
        for event_name in list(self._handlers.keys()):
            live_handlers = []
            for weak_handler in self._handlers[event_name]:
                if weak_handler() is not None:
                    live_handlers.append(weak_handler)

            if live_handlers:
                self._handlers[event_name] = live_handlers
            else:
                # Remove empty event lists
                del self._handlers[event_name]

    def xǁEventBusǁ_cleanup_dead_references__mutmut_1(self) -> None:
        """Clean up all dead weak references across all event types."""
        for event_name in list(None):
            live_handlers = []
            for weak_handler in self._handlers[event_name]:
                if weak_handler() is not None:
                    live_handlers.append(weak_handler)

            if live_handlers:
                self._handlers[event_name] = live_handlers
            else:
                # Remove empty event lists
                del self._handlers[event_name]

    def xǁEventBusǁ_cleanup_dead_references__mutmut_2(self) -> None:
        """Clean up all dead weak references across all event types."""
        for event_name in list(self._handlers.keys()):
            live_handlers = None
            for weak_handler in self._handlers[event_name]:
                if weak_handler() is not None:
                    live_handlers.append(weak_handler)

            if live_handlers:
                self._handlers[event_name] = live_handlers
            else:
                # Remove empty event lists
                del self._handlers[event_name]

    def xǁEventBusǁ_cleanup_dead_references__mutmut_3(self) -> None:
        """Clean up all dead weak references across all event types."""
        for event_name in list(self._handlers.keys()):
            live_handlers = []
            for weak_handler in self._handlers[event_name]:
                if weak_handler() is None:
                    live_handlers.append(weak_handler)

            if live_handlers:
                self._handlers[event_name] = live_handlers
            else:
                # Remove empty event lists
                del self._handlers[event_name]

    def xǁEventBusǁ_cleanup_dead_references__mutmut_4(self) -> None:
        """Clean up all dead weak references across all event types."""
        for event_name in list(self._handlers.keys()):
            live_handlers = []
            for weak_handler in self._handlers[event_name]:
                if weak_handler() is not None:
                    live_handlers.append(None)

            if live_handlers:
                self._handlers[event_name] = live_handlers
            else:
                # Remove empty event lists
                del self._handlers[event_name]

    def xǁEventBusǁ_cleanup_dead_references__mutmut_5(self) -> None:
        """Clean up all dead weak references across all event types."""
        for event_name in list(self._handlers.keys()):
            live_handlers = []
            for weak_handler in self._handlers[event_name]:
                if weak_handler() is not None:
                    live_handlers.append(weak_handler)

            if live_handlers:
                self._handlers[event_name] = None
            else:
                # Remove empty event lists
                del self._handlers[event_name]
    
    xǁEventBusǁ_cleanup_dead_references__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEventBusǁ_cleanup_dead_references__mutmut_1': xǁEventBusǁ_cleanup_dead_references__mutmut_1, 
        'xǁEventBusǁ_cleanup_dead_references__mutmut_2': xǁEventBusǁ_cleanup_dead_references__mutmut_2, 
        'xǁEventBusǁ_cleanup_dead_references__mutmut_3': xǁEventBusǁ_cleanup_dead_references__mutmut_3, 
        'xǁEventBusǁ_cleanup_dead_references__mutmut_4': xǁEventBusǁ_cleanup_dead_references__mutmut_4, 
        'xǁEventBusǁ_cleanup_dead_references__mutmut_5': xǁEventBusǁ_cleanup_dead_references__mutmut_5
    }
    
    def _cleanup_dead_references(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEventBusǁ_cleanup_dead_references__mutmut_orig"), object.__getattribute__(self, "xǁEventBusǁ_cleanup_dead_references__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _cleanup_dead_references.__signature__ = _mutmut_signature(xǁEventBusǁ_cleanup_dead_references__mutmut_orig)
    xǁEventBusǁ_cleanup_dead_references__mutmut_orig.__name__ = 'xǁEventBusǁ_cleanup_dead_references'

    def xǁEventBusǁget_memory_stats__mutmut_orig(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_1(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = None
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_2(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 1
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_3(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = None

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_4(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 1

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_5(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers = 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_6(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers -= 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_7(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 2
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_8(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is not None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_9(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers = 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_10(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers -= 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_11(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 2

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_12(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "XXevent_typesXX": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_13(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "EVENT_TYPES": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_14(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "XXtotal_handlersXX": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_15(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "TOTAL_HANDLERS": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_16(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "XXlive_handlersXX": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_17(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "LIVE_HANDLERS": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_18(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers + dead_handlers,
                "dead_handlers": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_19(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "XXdead_handlersXX": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_20(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "DEAD_HANDLERS": dead_handlers,
                "operation_count": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_21(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "XXoperation_countXX": self._operation_count,
            }

    def xǁEventBusǁget_memory_stats__mutmut_22(self) -> dict[str, Any]:
        """Get memory usage statistics for the event bus."""
        with self._lock:
            total_handlers = 0
            dead_handlers = 0

            for handlers in self._handlers.values():
                for weak_handler in handlers:
                    total_handlers += 1
                    if weak_handler() is None:
                        dead_handlers += 1

            return {
                "event_types": len(self._handlers),
                "total_handlers": total_handlers,
                "live_handlers": total_handlers - dead_handlers,
                "dead_handlers": dead_handlers,
                "OPERATION_COUNT": self._operation_count,
            }
    
    xǁEventBusǁget_memory_stats__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEventBusǁget_memory_stats__mutmut_1': xǁEventBusǁget_memory_stats__mutmut_1, 
        'xǁEventBusǁget_memory_stats__mutmut_2': xǁEventBusǁget_memory_stats__mutmut_2, 
        'xǁEventBusǁget_memory_stats__mutmut_3': xǁEventBusǁget_memory_stats__mutmut_3, 
        'xǁEventBusǁget_memory_stats__mutmut_4': xǁEventBusǁget_memory_stats__mutmut_4, 
        'xǁEventBusǁget_memory_stats__mutmut_5': xǁEventBusǁget_memory_stats__mutmut_5, 
        'xǁEventBusǁget_memory_stats__mutmut_6': xǁEventBusǁget_memory_stats__mutmut_6, 
        'xǁEventBusǁget_memory_stats__mutmut_7': xǁEventBusǁget_memory_stats__mutmut_7, 
        'xǁEventBusǁget_memory_stats__mutmut_8': xǁEventBusǁget_memory_stats__mutmut_8, 
        'xǁEventBusǁget_memory_stats__mutmut_9': xǁEventBusǁget_memory_stats__mutmut_9, 
        'xǁEventBusǁget_memory_stats__mutmut_10': xǁEventBusǁget_memory_stats__mutmut_10, 
        'xǁEventBusǁget_memory_stats__mutmut_11': xǁEventBusǁget_memory_stats__mutmut_11, 
        'xǁEventBusǁget_memory_stats__mutmut_12': xǁEventBusǁget_memory_stats__mutmut_12, 
        'xǁEventBusǁget_memory_stats__mutmut_13': xǁEventBusǁget_memory_stats__mutmut_13, 
        'xǁEventBusǁget_memory_stats__mutmut_14': xǁEventBusǁget_memory_stats__mutmut_14, 
        'xǁEventBusǁget_memory_stats__mutmut_15': xǁEventBusǁget_memory_stats__mutmut_15, 
        'xǁEventBusǁget_memory_stats__mutmut_16': xǁEventBusǁget_memory_stats__mutmut_16, 
        'xǁEventBusǁget_memory_stats__mutmut_17': xǁEventBusǁget_memory_stats__mutmut_17, 
        'xǁEventBusǁget_memory_stats__mutmut_18': xǁEventBusǁget_memory_stats__mutmut_18, 
        'xǁEventBusǁget_memory_stats__mutmut_19': xǁEventBusǁget_memory_stats__mutmut_19, 
        'xǁEventBusǁget_memory_stats__mutmut_20': xǁEventBusǁget_memory_stats__mutmut_20, 
        'xǁEventBusǁget_memory_stats__mutmut_21': xǁEventBusǁget_memory_stats__mutmut_21, 
        'xǁEventBusǁget_memory_stats__mutmut_22': xǁEventBusǁget_memory_stats__mutmut_22
    }
    
    def get_memory_stats(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEventBusǁget_memory_stats__mutmut_orig"), object.__getattribute__(self, "xǁEventBusǁget_memory_stats__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_memory_stats.__signature__ = _mutmut_signature(xǁEventBusǁget_memory_stats__mutmut_orig)
    xǁEventBusǁget_memory_stats__mutmut_orig.__name__ = 'xǁEventBusǁget_memory_stats'

    def xǁEventBusǁget_error_stats__mutmut_orig(self) -> dict[str, Any]:
        """Get error statistics for monitoring handler failures.

        Returns:
            Dictionary with error statistics including:
            - failed_handler_count: Total number of handler failures
            - recent_errors: List of recent error details (max 10)
        """
        with self._lock:
            return {
                "failed_handler_count": self._failed_handler_count,
                "recent_errors": self._last_errors.copy(),
            }

    def xǁEventBusǁget_error_stats__mutmut_1(self) -> dict[str, Any]:
        """Get error statistics for monitoring handler failures.

        Returns:
            Dictionary with error statistics including:
            - failed_handler_count: Total number of handler failures
            - recent_errors: List of recent error details (max 10)
        """
        with self._lock:
            return {
                "XXfailed_handler_countXX": self._failed_handler_count,
                "recent_errors": self._last_errors.copy(),
            }

    def xǁEventBusǁget_error_stats__mutmut_2(self) -> dict[str, Any]:
        """Get error statistics for monitoring handler failures.

        Returns:
            Dictionary with error statistics including:
            - failed_handler_count: Total number of handler failures
            - recent_errors: List of recent error details (max 10)
        """
        with self._lock:
            return {
                "FAILED_HANDLER_COUNT": self._failed_handler_count,
                "recent_errors": self._last_errors.copy(),
            }

    def xǁEventBusǁget_error_stats__mutmut_3(self) -> dict[str, Any]:
        """Get error statistics for monitoring handler failures.

        Returns:
            Dictionary with error statistics including:
            - failed_handler_count: Total number of handler failures
            - recent_errors: List of recent error details (max 10)
        """
        with self._lock:
            return {
                "failed_handler_count": self._failed_handler_count,
                "XXrecent_errorsXX": self._last_errors.copy(),
            }

    def xǁEventBusǁget_error_stats__mutmut_4(self) -> dict[str, Any]:
        """Get error statistics for monitoring handler failures.

        Returns:
            Dictionary with error statistics including:
            - failed_handler_count: Total number of handler failures
            - recent_errors: List of recent error details (max 10)
        """
        with self._lock:
            return {
                "failed_handler_count": self._failed_handler_count,
                "RECENT_ERRORS": self._last_errors.copy(),
            }
    
    xǁEventBusǁget_error_stats__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEventBusǁget_error_stats__mutmut_1': xǁEventBusǁget_error_stats__mutmut_1, 
        'xǁEventBusǁget_error_stats__mutmut_2': xǁEventBusǁget_error_stats__mutmut_2, 
        'xǁEventBusǁget_error_stats__mutmut_3': xǁEventBusǁget_error_stats__mutmut_3, 
        'xǁEventBusǁget_error_stats__mutmut_4': xǁEventBusǁget_error_stats__mutmut_4
    }
    
    def get_error_stats(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEventBusǁget_error_stats__mutmut_orig"), object.__getattribute__(self, "xǁEventBusǁget_error_stats__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_error_stats.__signature__ = _mutmut_signature(xǁEventBusǁget_error_stats__mutmut_orig)
    xǁEventBusǁget_error_stats__mutmut_orig.__name__ = 'xǁEventBusǁget_error_stats'

    def xǁEventBusǁforce_cleanup__mutmut_orig(self) -> None:
        """Force immediate cleanup of all dead references."""
        with self._lock:
            self._cleanup_dead_references()
            self._operation_count = 0

    def xǁEventBusǁforce_cleanup__mutmut_1(self) -> None:
        """Force immediate cleanup of all dead references."""
        with self._lock:
            self._cleanup_dead_references()
            self._operation_count = None

    def xǁEventBusǁforce_cleanup__mutmut_2(self) -> None:
        """Force immediate cleanup of all dead references."""
        with self._lock:
            self._cleanup_dead_references()
            self._operation_count = 1
    
    xǁEventBusǁforce_cleanup__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEventBusǁforce_cleanup__mutmut_1': xǁEventBusǁforce_cleanup__mutmut_1, 
        'xǁEventBusǁforce_cleanup__mutmut_2': xǁEventBusǁforce_cleanup__mutmut_2
    }
    
    def force_cleanup(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEventBusǁforce_cleanup__mutmut_orig"), object.__getattribute__(self, "xǁEventBusǁforce_cleanup__mutmut_mutants"), args, kwargs, self)
        return result 
    
    force_cleanup.__signature__ = _mutmut_signature(xǁEventBusǁforce_cleanup__mutmut_orig)
    xǁEventBusǁforce_cleanup__mutmut_orig.__name__ = 'xǁEventBusǁforce_cleanup'

    def xǁEventBusǁclear__mutmut_orig(self) -> None:
        """Clear all event subscriptions.

        This is primarily used during test resets to prevent duplicate
        event handlers from accumulating across test runs.
        """
        with self._lock:
            self._handlers.clear()
            self._operation_count = 0
            self._failed_handler_count = 0
            self._last_errors.clear()

    def xǁEventBusǁclear__mutmut_1(self) -> None:
        """Clear all event subscriptions.

        This is primarily used during test resets to prevent duplicate
        event handlers from accumulating across test runs.
        """
        with self._lock:
            self._handlers.clear()
            self._operation_count = None
            self._failed_handler_count = 0
            self._last_errors.clear()

    def xǁEventBusǁclear__mutmut_2(self) -> None:
        """Clear all event subscriptions.

        This is primarily used during test resets to prevent duplicate
        event handlers from accumulating across test runs.
        """
        with self._lock:
            self._handlers.clear()
            self._operation_count = 1
            self._failed_handler_count = 0
            self._last_errors.clear()

    def xǁEventBusǁclear__mutmut_3(self) -> None:
        """Clear all event subscriptions.

        This is primarily used during test resets to prevent duplicate
        event handlers from accumulating across test runs.
        """
        with self._lock:
            self._handlers.clear()
            self._operation_count = 0
            self._failed_handler_count = None
            self._last_errors.clear()

    def xǁEventBusǁclear__mutmut_4(self) -> None:
        """Clear all event subscriptions.

        This is primarily used during test resets to prevent duplicate
        event handlers from accumulating across test runs.
        """
        with self._lock:
            self._handlers.clear()
            self._operation_count = 0
            self._failed_handler_count = 1
            self._last_errors.clear()
    
    xǁEventBusǁclear__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEventBusǁclear__mutmut_1': xǁEventBusǁclear__mutmut_1, 
        'xǁEventBusǁclear__mutmut_2': xǁEventBusǁclear__mutmut_2, 
        'xǁEventBusǁclear__mutmut_3': xǁEventBusǁclear__mutmut_3, 
        'xǁEventBusǁclear__mutmut_4': xǁEventBusǁclear__mutmut_4
    }
    
    def clear(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEventBusǁclear__mutmut_orig"), object.__getattribute__(self, "xǁEventBusǁclear__mutmut_mutants"), args, kwargs, self)
        return result 
    
    clear.__signature__ = _mutmut_signature(xǁEventBusǁclear__mutmut_orig)
    xǁEventBusǁclear__mutmut_orig.__name__ = 'xǁEventBusǁclear'


# Global event bus instance
_event_bus = EventBus()


def get_event_bus() -> EventBus:
    """Get the global event bus instance."""
    return _event_bus


def x_emit_registry_event__mutmut_orig(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        operation=operation,
        item_name=item_name,
        dimension=dimension,
        data=kwargs,
        source="registry",
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_1(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = None
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_2(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name=None,  # Will be set by __attrs_post_init__
        operation=operation,
        item_name=item_name,
        dimension=dimension,
        data=kwargs,
        source="registry",
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_3(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        operation=None,
        item_name=item_name,
        dimension=dimension,
        data=kwargs,
        source="registry",
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_4(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        operation=operation,
        item_name=None,
        dimension=dimension,
        data=kwargs,
        source="registry",
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_5(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        operation=operation,
        item_name=item_name,
        dimension=None,
        data=kwargs,
        source="registry",
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_6(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        operation=operation,
        item_name=item_name,
        dimension=dimension,
        data=None,
        source="registry",
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_7(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        operation=operation,
        item_name=item_name,
        dimension=dimension,
        data=kwargs,
        source=None,
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_8(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        operation=operation,
        item_name=item_name,
        dimension=dimension,
        data=kwargs,
        source="registry",
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_9(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        item_name=item_name,
        dimension=dimension,
        data=kwargs,
        source="registry",
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_10(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        operation=operation,
        dimension=dimension,
        data=kwargs,
        source="registry",
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_11(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        operation=operation,
        item_name=item_name,
        data=kwargs,
        source="registry",
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_12(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        operation=operation,
        item_name=item_name,
        dimension=dimension,
        source="registry",
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_13(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        operation=operation,
        item_name=item_name,
        dimension=dimension,
        data=kwargs,
        )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_14(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="XXXX",  # Will be set by __attrs_post_init__
        operation=operation,
        item_name=item_name,
        dimension=dimension,
        data=kwargs,
        source="registry",
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_15(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        operation=operation,
        item_name=item_name,
        dimension=dimension,
        data=kwargs,
        source="XXregistryXX",
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_16(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        operation=operation,
        item_name=item_name,
        dimension=dimension,
        data=kwargs,
        source="REGISTRY",
    )
    _event_bus.emit(event)


def x_emit_registry_event__mutmut_17(operation: str, item_name: str, dimension: str, **kwargs: Any) -> None:
    """Emit a registry operation event.

    Args:
        operation: Type of operation (register, remove, etc.)
        item_name: Name of the registry item
        dimension: Registry dimension
        **kwargs: Additional event data
    """
    event = RegistryEvent(
        name="",  # Will be set by __attrs_post_init__
        operation=operation,
        item_name=item_name,
        dimension=dimension,
        data=kwargs,
        source="registry",
    )
    _event_bus.emit(None)

x_emit_registry_event__mutmut_mutants : ClassVar[MutantDict] = {
'x_emit_registry_event__mutmut_1': x_emit_registry_event__mutmut_1, 
    'x_emit_registry_event__mutmut_2': x_emit_registry_event__mutmut_2, 
    'x_emit_registry_event__mutmut_3': x_emit_registry_event__mutmut_3, 
    'x_emit_registry_event__mutmut_4': x_emit_registry_event__mutmut_4, 
    'x_emit_registry_event__mutmut_5': x_emit_registry_event__mutmut_5, 
    'x_emit_registry_event__mutmut_6': x_emit_registry_event__mutmut_6, 
    'x_emit_registry_event__mutmut_7': x_emit_registry_event__mutmut_7, 
    'x_emit_registry_event__mutmut_8': x_emit_registry_event__mutmut_8, 
    'x_emit_registry_event__mutmut_9': x_emit_registry_event__mutmut_9, 
    'x_emit_registry_event__mutmut_10': x_emit_registry_event__mutmut_10, 
    'x_emit_registry_event__mutmut_11': x_emit_registry_event__mutmut_11, 
    'x_emit_registry_event__mutmut_12': x_emit_registry_event__mutmut_12, 
    'x_emit_registry_event__mutmut_13': x_emit_registry_event__mutmut_13, 
    'x_emit_registry_event__mutmut_14': x_emit_registry_event__mutmut_14, 
    'x_emit_registry_event__mutmut_15': x_emit_registry_event__mutmut_15, 
    'x_emit_registry_event__mutmut_16': x_emit_registry_event__mutmut_16, 
    'x_emit_registry_event__mutmut_17': x_emit_registry_event__mutmut_17
}

def emit_registry_event(*args, **kwargs):
    result = _mutmut_trampoline(x_emit_registry_event__mutmut_orig, x_emit_registry_event__mutmut_mutants, args, kwargs)
    return result 

emit_registry_event.__signature__ = _mutmut_signature(x_emit_registry_event__mutmut_orig)
x_emit_registry_event__mutmut_orig.__name__ = 'x_emit_registry_event'


__all__ = ["Event", "EventBus", "RegistryEvent", "emit_registry_event", "get_event_bus"]


# <3 🧱🤝🌐🪄
