# provide/foundation/hub/components.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Protocol

from attrs import define, field

from provide.foundation.config.defaults import DEFAULT_COMPONENT_DIMENSION
from provide.foundation.errors.decorators import resilient

# Import ComponentCategory from its own module (no circular deps)
from provide.foundation.hub.categories import ComponentCategory

# Import functions from specialized modules for re-export
from provide.foundation.hub.config import (
    get_config_chain,
    load_all_configs,
    load_config_from_registry,
    resolve_config_value,
)
from provide.foundation.hub.discovery import (
    discover_components,
    resolve_component_dependencies,
)
from provide.foundation.hub.handlers import (
    execute_error_handlers,
    get_handlers_for_exception,
)
from provide.foundation.hub.lifecycle import (
    cleanup_all_components,
    get_or_initialize_component,
    initialize_all_async_components,
    initialize_async_component,
)
from provide.foundation.hub.processors import (
    get_processor_pipeline,
    get_processors_for_stage,
)
from provide.foundation.hub.registry import Registry

"""Registry-based component management system for Foundation.

This module implements Foundation's end-state architecture where all internal
components are managed through the Hub registry system. Provides centralized
component discovery, lifecycle management, and dependency resolution.
"""
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


@define(frozen=True, slots=True)
class ComponentInfo:
    """Information about a registered component."""

    name: str = field()
    component_class: type[Any] = field()
    dimension: str = field(default=DEFAULT_COMPONENT_DIMENSION)
    version: str | None = field(default=None)
    description: str | None = field(default=None)
    author: str | None = field(default=None)
    tags: list[str] = field(factory=list)
    metadata: dict[str, Any] = field(factory=dict)


class ComponentLifecycle(Protocol):
    """Protocol for components that support lifecycle management."""

    async def initialize(self) -> None:
        """Initialize the component."""
        ...

    async def cleanup(self) -> None:
        """Clean up the component."""
        ...


# Global component registry
_component_registry = Registry()
_initialized_components: dict[tuple[str, str], Any] = {}


def get_component_registry() -> Registry:
    """Get the global component registry."""
    return _component_registry


@resilient(
    fallback={"status": "error"},
    context_provider=lambda: {
        "function": "check_component_health",
        "module": "hub.components",
    },
)
def check_component_health(name: str, dimension: str) -> dict[str, Any]:
    """Check component health status."""
    component = _component_registry.get(name, dimension)

    if not component:
        return {"status": "not_found"}

    entry = _component_registry.get_entry(name, dimension)
    if not entry or not entry.metadata.get("supports_health_check", False):
        return {"status": "no_health_check"}

    if hasattr(component, "health_check"):
        try:
            return component.health_check()
        except Exception as e:
            return {"status": "error", "error": str(e)}

    return {"status": "unknown"}


def x_get_component_config_schema__mutmut_orig(name: str, dimension: str) -> dict[str, Any] | None:
    """Get component configuration schema."""
    entry = _component_registry.get_entry(name, dimension)

    if not entry:
        return None

    return entry.metadata.get("config_schema")


def x_get_component_config_schema__mutmut_1(name: str, dimension: str) -> dict[str, Any] | None:
    """Get component configuration schema."""
    entry = None

    if not entry:
        return None

    return entry.metadata.get("config_schema")


def x_get_component_config_schema__mutmut_2(name: str, dimension: str) -> dict[str, Any] | None:
    """Get component configuration schema."""
    entry = _component_registry.get_entry(None, dimension)

    if not entry:
        return None

    return entry.metadata.get("config_schema")


def x_get_component_config_schema__mutmut_3(name: str, dimension: str) -> dict[str, Any] | None:
    """Get component configuration schema."""
    entry = _component_registry.get_entry(name, None)

    if not entry:
        return None

    return entry.metadata.get("config_schema")


def x_get_component_config_schema__mutmut_4(name: str, dimension: str) -> dict[str, Any] | None:
    """Get component configuration schema."""
    entry = _component_registry.get_entry(dimension)

    if not entry:
        return None

    return entry.metadata.get("config_schema")


def x_get_component_config_schema__mutmut_5(name: str, dimension: str) -> dict[str, Any] | None:
    """Get component configuration schema."""
    entry = _component_registry.get_entry(
        name,
    )

    if not entry:
        return None

    return entry.metadata.get("config_schema")


def x_get_component_config_schema__mutmut_6(name: str, dimension: str) -> dict[str, Any] | None:
    """Get component configuration schema."""
    entry = _component_registry.get_entry(name, dimension)

    if entry:
        return None

    return entry.metadata.get("config_schema")


def x_get_component_config_schema__mutmut_7(name: str, dimension: str) -> dict[str, Any] | None:
    """Get component configuration schema."""
    entry = _component_registry.get_entry(name, dimension)

    if not entry:
        return None

    return entry.metadata.get(None)


def x_get_component_config_schema__mutmut_8(name: str, dimension: str) -> dict[str, Any] | None:
    """Get component configuration schema."""
    entry = _component_registry.get_entry(name, dimension)

    if not entry:
        return None

    return entry.metadata.get("XXconfig_schemaXX")


def x_get_component_config_schema__mutmut_9(name: str, dimension: str) -> dict[str, Any] | None:
    """Get component configuration schema."""
    entry = _component_registry.get_entry(name, dimension)

    if not entry:
        return None

    return entry.metadata.get("CONFIG_SCHEMA")


x_get_component_config_schema__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_component_config_schema__mutmut_1": x_get_component_config_schema__mutmut_1,
    "x_get_component_config_schema__mutmut_2": x_get_component_config_schema__mutmut_2,
    "x_get_component_config_schema__mutmut_3": x_get_component_config_schema__mutmut_3,
    "x_get_component_config_schema__mutmut_4": x_get_component_config_schema__mutmut_4,
    "x_get_component_config_schema__mutmut_5": x_get_component_config_schema__mutmut_5,
    "x_get_component_config_schema__mutmut_6": x_get_component_config_schema__mutmut_6,
    "x_get_component_config_schema__mutmut_7": x_get_component_config_schema__mutmut_7,
    "x_get_component_config_schema__mutmut_8": x_get_component_config_schema__mutmut_8,
    "x_get_component_config_schema__mutmut_9": x_get_component_config_schema__mutmut_9,
}


def get_component_config_schema(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_component_config_schema__mutmut_orig, x_get_component_config_schema__mutmut_mutants, args, kwargs
    )
    return result


get_component_config_schema.__signature__ = _mutmut_signature(x_get_component_config_schema__mutmut_orig)
x_get_component_config_schema__mutmut_orig.__name__ = "x_get_component_config_schema"


def x_bootstrap_foundation__mutmut_orig() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_1() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = None

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_2() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry(None, ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_3() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", None):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_4() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry(ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_5() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry(
        "timestamp",
    ):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_6() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("XXtimestampXX", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_7() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("TIMESTAMP", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_8() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = None
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_9() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["XXtimestampXX"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_10() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["TIMESTAMP"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_11() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name=None,
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_12() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=None,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_13() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=None,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_14() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata=None,
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_15() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=None,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_16() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_17() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_18() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_19() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_20() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_21() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="XXtimestampXX",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_22() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="TIMESTAMP",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_23() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"XXpriorityXX": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_24() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"PRIORITY": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_25() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 101, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_26() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "XXstageXX": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_27() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "STAGE": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_28() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "XXpre_formatXX"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_29() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "PRE_FORMAT"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_30() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=False,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("Foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_31() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug(None)


def x_bootstrap_foundation__mutmut_32() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("XXFoundation bootstrap completed with registry componentsXX")


def x_bootstrap_foundation__mutmut_33() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("foundation bootstrap completed with registry components")


def x_bootstrap_foundation__mutmut_34() -> None:
    """Bootstrap Foundation with core registry components."""
    registry = get_component_registry()

    # Check if already bootstrapped
    if registry.get_entry("timestamp", ComponentCategory.PROCESSOR.value):
        return  # Already bootstrapped

    # Register core processors
    def timestamp_processor(logger: object, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        import time

        event_dict["timestamp"] = time.time()
        return event_dict

    registry.register(
        name="timestamp",
        value=timestamp_processor,
        dimension=ComponentCategory.PROCESSOR.value,
        metadata={"priority": 100, "stage": "pre_format"},
        replace=True,  # Allow replacement for test scenarios
    )

    # Register configuration schemas
    from provide.foundation.config.bootstrap import discover_and_register_configs

    discover_and_register_configs()

    from provide.foundation.hub.foundation import get_foundation_logger

    get_foundation_logger().debug("FOUNDATION BOOTSTRAP COMPLETED WITH REGISTRY COMPONENTS")


x_bootstrap_foundation__mutmut_mutants: ClassVar[MutantDict] = {
    "x_bootstrap_foundation__mutmut_1": x_bootstrap_foundation__mutmut_1,
    "x_bootstrap_foundation__mutmut_2": x_bootstrap_foundation__mutmut_2,
    "x_bootstrap_foundation__mutmut_3": x_bootstrap_foundation__mutmut_3,
    "x_bootstrap_foundation__mutmut_4": x_bootstrap_foundation__mutmut_4,
    "x_bootstrap_foundation__mutmut_5": x_bootstrap_foundation__mutmut_5,
    "x_bootstrap_foundation__mutmut_6": x_bootstrap_foundation__mutmut_6,
    "x_bootstrap_foundation__mutmut_7": x_bootstrap_foundation__mutmut_7,
    "x_bootstrap_foundation__mutmut_8": x_bootstrap_foundation__mutmut_8,
    "x_bootstrap_foundation__mutmut_9": x_bootstrap_foundation__mutmut_9,
    "x_bootstrap_foundation__mutmut_10": x_bootstrap_foundation__mutmut_10,
    "x_bootstrap_foundation__mutmut_11": x_bootstrap_foundation__mutmut_11,
    "x_bootstrap_foundation__mutmut_12": x_bootstrap_foundation__mutmut_12,
    "x_bootstrap_foundation__mutmut_13": x_bootstrap_foundation__mutmut_13,
    "x_bootstrap_foundation__mutmut_14": x_bootstrap_foundation__mutmut_14,
    "x_bootstrap_foundation__mutmut_15": x_bootstrap_foundation__mutmut_15,
    "x_bootstrap_foundation__mutmut_16": x_bootstrap_foundation__mutmut_16,
    "x_bootstrap_foundation__mutmut_17": x_bootstrap_foundation__mutmut_17,
    "x_bootstrap_foundation__mutmut_18": x_bootstrap_foundation__mutmut_18,
    "x_bootstrap_foundation__mutmut_19": x_bootstrap_foundation__mutmut_19,
    "x_bootstrap_foundation__mutmut_20": x_bootstrap_foundation__mutmut_20,
    "x_bootstrap_foundation__mutmut_21": x_bootstrap_foundation__mutmut_21,
    "x_bootstrap_foundation__mutmut_22": x_bootstrap_foundation__mutmut_22,
    "x_bootstrap_foundation__mutmut_23": x_bootstrap_foundation__mutmut_23,
    "x_bootstrap_foundation__mutmut_24": x_bootstrap_foundation__mutmut_24,
    "x_bootstrap_foundation__mutmut_25": x_bootstrap_foundation__mutmut_25,
    "x_bootstrap_foundation__mutmut_26": x_bootstrap_foundation__mutmut_26,
    "x_bootstrap_foundation__mutmut_27": x_bootstrap_foundation__mutmut_27,
    "x_bootstrap_foundation__mutmut_28": x_bootstrap_foundation__mutmut_28,
    "x_bootstrap_foundation__mutmut_29": x_bootstrap_foundation__mutmut_29,
    "x_bootstrap_foundation__mutmut_30": x_bootstrap_foundation__mutmut_30,
    "x_bootstrap_foundation__mutmut_31": x_bootstrap_foundation__mutmut_31,
    "x_bootstrap_foundation__mutmut_32": x_bootstrap_foundation__mutmut_32,
    "x_bootstrap_foundation__mutmut_33": x_bootstrap_foundation__mutmut_33,
    "x_bootstrap_foundation__mutmut_34": x_bootstrap_foundation__mutmut_34,
}


def bootstrap_foundation(*args, **kwargs):
    result = _mutmut_trampoline(
        x_bootstrap_foundation__mutmut_orig, x_bootstrap_foundation__mutmut_mutants, args, kwargs
    )
    return result


bootstrap_foundation.__signature__ = _mutmut_signature(x_bootstrap_foundation__mutmut_orig)
x_bootstrap_foundation__mutmut_orig.__name__ = "x_bootstrap_foundation"


# Bootstrap will happen lazily on first hub access to avoid circular imports
# bootstrap_foundation()


__all__ = [
    "ComponentCategory",
    # Core classes
    "ComponentInfo",
    "ComponentLifecycle",
    # Bootstrap and testing
    "bootstrap_foundation",
    # Health and schema
    "check_component_health",
    "cleanup_all_components",
    "discover_components",
    "execute_error_handlers",
    "get_component_config_schema",
    # Registry access
    "get_component_registry",
    "get_config_chain",
    "get_handlers_for_exception",
    "get_or_initialize_component",
    "get_processor_pipeline",
    "get_processors_for_stage",
    "initialize_all_async_components",
    "initialize_async_component",
    "load_all_configs",
    "load_config_from_registry",
    "resolve_component_dependencies",
    # Re-exported from specialized modules
    "resolve_config_value",
]


# <3 🧱🤝🌐🪄
