# provide/foundation/eventsets/registry.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import importlib
from pathlib import Path
import pkgutil

from provide.foundation.errors.resources import AlreadyExistsError, NotFoundError
from provide.foundation.eventsets.types import EventSet
from provide.foundation.hub.registry import Registry
from provide.foundation.logger.setup.coordinator import (
    create_foundation_internal_logger,
)

"""Event set registry and discovery."""

# Bootstrap logger that doesn't trigger full logger setup
logger = create_foundation_internal_logger()
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


class EventSetRegistry(Registry):
    """Registry for event set definitions using foundation Registry.

    Extends the foundation Registry to provide specialized
    methods for event set registration and discovery.
    """

    def xǁEventSetRegistryǁregister_event_set__mutmut_orig(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_1(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                None,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_2(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                None,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_3(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                None,
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_4(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata=None,
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_5(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_6(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_7(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_8(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_9(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "XXeventsetXX",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_10(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "EVENTSET",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_11(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"XXpriorityXX": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_12(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"PRIORITY": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_13(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                None,
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_14(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=None,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_15(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=None,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_16(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=None,
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_17(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=None,
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_18(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_19(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_20(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_21(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_22(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_23(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "XXRegistered event setXX",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_24(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_25(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "REGISTERED EVENT SET",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_26(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace(None, name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_27(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("Event set already registered", name=None)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_28(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace(name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_29(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace(
                "Event set already registered",
            )
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_30(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("XXEvent set already registeredXX", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_31(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("event set already registered", name=event_set.name)
            raise

    def xǁEventSetRegistryǁregister_event_set__mutmut_32(self, event_set: EventSet) -> None:
        """Register an event set definition.

        Args:
            event_set: The EventSet to register

        Raises:
            AlreadyExistsError: If an event set with this name already exists

        """
        try:
            self.register(
                event_set.name,
                event_set,
                "eventset",
                metadata={"priority": event_set.priority},
            )
            logger.debug(
                "Registered event set",
                name=event_set.name,
                priority=event_set.priority,
                field_count=len(event_set.field_mappings),
                mapping_count=len(event_set.mappings),
            )
        except AlreadyExistsError:
            logger.trace("EVENT SET ALREADY REGISTERED", name=event_set.name)
            raise

    xǁEventSetRegistryǁregister_event_set__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEventSetRegistryǁregister_event_set__mutmut_1": xǁEventSetRegistryǁregister_event_set__mutmut_1,
        "xǁEventSetRegistryǁregister_event_set__mutmut_2": xǁEventSetRegistryǁregister_event_set__mutmut_2,
        "xǁEventSetRegistryǁregister_event_set__mutmut_3": xǁEventSetRegistryǁregister_event_set__mutmut_3,
        "xǁEventSetRegistryǁregister_event_set__mutmut_4": xǁEventSetRegistryǁregister_event_set__mutmut_4,
        "xǁEventSetRegistryǁregister_event_set__mutmut_5": xǁEventSetRegistryǁregister_event_set__mutmut_5,
        "xǁEventSetRegistryǁregister_event_set__mutmut_6": xǁEventSetRegistryǁregister_event_set__mutmut_6,
        "xǁEventSetRegistryǁregister_event_set__mutmut_7": xǁEventSetRegistryǁregister_event_set__mutmut_7,
        "xǁEventSetRegistryǁregister_event_set__mutmut_8": xǁEventSetRegistryǁregister_event_set__mutmut_8,
        "xǁEventSetRegistryǁregister_event_set__mutmut_9": xǁEventSetRegistryǁregister_event_set__mutmut_9,
        "xǁEventSetRegistryǁregister_event_set__mutmut_10": xǁEventSetRegistryǁregister_event_set__mutmut_10,
        "xǁEventSetRegistryǁregister_event_set__mutmut_11": xǁEventSetRegistryǁregister_event_set__mutmut_11,
        "xǁEventSetRegistryǁregister_event_set__mutmut_12": xǁEventSetRegistryǁregister_event_set__mutmut_12,
        "xǁEventSetRegistryǁregister_event_set__mutmut_13": xǁEventSetRegistryǁregister_event_set__mutmut_13,
        "xǁEventSetRegistryǁregister_event_set__mutmut_14": xǁEventSetRegistryǁregister_event_set__mutmut_14,
        "xǁEventSetRegistryǁregister_event_set__mutmut_15": xǁEventSetRegistryǁregister_event_set__mutmut_15,
        "xǁEventSetRegistryǁregister_event_set__mutmut_16": xǁEventSetRegistryǁregister_event_set__mutmut_16,
        "xǁEventSetRegistryǁregister_event_set__mutmut_17": xǁEventSetRegistryǁregister_event_set__mutmut_17,
        "xǁEventSetRegistryǁregister_event_set__mutmut_18": xǁEventSetRegistryǁregister_event_set__mutmut_18,
        "xǁEventSetRegistryǁregister_event_set__mutmut_19": xǁEventSetRegistryǁregister_event_set__mutmut_19,
        "xǁEventSetRegistryǁregister_event_set__mutmut_20": xǁEventSetRegistryǁregister_event_set__mutmut_20,
        "xǁEventSetRegistryǁregister_event_set__mutmut_21": xǁEventSetRegistryǁregister_event_set__mutmut_21,
        "xǁEventSetRegistryǁregister_event_set__mutmut_22": xǁEventSetRegistryǁregister_event_set__mutmut_22,
        "xǁEventSetRegistryǁregister_event_set__mutmut_23": xǁEventSetRegistryǁregister_event_set__mutmut_23,
        "xǁEventSetRegistryǁregister_event_set__mutmut_24": xǁEventSetRegistryǁregister_event_set__mutmut_24,
        "xǁEventSetRegistryǁregister_event_set__mutmut_25": xǁEventSetRegistryǁregister_event_set__mutmut_25,
        "xǁEventSetRegistryǁregister_event_set__mutmut_26": xǁEventSetRegistryǁregister_event_set__mutmut_26,
        "xǁEventSetRegistryǁregister_event_set__mutmut_27": xǁEventSetRegistryǁregister_event_set__mutmut_27,
        "xǁEventSetRegistryǁregister_event_set__mutmut_28": xǁEventSetRegistryǁregister_event_set__mutmut_28,
        "xǁEventSetRegistryǁregister_event_set__mutmut_29": xǁEventSetRegistryǁregister_event_set__mutmut_29,
        "xǁEventSetRegistryǁregister_event_set__mutmut_30": xǁEventSetRegistryǁregister_event_set__mutmut_30,
        "xǁEventSetRegistryǁregister_event_set__mutmut_31": xǁEventSetRegistryǁregister_event_set__mutmut_31,
        "xǁEventSetRegistryǁregister_event_set__mutmut_32": xǁEventSetRegistryǁregister_event_set__mutmut_32,
    }

    def register_event_set(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEventSetRegistryǁregister_event_set__mutmut_orig"),
            object.__getattribute__(self, "xǁEventSetRegistryǁregister_event_set__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    register_event_set.__signature__ = _mutmut_signature(xǁEventSetRegistryǁregister_event_set__mutmut_orig)
    xǁEventSetRegistryǁregister_event_set__mutmut_orig.__name__ = "xǁEventSetRegistryǁregister_event_set"

    def xǁEventSetRegistryǁget_event_set__mutmut_orig(self, name: str) -> EventSet:
        """Retrieve an event set by name.

        Args:
            name: The name of the event set

        Returns:
            The EventSet

        Raises:
            NotFoundError: If no event set with this name exists

        """
        event_set = self.get(name, "eventset")
        if event_set is None:
            raise NotFoundError(f"Event set '{name}' not found")
        return event_set

    def xǁEventSetRegistryǁget_event_set__mutmut_1(self, name: str) -> EventSet:
        """Retrieve an event set by name.

        Args:
            name: The name of the event set

        Returns:
            The EventSet

        Raises:
            NotFoundError: If no event set with this name exists

        """
        event_set = None
        if event_set is None:
            raise NotFoundError(f"Event set '{name}' not found")
        return event_set

    def xǁEventSetRegistryǁget_event_set__mutmut_2(self, name: str) -> EventSet:
        """Retrieve an event set by name.

        Args:
            name: The name of the event set

        Returns:
            The EventSet

        Raises:
            NotFoundError: If no event set with this name exists

        """
        event_set = self.get(None, "eventset")
        if event_set is None:
            raise NotFoundError(f"Event set '{name}' not found")
        return event_set

    def xǁEventSetRegistryǁget_event_set__mutmut_3(self, name: str) -> EventSet:
        """Retrieve an event set by name.

        Args:
            name: The name of the event set

        Returns:
            The EventSet

        Raises:
            NotFoundError: If no event set with this name exists

        """
        event_set = self.get(name, None)
        if event_set is None:
            raise NotFoundError(f"Event set '{name}' not found")
        return event_set

    def xǁEventSetRegistryǁget_event_set__mutmut_4(self, name: str) -> EventSet:
        """Retrieve an event set by name.

        Args:
            name: The name of the event set

        Returns:
            The EventSet

        Raises:
            NotFoundError: If no event set with this name exists

        """
        event_set = self.get("eventset")
        if event_set is None:
            raise NotFoundError(f"Event set '{name}' not found")
        return event_set

    def xǁEventSetRegistryǁget_event_set__mutmut_5(self, name: str) -> EventSet:
        """Retrieve an event set by name.

        Args:
            name: The name of the event set

        Returns:
            The EventSet

        Raises:
            NotFoundError: If no event set with this name exists

        """
        event_set = self.get(
            name,
        )
        if event_set is None:
            raise NotFoundError(f"Event set '{name}' not found")
        return event_set

    def xǁEventSetRegistryǁget_event_set__mutmut_6(self, name: str) -> EventSet:
        """Retrieve an event set by name.

        Args:
            name: The name of the event set

        Returns:
            The EventSet

        Raises:
            NotFoundError: If no event set with this name exists

        """
        event_set = self.get(name, "XXeventsetXX")
        if event_set is None:
            raise NotFoundError(f"Event set '{name}' not found")
        return event_set

    def xǁEventSetRegistryǁget_event_set__mutmut_7(self, name: str) -> EventSet:
        """Retrieve an event set by name.

        Args:
            name: The name of the event set

        Returns:
            The EventSet

        Raises:
            NotFoundError: If no event set with this name exists

        """
        event_set = self.get(name, "EVENTSET")
        if event_set is None:
            raise NotFoundError(f"Event set '{name}' not found")
        return event_set

    def xǁEventSetRegistryǁget_event_set__mutmut_8(self, name: str) -> EventSet:
        """Retrieve an event set by name.

        Args:
            name: The name of the event set

        Returns:
            The EventSet

        Raises:
            NotFoundError: If no event set with this name exists

        """
        event_set = self.get(name, "eventset")
        if event_set is not None:
            raise NotFoundError(f"Event set '{name}' not found")
        return event_set

    def xǁEventSetRegistryǁget_event_set__mutmut_9(self, name: str) -> EventSet:
        """Retrieve an event set by name.

        Args:
            name: The name of the event set

        Returns:
            The EventSet

        Raises:
            NotFoundError: If no event set with this name exists

        """
        event_set = self.get(name, "eventset")
        if event_set is None:
            raise NotFoundError(None)
        return event_set

    xǁEventSetRegistryǁget_event_set__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEventSetRegistryǁget_event_set__mutmut_1": xǁEventSetRegistryǁget_event_set__mutmut_1,
        "xǁEventSetRegistryǁget_event_set__mutmut_2": xǁEventSetRegistryǁget_event_set__mutmut_2,
        "xǁEventSetRegistryǁget_event_set__mutmut_3": xǁEventSetRegistryǁget_event_set__mutmut_3,
        "xǁEventSetRegistryǁget_event_set__mutmut_4": xǁEventSetRegistryǁget_event_set__mutmut_4,
        "xǁEventSetRegistryǁget_event_set__mutmut_5": xǁEventSetRegistryǁget_event_set__mutmut_5,
        "xǁEventSetRegistryǁget_event_set__mutmut_6": xǁEventSetRegistryǁget_event_set__mutmut_6,
        "xǁEventSetRegistryǁget_event_set__mutmut_7": xǁEventSetRegistryǁget_event_set__mutmut_7,
        "xǁEventSetRegistryǁget_event_set__mutmut_8": xǁEventSetRegistryǁget_event_set__mutmut_8,
        "xǁEventSetRegistryǁget_event_set__mutmut_9": xǁEventSetRegistryǁget_event_set__mutmut_9,
    }

    def get_event_set(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEventSetRegistryǁget_event_set__mutmut_orig"),
            object.__getattribute__(self, "xǁEventSetRegistryǁget_event_set__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_event_set.__signature__ = _mutmut_signature(xǁEventSetRegistryǁget_event_set__mutmut_orig)
    xǁEventSetRegistryǁget_event_set__mutmut_orig.__name__ = "xǁEventSetRegistryǁget_event_set"

    def xǁEventSetRegistryǁlist_event_sets__mutmut_orig(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_1(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = None
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_2(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension(None)
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_3(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("XXeventsetXX")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_4(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("EVENTSET")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_5(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = None
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_6(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(None, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_7(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, None) for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_8(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry("eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_9(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [
            self.get_entry(
                name,
            )
            for name in names
        ]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_10(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "XXeventsetXX") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_11(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "EVENTSET") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_12(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = None
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_13(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_14(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=None, reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_15(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=None)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_16(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_17(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(
            key=lambda e: e.metadata.get("priority", 0),
        )
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_18(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: None, reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_19(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get(None, 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_20(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", None), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_21(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get(0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_22(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(
            key=lambda e: e.metadata.get(
                "priority",
            ),
            reverse=True,
        )
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_23(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("XXpriorityXX", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_24(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("PRIORITY", 0), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_25(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 1), reverse=True)
        return [entry.value for entry in valid_entries]

    def xǁEventSetRegistryǁlist_event_sets__mutmut_26(self) -> list[EventSet]:
        """List all registered event sets sorted by priority.

        Returns:
            List of EventSet objects sorted by descending priority

        """
        names = self.list_dimension("eventset")
        entries = [self.get_entry(name, "eventset") for name in names]
        valid_entries = [entry for entry in entries if entry is not None]
        valid_entries.sort(key=lambda e: e.metadata.get("priority", 0), reverse=False)
        return [entry.value for entry in valid_entries]

    xǁEventSetRegistryǁlist_event_sets__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEventSetRegistryǁlist_event_sets__mutmut_1": xǁEventSetRegistryǁlist_event_sets__mutmut_1,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_2": xǁEventSetRegistryǁlist_event_sets__mutmut_2,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_3": xǁEventSetRegistryǁlist_event_sets__mutmut_3,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_4": xǁEventSetRegistryǁlist_event_sets__mutmut_4,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_5": xǁEventSetRegistryǁlist_event_sets__mutmut_5,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_6": xǁEventSetRegistryǁlist_event_sets__mutmut_6,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_7": xǁEventSetRegistryǁlist_event_sets__mutmut_7,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_8": xǁEventSetRegistryǁlist_event_sets__mutmut_8,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_9": xǁEventSetRegistryǁlist_event_sets__mutmut_9,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_10": xǁEventSetRegistryǁlist_event_sets__mutmut_10,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_11": xǁEventSetRegistryǁlist_event_sets__mutmut_11,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_12": xǁEventSetRegistryǁlist_event_sets__mutmut_12,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_13": xǁEventSetRegistryǁlist_event_sets__mutmut_13,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_14": xǁEventSetRegistryǁlist_event_sets__mutmut_14,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_15": xǁEventSetRegistryǁlist_event_sets__mutmut_15,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_16": xǁEventSetRegistryǁlist_event_sets__mutmut_16,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_17": xǁEventSetRegistryǁlist_event_sets__mutmut_17,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_18": xǁEventSetRegistryǁlist_event_sets__mutmut_18,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_19": xǁEventSetRegistryǁlist_event_sets__mutmut_19,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_20": xǁEventSetRegistryǁlist_event_sets__mutmut_20,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_21": xǁEventSetRegistryǁlist_event_sets__mutmut_21,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_22": xǁEventSetRegistryǁlist_event_sets__mutmut_22,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_23": xǁEventSetRegistryǁlist_event_sets__mutmut_23,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_24": xǁEventSetRegistryǁlist_event_sets__mutmut_24,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_25": xǁEventSetRegistryǁlist_event_sets__mutmut_25,
        "xǁEventSetRegistryǁlist_event_sets__mutmut_26": xǁEventSetRegistryǁlist_event_sets__mutmut_26,
    }

    def list_event_sets(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEventSetRegistryǁlist_event_sets__mutmut_orig"),
            object.__getattribute__(self, "xǁEventSetRegistryǁlist_event_sets__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    list_event_sets.__signature__ = _mutmut_signature(xǁEventSetRegistryǁlist_event_sets__mutmut_orig)
    xǁEventSetRegistryǁlist_event_sets__mutmut_orig.__name__ = "xǁEventSetRegistryǁlist_event_sets"

    def xǁEventSetRegistryǁdiscover_sets__mutmut_orig(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_1(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = None
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_2(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent * "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_3(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(None).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_4(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "XXsetsXX"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_5(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "SETS"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_6(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_7(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug(None)
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_8(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("XXNo sets directory found for auto-discoveryXX")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_9(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("no sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_10(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("NO SETS DIRECTORY FOUND FOR AUTO-DISCOVERY")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_11(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules(None):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_12(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(None)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_13(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                break

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_14(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = None
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_15(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = None

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_16(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(None)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_17(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(None, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_18(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, None):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_19(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr("EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_20(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(
                    module,
                ):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_21(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "XXEVENT_SETXX"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_22(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "event_set"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_23(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = None
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_24(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(None)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_25(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                None,
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_26(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=None,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_27(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=None,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_28(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_29(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_30(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_31(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "XXAuto-discovered event setXX",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_32(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_33(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "AUTO-DISCOVERED EVENT SET",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_34(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                None,
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_35(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=None,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_36(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=None,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_37(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_38(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_39(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_40(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "XXEvent set already registered during discoveryXX",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_41(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_42(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "EVENT SET ALREADY REGISTERED DURING DISCOVERY",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_43(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            None,
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_44(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=None,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_45(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=None,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_46(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_47(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_48(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_49(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "XXEVENT_SET is not an EventSetXX",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_50(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "event_set is not an eventset",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_51(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET IS NOT AN EVENTSET",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_52(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(None).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_53(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    None,
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_54(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=None,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_55(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=None,
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_56(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_57(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_58(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_59(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "XXFailed to import event set moduleXX",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_60(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_61(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "FAILED TO IMPORT EVENT SET MODULE",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_62(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(None),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_63(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    None,
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_64(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=None,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_65(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=None,
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_66(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=None,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_67(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_68(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_69(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_70(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_71(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "XXError during event set discoveryXX",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_72(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_73(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "ERROR DURING EVENT SET DISCOVERY",
                    module=module_name,
                    error=str(e),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_74(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(None),
                    error_type=type(e).__name__,
                )

    def xǁEventSetRegistryǁdiscover_sets__mutmut_75(self) -> None:
        """Auto-discover and register event sets from the sets/ directory.

        Imports all modules in the sets/ subdirectory and registers
        any EVENT_SET constants found.
        """
        sets_path = Path(__file__).parent / "sets"
        if not sets_path.exists():
            logger.debug("No sets directory found for auto-discovery")
            return

        for module_info in pkgutil.iter_modules([str(sets_path)]):
            if module_info.ispkg:
                continue

            module_name = f"provide.foundation.eventsets.sets.{module_info.name}"
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "EVENT_SET"):
                    event_set = module.EVENT_SET
                    if isinstance(event_set, EventSet):
                        try:
                            self.register_event_set(event_set)
                            logger.debug(
                                "Auto-discovered event set",
                                module=module_name,
                                name=event_set.name,
                            )
                        except AlreadyExistsError:
                            logger.trace(
                                "Event set already registered during discovery",
                                module=module_name,
                                name=event_set.name,
                            )
                    else:
                        logger.warning(
                            "EVENT_SET is not an EventSet",
                            module=module_name,
                            type=type(event_set).__name__,
                        )

            except ImportError as e:
                logger.debug(
                    "Failed to import event set module",
                    module=module_name,
                    error=str(e),
                )
            except Exception as e:
                logger.warning(
                    "Error during event set discovery",
                    module=module_name,
                    error=str(e),
                    error_type=type(None).__name__,
                )

    xǁEventSetRegistryǁdiscover_sets__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEventSetRegistryǁdiscover_sets__mutmut_1": xǁEventSetRegistryǁdiscover_sets__mutmut_1,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_2": xǁEventSetRegistryǁdiscover_sets__mutmut_2,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_3": xǁEventSetRegistryǁdiscover_sets__mutmut_3,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_4": xǁEventSetRegistryǁdiscover_sets__mutmut_4,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_5": xǁEventSetRegistryǁdiscover_sets__mutmut_5,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_6": xǁEventSetRegistryǁdiscover_sets__mutmut_6,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_7": xǁEventSetRegistryǁdiscover_sets__mutmut_7,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_8": xǁEventSetRegistryǁdiscover_sets__mutmut_8,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_9": xǁEventSetRegistryǁdiscover_sets__mutmut_9,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_10": xǁEventSetRegistryǁdiscover_sets__mutmut_10,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_11": xǁEventSetRegistryǁdiscover_sets__mutmut_11,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_12": xǁEventSetRegistryǁdiscover_sets__mutmut_12,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_13": xǁEventSetRegistryǁdiscover_sets__mutmut_13,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_14": xǁEventSetRegistryǁdiscover_sets__mutmut_14,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_15": xǁEventSetRegistryǁdiscover_sets__mutmut_15,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_16": xǁEventSetRegistryǁdiscover_sets__mutmut_16,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_17": xǁEventSetRegistryǁdiscover_sets__mutmut_17,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_18": xǁEventSetRegistryǁdiscover_sets__mutmut_18,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_19": xǁEventSetRegistryǁdiscover_sets__mutmut_19,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_20": xǁEventSetRegistryǁdiscover_sets__mutmut_20,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_21": xǁEventSetRegistryǁdiscover_sets__mutmut_21,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_22": xǁEventSetRegistryǁdiscover_sets__mutmut_22,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_23": xǁEventSetRegistryǁdiscover_sets__mutmut_23,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_24": xǁEventSetRegistryǁdiscover_sets__mutmut_24,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_25": xǁEventSetRegistryǁdiscover_sets__mutmut_25,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_26": xǁEventSetRegistryǁdiscover_sets__mutmut_26,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_27": xǁEventSetRegistryǁdiscover_sets__mutmut_27,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_28": xǁEventSetRegistryǁdiscover_sets__mutmut_28,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_29": xǁEventSetRegistryǁdiscover_sets__mutmut_29,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_30": xǁEventSetRegistryǁdiscover_sets__mutmut_30,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_31": xǁEventSetRegistryǁdiscover_sets__mutmut_31,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_32": xǁEventSetRegistryǁdiscover_sets__mutmut_32,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_33": xǁEventSetRegistryǁdiscover_sets__mutmut_33,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_34": xǁEventSetRegistryǁdiscover_sets__mutmut_34,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_35": xǁEventSetRegistryǁdiscover_sets__mutmut_35,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_36": xǁEventSetRegistryǁdiscover_sets__mutmut_36,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_37": xǁEventSetRegistryǁdiscover_sets__mutmut_37,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_38": xǁEventSetRegistryǁdiscover_sets__mutmut_38,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_39": xǁEventSetRegistryǁdiscover_sets__mutmut_39,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_40": xǁEventSetRegistryǁdiscover_sets__mutmut_40,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_41": xǁEventSetRegistryǁdiscover_sets__mutmut_41,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_42": xǁEventSetRegistryǁdiscover_sets__mutmut_42,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_43": xǁEventSetRegistryǁdiscover_sets__mutmut_43,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_44": xǁEventSetRegistryǁdiscover_sets__mutmut_44,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_45": xǁEventSetRegistryǁdiscover_sets__mutmut_45,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_46": xǁEventSetRegistryǁdiscover_sets__mutmut_46,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_47": xǁEventSetRegistryǁdiscover_sets__mutmut_47,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_48": xǁEventSetRegistryǁdiscover_sets__mutmut_48,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_49": xǁEventSetRegistryǁdiscover_sets__mutmut_49,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_50": xǁEventSetRegistryǁdiscover_sets__mutmut_50,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_51": xǁEventSetRegistryǁdiscover_sets__mutmut_51,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_52": xǁEventSetRegistryǁdiscover_sets__mutmut_52,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_53": xǁEventSetRegistryǁdiscover_sets__mutmut_53,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_54": xǁEventSetRegistryǁdiscover_sets__mutmut_54,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_55": xǁEventSetRegistryǁdiscover_sets__mutmut_55,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_56": xǁEventSetRegistryǁdiscover_sets__mutmut_56,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_57": xǁEventSetRegistryǁdiscover_sets__mutmut_57,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_58": xǁEventSetRegistryǁdiscover_sets__mutmut_58,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_59": xǁEventSetRegistryǁdiscover_sets__mutmut_59,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_60": xǁEventSetRegistryǁdiscover_sets__mutmut_60,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_61": xǁEventSetRegistryǁdiscover_sets__mutmut_61,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_62": xǁEventSetRegistryǁdiscover_sets__mutmut_62,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_63": xǁEventSetRegistryǁdiscover_sets__mutmut_63,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_64": xǁEventSetRegistryǁdiscover_sets__mutmut_64,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_65": xǁEventSetRegistryǁdiscover_sets__mutmut_65,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_66": xǁEventSetRegistryǁdiscover_sets__mutmut_66,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_67": xǁEventSetRegistryǁdiscover_sets__mutmut_67,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_68": xǁEventSetRegistryǁdiscover_sets__mutmut_68,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_69": xǁEventSetRegistryǁdiscover_sets__mutmut_69,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_70": xǁEventSetRegistryǁdiscover_sets__mutmut_70,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_71": xǁEventSetRegistryǁdiscover_sets__mutmut_71,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_72": xǁEventSetRegistryǁdiscover_sets__mutmut_72,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_73": xǁEventSetRegistryǁdiscover_sets__mutmut_73,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_74": xǁEventSetRegistryǁdiscover_sets__mutmut_74,
        "xǁEventSetRegistryǁdiscover_sets__mutmut_75": xǁEventSetRegistryǁdiscover_sets__mutmut_75,
    }

    def discover_sets(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEventSetRegistryǁdiscover_sets__mutmut_orig"),
            object.__getattribute__(self, "xǁEventSetRegistryǁdiscover_sets__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    discover_sets.__signature__ = _mutmut_signature(xǁEventSetRegistryǁdiscover_sets__mutmut_orig)
    xǁEventSetRegistryǁdiscover_sets__mutmut_orig.__name__ = "xǁEventSetRegistryǁdiscover_sets"


# Global registry instance
_registry = EventSetRegistry()
_discovery_completed = False


def get_registry() -> EventSetRegistry:
    """Get the global event set registry instance."""
    return _registry


def x_register_event_set__mutmut_orig(event_set: EventSet) -> None:
    """Register an event set in the global registry.

    Args:
        event_set: The EventSet to register

    """
    _registry.register_event_set(event_set)


def x_register_event_set__mutmut_1(event_set: EventSet) -> None:
    """Register an event set in the global registry.

    Args:
        event_set: The EventSet to register

    """
    _registry.register_event_set(None)


x_register_event_set__mutmut_mutants: ClassVar[MutantDict] = {
    "x_register_event_set__mutmut_1": x_register_event_set__mutmut_1
}


def register_event_set(*args, **kwargs):
    result = _mutmut_trampoline(
        x_register_event_set__mutmut_orig, x_register_event_set__mutmut_mutants, args, kwargs
    )
    return result


register_event_set.__signature__ = _mutmut_signature(x_register_event_set__mutmut_orig)
x_register_event_set__mutmut_orig.__name__ = "x_register_event_set"


def x_discover_event_sets__mutmut_orig() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("Event set discovery already completed, skipping")
        return

    logger.debug("Starting event set discovery")
    _registry.discover_sets()
    _discovery_completed = True
    logger.debug("Event set discovery completed")


def x_discover_event_sets__mutmut_1() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace(None)
        return

    logger.debug("Starting event set discovery")
    _registry.discover_sets()
    _discovery_completed = True
    logger.debug("Event set discovery completed")


def x_discover_event_sets__mutmut_2() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("XXEvent set discovery already completed, skippingXX")
        return

    logger.debug("Starting event set discovery")
    _registry.discover_sets()
    _discovery_completed = True
    logger.debug("Event set discovery completed")


def x_discover_event_sets__mutmut_3() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("event set discovery already completed, skipping")
        return

    logger.debug("Starting event set discovery")
    _registry.discover_sets()
    _discovery_completed = True
    logger.debug("Event set discovery completed")


def x_discover_event_sets__mutmut_4() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("EVENT SET DISCOVERY ALREADY COMPLETED, SKIPPING")
        return

    logger.debug("Starting event set discovery")
    _registry.discover_sets()
    _discovery_completed = True
    logger.debug("Event set discovery completed")


def x_discover_event_sets__mutmut_5() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("Event set discovery already completed, skipping")
        return

    logger.debug(None)
    _registry.discover_sets()
    _discovery_completed = True
    logger.debug("Event set discovery completed")


def x_discover_event_sets__mutmut_6() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("Event set discovery already completed, skipping")
        return

    logger.debug("XXStarting event set discoveryXX")
    _registry.discover_sets()
    _discovery_completed = True
    logger.debug("Event set discovery completed")


def x_discover_event_sets__mutmut_7() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("Event set discovery already completed, skipping")
        return

    logger.debug("starting event set discovery")
    _registry.discover_sets()
    _discovery_completed = True
    logger.debug("Event set discovery completed")


def x_discover_event_sets__mutmut_8() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("Event set discovery already completed, skipping")
        return

    logger.debug("STARTING EVENT SET DISCOVERY")
    _registry.discover_sets()
    _discovery_completed = True
    logger.debug("Event set discovery completed")


def x_discover_event_sets__mutmut_9() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("Event set discovery already completed, skipping")
        return

    logger.debug("Starting event set discovery")
    _registry.discover_sets()
    _discovery_completed = None
    logger.debug("Event set discovery completed")


def x_discover_event_sets__mutmut_10() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("Event set discovery already completed, skipping")
        return

    logger.debug("Starting event set discovery")
    _registry.discover_sets()
    _discovery_completed = False
    logger.debug("Event set discovery completed")


def x_discover_event_sets__mutmut_11() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("Event set discovery already completed, skipping")
        return

    logger.debug("Starting event set discovery")
    _registry.discover_sets()
    _discovery_completed = True
    logger.debug(None)


def x_discover_event_sets__mutmut_12() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("Event set discovery already completed, skipping")
        return

    logger.debug("Starting event set discovery")
    _registry.discover_sets()
    _discovery_completed = True
    logger.debug("XXEvent set discovery completedXX")


def x_discover_event_sets__mutmut_13() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("Event set discovery already completed, skipping")
        return

    logger.debug("Starting event set discovery")
    _registry.discover_sets()
    _discovery_completed = True
    logger.debug("event set discovery completed")


def x_discover_event_sets__mutmut_14() -> None:
    """Auto-discover and register all event sets."""
    global _discovery_completed
    if _discovery_completed:
        logger.trace("Event set discovery already completed, skipping")
        return

    logger.debug("Starting event set discovery")
    _registry.discover_sets()
    _discovery_completed = True
    logger.debug("EVENT SET DISCOVERY COMPLETED")


x_discover_event_sets__mutmut_mutants: ClassVar[MutantDict] = {
    "x_discover_event_sets__mutmut_1": x_discover_event_sets__mutmut_1,
    "x_discover_event_sets__mutmut_2": x_discover_event_sets__mutmut_2,
    "x_discover_event_sets__mutmut_3": x_discover_event_sets__mutmut_3,
    "x_discover_event_sets__mutmut_4": x_discover_event_sets__mutmut_4,
    "x_discover_event_sets__mutmut_5": x_discover_event_sets__mutmut_5,
    "x_discover_event_sets__mutmut_6": x_discover_event_sets__mutmut_6,
    "x_discover_event_sets__mutmut_7": x_discover_event_sets__mutmut_7,
    "x_discover_event_sets__mutmut_8": x_discover_event_sets__mutmut_8,
    "x_discover_event_sets__mutmut_9": x_discover_event_sets__mutmut_9,
    "x_discover_event_sets__mutmut_10": x_discover_event_sets__mutmut_10,
    "x_discover_event_sets__mutmut_11": x_discover_event_sets__mutmut_11,
    "x_discover_event_sets__mutmut_12": x_discover_event_sets__mutmut_12,
    "x_discover_event_sets__mutmut_13": x_discover_event_sets__mutmut_13,
    "x_discover_event_sets__mutmut_14": x_discover_event_sets__mutmut_14,
}


def discover_event_sets(*args, **kwargs):
    result = _mutmut_trampoline(
        x_discover_event_sets__mutmut_orig, x_discover_event_sets__mutmut_mutants, args, kwargs
    )
    return result


discover_event_sets.__signature__ = _mutmut_signature(x_discover_event_sets__mutmut_orig)
x_discover_event_sets__mutmut_orig.__name__ = "x_discover_event_sets"


def x_reset_discovery_state__mutmut_orig() -> None:
    """Reset discovery state for testing."""
    global _discovery_completed
    _discovery_completed = False
    logger.trace("Event set discovery state reset")


def x_reset_discovery_state__mutmut_1() -> None:
    """Reset discovery state for testing."""
    global _discovery_completed
    _discovery_completed = None
    logger.trace("Event set discovery state reset")


def x_reset_discovery_state__mutmut_2() -> None:
    """Reset discovery state for testing."""
    global _discovery_completed
    _discovery_completed = True
    logger.trace("Event set discovery state reset")


def x_reset_discovery_state__mutmut_3() -> None:
    """Reset discovery state for testing."""
    global _discovery_completed
    _discovery_completed = False
    logger.trace(None)


def x_reset_discovery_state__mutmut_4() -> None:
    """Reset discovery state for testing."""
    global _discovery_completed
    _discovery_completed = False
    logger.trace("XXEvent set discovery state resetXX")


def x_reset_discovery_state__mutmut_5() -> None:
    """Reset discovery state for testing."""
    global _discovery_completed
    _discovery_completed = False
    logger.trace("event set discovery state reset")


def x_reset_discovery_state__mutmut_6() -> None:
    """Reset discovery state for testing."""
    global _discovery_completed
    _discovery_completed = False
    logger.trace("EVENT SET DISCOVERY STATE RESET")


x_reset_discovery_state__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_discovery_state__mutmut_1": x_reset_discovery_state__mutmut_1,
    "x_reset_discovery_state__mutmut_2": x_reset_discovery_state__mutmut_2,
    "x_reset_discovery_state__mutmut_3": x_reset_discovery_state__mutmut_3,
    "x_reset_discovery_state__mutmut_4": x_reset_discovery_state__mutmut_4,
    "x_reset_discovery_state__mutmut_5": x_reset_discovery_state__mutmut_5,
    "x_reset_discovery_state__mutmut_6": x_reset_discovery_state__mutmut_6,
}


def reset_discovery_state(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_discovery_state__mutmut_orig, x_reset_discovery_state__mutmut_mutants, args, kwargs
    )
    return result


reset_discovery_state.__signature__ = _mutmut_signature(x_reset_discovery_state__mutmut_orig)
x_reset_discovery_state__mutmut_orig.__name__ = "x_reset_discovery_state"


def x_clear_registry__mutmut_orig() -> None:
    """Clear the registry for testing."""
    global _registry, _discovery_completed
    _registry = EventSetRegistry()
    _discovery_completed = False
    logger.trace("Event set registry cleared")


def x_clear_registry__mutmut_1() -> None:
    """Clear the registry for testing."""
    global _registry, _discovery_completed
    _registry = None
    _discovery_completed = False
    logger.trace("Event set registry cleared")


def x_clear_registry__mutmut_2() -> None:
    """Clear the registry for testing."""
    global _registry, _discovery_completed
    _registry = EventSetRegistry()
    _discovery_completed = None
    logger.trace("Event set registry cleared")


def x_clear_registry__mutmut_3() -> None:
    """Clear the registry for testing."""
    global _registry, _discovery_completed
    _registry = EventSetRegistry()
    _discovery_completed = True
    logger.trace("Event set registry cleared")


def x_clear_registry__mutmut_4() -> None:
    """Clear the registry for testing."""
    global _registry, _discovery_completed
    _registry = EventSetRegistry()
    _discovery_completed = False
    logger.trace(None)


def x_clear_registry__mutmut_5() -> None:
    """Clear the registry for testing."""
    global _registry, _discovery_completed
    _registry = EventSetRegistry()
    _discovery_completed = False
    logger.trace("XXEvent set registry clearedXX")


def x_clear_registry__mutmut_6() -> None:
    """Clear the registry for testing."""
    global _registry, _discovery_completed
    _registry = EventSetRegistry()
    _discovery_completed = False
    logger.trace("event set registry cleared")


def x_clear_registry__mutmut_7() -> None:
    """Clear the registry for testing."""
    global _registry, _discovery_completed
    _registry = EventSetRegistry()
    _discovery_completed = False
    logger.trace("EVENT SET REGISTRY CLEARED")


x_clear_registry__mutmut_mutants: ClassVar[MutantDict] = {
    "x_clear_registry__mutmut_1": x_clear_registry__mutmut_1,
    "x_clear_registry__mutmut_2": x_clear_registry__mutmut_2,
    "x_clear_registry__mutmut_3": x_clear_registry__mutmut_3,
    "x_clear_registry__mutmut_4": x_clear_registry__mutmut_4,
    "x_clear_registry__mutmut_5": x_clear_registry__mutmut_5,
    "x_clear_registry__mutmut_6": x_clear_registry__mutmut_6,
    "x_clear_registry__mutmut_7": x_clear_registry__mutmut_7,
}


def clear_registry(*args, **kwargs):
    result = _mutmut_trampoline(x_clear_registry__mutmut_orig, x_clear_registry__mutmut_mutants, args, kwargs)
    return result


clear_registry.__signature__ = _mutmut_signature(x_clear_registry__mutmut_orig)
x_clear_registry__mutmut_orig.__name__ = "x_clear_registry"


# <3 🧱🤝📊🪄
