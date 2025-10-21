# provide/foundation/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation import config, errors, hub, platform, process, resilience, tracer
from provide.foundation.console import perr, pin, pout
from provide.foundation.context import CLIContext
from provide.foundation.errors import (
    FoundationError,
    error_boundary,
    resilient,
)
from provide.foundation.eventsets.display import show_event_matrix
from provide.foundation.eventsets.types import (
    EventMapping,
    EventSet,
    FieldMapping,
)
from provide.foundation.hub.components import ComponentCategory, get_component_registry
from provide.foundation.hub.manager import (
    Hub,
    clear_hub,
    get_hub,
)
from provide.foundation.hub.registry import Registry, RegistryEntry
from provide.foundation.logger import (
    LoggingConfig,
    TelemetryConfig,
    get_logger,
    logger,
)
from provide.foundation.logger.types import (
    ConsoleFormatterStr,
    LogLevelStr,
)
from provide.foundation.resilience import (
    AsyncCircuitBreaker,
    BackoffStrategy,
    CircuitState,
    FallbackChain,
    RetryExecutor,
    RetryPolicy,
    SyncCircuitBreaker,
    circuit_breaker,
    fallback,
    retry,
)
from provide.foundation.setup import shutdown_foundation
from provide.foundation.utils import (
    TokenBucketRateLimiter,
    check_optional_deps,
    timed_block,
)

"""A foundational framework for building operationally excellent Python applications.

This is the primary public interface for the framework, re-exporting common
components for application development.
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


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_orig(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_1(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name != "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_2(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "XX__version__XX":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_3(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__VERSION__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_4(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version(None, caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_5(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=None)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_6(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version(caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_7(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", )

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_8(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("XXprovide-foundationXX", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_9(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("PROVIDE-FOUNDATION", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_10(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(None, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_11(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, None)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_12(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_13(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, )
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_14(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = None
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_15(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name not in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_16(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(None):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_17(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(None) from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


# Lazy loading support for optional modules and __version__
def x___getattr____mutmut_18(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(None) from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)

x___getattr____mutmut_mutants : ClassVar[MutantDict] = {
'x___getattr____mutmut_1': x___getattr____mutmut_1, 
    'x___getattr____mutmut_2': x___getattr____mutmut_2, 
    'x___getattr____mutmut_3': x___getattr____mutmut_3, 
    'x___getattr____mutmut_4': x___getattr____mutmut_4, 
    'x___getattr____mutmut_5': x___getattr____mutmut_5, 
    'x___getattr____mutmut_6': x___getattr____mutmut_6, 
    'x___getattr____mutmut_7': x___getattr____mutmut_7, 
    'x___getattr____mutmut_8': x___getattr____mutmut_8, 
    'x___getattr____mutmut_9': x___getattr____mutmut_9, 
    'x___getattr____mutmut_10': x___getattr____mutmut_10, 
    'x___getattr____mutmut_11': x___getattr____mutmut_11, 
    'x___getattr____mutmut_12': x___getattr____mutmut_12, 
    'x___getattr____mutmut_13': x___getattr____mutmut_13, 
    'x___getattr____mutmut_14': x___getattr____mutmut_14, 
    'x___getattr____mutmut_15': x___getattr____mutmut_15, 
    'x___getattr____mutmut_16': x___getattr____mutmut_16, 
    'x___getattr____mutmut_17': x___getattr____mutmut_17, 
    'x___getattr____mutmut_18': x___getattr____mutmut_18
}

def __getattr__(*args, **kwargs):
    result = _mutmut_trampoline(x___getattr____mutmut_orig, x___getattr____mutmut_mutants, args, kwargs)
    return result 

__getattr__.__signature__ = _mutmut_signature(x___getattr____mutmut_orig)
x___getattr____mutmut_orig.__name__ = 'x___getattr__'


__all__ = [
    # Resilience - Circuit Breaker (async)
    "AsyncCircuitBreaker",
    "BackoffStrategy",
    # New foundation modules
    "CLIContext",
    "CircuitState",
    "ComponentCategory",
    "ConsoleFormatterStr",
    # Event set types
    "EventMapping",
    "EventSet",
    "FallbackChain",
    "FieldMapping",
    # Error handling essentials
    "FoundationError",
    "Hub",
    # Type aliases
    "LogLevelStr",
    "LoggingConfig",
    # Hub and Registry (public API)
    "Registry",
    "RegistryEntry",
    "RetryExecutor",
    "RetryPolicy",
    # Resilience - Circuit Breaker (sync)
    "SyncCircuitBreaker",
    # Configuration classes
    "TelemetryConfig",
    # Rate limiting utilities
    "TokenBucketRateLimiter",
    # Version
    "__version__",
    # Dependency checking utility
    "check_optional_deps",
    "circuit_breaker",
    "clear_hub",
    # Config module
    "config",
    # Crypto module (lazy loaded)
    "crypto",
    # Docs module (lazy loaded)
    "docs",
    "error_boundary",
    "errors",  # The errors module for detailed imports
    "fallback",
    # Formatting module (lazy loaded)
    "formatting",
    "get_component_registry",
    "get_hub",
    "get_logger",
    "hub",
    # Core setup and logger
    "logger",
    # Console functions (work with or without click)
    "perr",
    "pin",
    "platform",
    "pout",
    "process",
    "resilience",  # The resilience module for detailed imports
    "resilient",
    # Resilience patterns
    "retry",
    # Event enrichment utilities
    "show_event_matrix",
    # Utilities
    "shutdown_foundation",
    "timed_block",
    "tracer",  # The tracer module for distributed tracing
]

# Logger instance is imported above with other logger imports

# 🐍📝


# <3 🧱🤝🤔🪄
