# provide/foundation/utils/stubs.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Never

from provide.foundation.errors import DependencyError

"""Utilities for creating dependency stubs with helpful error messages."""
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


def x_create_dependency_stub__mutmut_orig(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(package, feature=feature)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def x_create_dependency_stub__mutmut_1(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(None, feature=feature)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def x_create_dependency_stub__mutmut_2(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(package, feature=None)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def x_create_dependency_stub__mutmut_3(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(feature=feature)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def x_create_dependency_stub__mutmut_4(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(
                package,
            )

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def x_create_dependency_stub__mutmut_5(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(package, feature=feature)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(None, feature=feature)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def x_create_dependency_stub__mutmut_6(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(package, feature=feature)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=None)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def x_create_dependency_stub__mutmut_7(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(package, feature=feature)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(feature=feature)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def x_create_dependency_stub__mutmut_8(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(package, feature=feature)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(
                package,
            )

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def x_create_dependency_stub__mutmut_9(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(package, feature=feature)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(None, feature=feature)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def x_create_dependency_stub__mutmut_10(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(package, feature=feature)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=None)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def x_create_dependency_stub__mutmut_11(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(package, feature=feature)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(feature=feature)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def x_create_dependency_stub__mutmut_12(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(package, feature=feature)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(
                package,
            )

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def x_create_dependency_stub__mutmut_13(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(package, feature=feature)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = None
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def x_create_dependency_stub__mutmut_14(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(package, feature=feature)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = None

    return DependencyStub


x_create_dependency_stub__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_dependency_stub__mutmut_1": x_create_dependency_stub__mutmut_1,
    "x_create_dependency_stub__mutmut_2": x_create_dependency_stub__mutmut_2,
    "x_create_dependency_stub__mutmut_3": x_create_dependency_stub__mutmut_3,
    "x_create_dependency_stub__mutmut_4": x_create_dependency_stub__mutmut_4,
    "x_create_dependency_stub__mutmut_5": x_create_dependency_stub__mutmut_5,
    "x_create_dependency_stub__mutmut_6": x_create_dependency_stub__mutmut_6,
    "x_create_dependency_stub__mutmut_7": x_create_dependency_stub__mutmut_7,
    "x_create_dependency_stub__mutmut_8": x_create_dependency_stub__mutmut_8,
    "x_create_dependency_stub__mutmut_9": x_create_dependency_stub__mutmut_9,
    "x_create_dependency_stub__mutmut_10": x_create_dependency_stub__mutmut_10,
    "x_create_dependency_stub__mutmut_11": x_create_dependency_stub__mutmut_11,
    "x_create_dependency_stub__mutmut_12": x_create_dependency_stub__mutmut_12,
    "x_create_dependency_stub__mutmut_13": x_create_dependency_stub__mutmut_13,
    "x_create_dependency_stub__mutmut_14": x_create_dependency_stub__mutmut_14,
}


def create_dependency_stub(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_dependency_stub__mutmut_orig, x_create_dependency_stub__mutmut_mutants, args, kwargs
    )
    return result


create_dependency_stub.__signature__ = _mutmut_signature(x_create_dependency_stub__mutmut_orig)
x_create_dependency_stub__mutmut_orig.__name__ = "x_create_dependency_stub"


def x_create_function_stub__mutmut_orig(package: str, feature: str) -> Any:
    """Create a stub function that raises DependencyError when called.

    Args:
        package: Name of the missing package (e.g., "httpx", "mkdocs")
        feature: Foundation feature name (e.g., "transport", "docs")

    Returns:
        A stub function that raises DependencyError when called

    Example:
        >>> generate_docs = create_function_stub("mkdocs", "docs")
        >>> generate_docs()  # Raises DependencyError with install instructions
    """

    def stub_function(*args: Any, **kwargs: Any) -> Never:
        raise DependencyError(package, feature=feature)

    stub_function.__name__ = f"{feature}_stub"
    stub_function.__qualname__ = f"{feature}_stub"

    return stub_function


def x_create_function_stub__mutmut_1(package: str, feature: str) -> Any:
    """Create a stub function that raises DependencyError when called.

    Args:
        package: Name of the missing package (e.g., "httpx", "mkdocs")
        feature: Foundation feature name (e.g., "transport", "docs")

    Returns:
        A stub function that raises DependencyError when called

    Example:
        >>> generate_docs = create_function_stub("mkdocs", "docs")
        >>> generate_docs()  # Raises DependencyError with install instructions
    """

    def stub_function(*args: Any, **kwargs: Any) -> Never:
        raise DependencyError(None, feature=feature)

    stub_function.__name__ = f"{feature}_stub"
    stub_function.__qualname__ = f"{feature}_stub"

    return stub_function


def x_create_function_stub__mutmut_2(package: str, feature: str) -> Any:
    """Create a stub function that raises DependencyError when called.

    Args:
        package: Name of the missing package (e.g., "httpx", "mkdocs")
        feature: Foundation feature name (e.g., "transport", "docs")

    Returns:
        A stub function that raises DependencyError when called

    Example:
        >>> generate_docs = create_function_stub("mkdocs", "docs")
        >>> generate_docs()  # Raises DependencyError with install instructions
    """

    def stub_function(*args: Any, **kwargs: Any) -> Never:
        raise DependencyError(package, feature=None)

    stub_function.__name__ = f"{feature}_stub"
    stub_function.__qualname__ = f"{feature}_stub"

    return stub_function


def x_create_function_stub__mutmut_3(package: str, feature: str) -> Any:
    """Create a stub function that raises DependencyError when called.

    Args:
        package: Name of the missing package (e.g., "httpx", "mkdocs")
        feature: Foundation feature name (e.g., "transport", "docs")

    Returns:
        A stub function that raises DependencyError when called

    Example:
        >>> generate_docs = create_function_stub("mkdocs", "docs")
        >>> generate_docs()  # Raises DependencyError with install instructions
    """

    def stub_function(*args: Any, **kwargs: Any) -> Never:
        raise DependencyError(feature=feature)

    stub_function.__name__ = f"{feature}_stub"
    stub_function.__qualname__ = f"{feature}_stub"

    return stub_function


def x_create_function_stub__mutmut_4(package: str, feature: str) -> Any:
    """Create a stub function that raises DependencyError when called.

    Args:
        package: Name of the missing package (e.g., "httpx", "mkdocs")
        feature: Foundation feature name (e.g., "transport", "docs")

    Returns:
        A stub function that raises DependencyError when called

    Example:
        >>> generate_docs = create_function_stub("mkdocs", "docs")
        >>> generate_docs()  # Raises DependencyError with install instructions
    """

    def stub_function(*args: Any, **kwargs: Any) -> Never:
        raise DependencyError(
            package,
        )

    stub_function.__name__ = f"{feature}_stub"
    stub_function.__qualname__ = f"{feature}_stub"

    return stub_function


def x_create_function_stub__mutmut_5(package: str, feature: str) -> Any:
    """Create a stub function that raises DependencyError when called.

    Args:
        package: Name of the missing package (e.g., "httpx", "mkdocs")
        feature: Foundation feature name (e.g., "transport", "docs")

    Returns:
        A stub function that raises DependencyError when called

    Example:
        >>> generate_docs = create_function_stub("mkdocs", "docs")
        >>> generate_docs()  # Raises DependencyError with install instructions
    """

    def stub_function(*args: Any, **kwargs: Any) -> Never:
        raise DependencyError(package, feature=feature)

    stub_function.__name__ = None
    stub_function.__qualname__ = f"{feature}_stub"

    return stub_function


def x_create_function_stub__mutmut_6(package: str, feature: str) -> Any:
    """Create a stub function that raises DependencyError when called.

    Args:
        package: Name of the missing package (e.g., "httpx", "mkdocs")
        feature: Foundation feature name (e.g., "transport", "docs")

    Returns:
        A stub function that raises DependencyError when called

    Example:
        >>> generate_docs = create_function_stub("mkdocs", "docs")
        >>> generate_docs()  # Raises DependencyError with install instructions
    """

    def stub_function(*args: Any, **kwargs: Any) -> Never:
        raise DependencyError(package, feature=feature)

    stub_function.__name__ = f"{feature}_stub"
    stub_function.__qualname__ = None

    return stub_function


x_create_function_stub__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_function_stub__mutmut_1": x_create_function_stub__mutmut_1,
    "x_create_function_stub__mutmut_2": x_create_function_stub__mutmut_2,
    "x_create_function_stub__mutmut_3": x_create_function_stub__mutmut_3,
    "x_create_function_stub__mutmut_4": x_create_function_stub__mutmut_4,
    "x_create_function_stub__mutmut_5": x_create_function_stub__mutmut_5,
    "x_create_function_stub__mutmut_6": x_create_function_stub__mutmut_6,
}


def create_function_stub(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_function_stub__mutmut_orig, x_create_function_stub__mutmut_mutants, args, kwargs
    )
    return result


create_function_stub.__signature__ = _mutmut_signature(x_create_function_stub__mutmut_orig)
x_create_function_stub__mutmut_orig.__name__ = "x_create_function_stub"


def x_create_module_stub__mutmut_orig(package: str, feature: str) -> Any:
    """Create a stub module-like object that raises DependencyError on attribute access.

    Args:
        package: Name of the missing package (e.g., "httpx")
        feature: Foundation feature name (e.g., "transport")

    Returns:
        A stub object that raises DependencyError on any attribute access

    Example:
        >>> httpx = create_module_stub("httpx", "transport")
        >>> httpx.AsyncClient()  # Raises DependencyError with install instructions
    """

    class ModuleStub:
        """Stub module for missing optional dependency."""

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

    ModuleStub.__name__ = f"{package}_stub"
    ModuleStub.__qualname__ = f"{package}_stub"

    return ModuleStub()


def x_create_module_stub__mutmut_1(package: str, feature: str) -> Any:
    """Create a stub module-like object that raises DependencyError on attribute access.

    Args:
        package: Name of the missing package (e.g., "httpx")
        feature: Foundation feature name (e.g., "transport")

    Returns:
        A stub object that raises DependencyError on any attribute access

    Example:
        >>> httpx = create_module_stub("httpx", "transport")
        >>> httpx.AsyncClient()  # Raises DependencyError with install instructions
    """

    class ModuleStub:
        """Stub module for missing optional dependency."""

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(None, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

    ModuleStub.__name__ = f"{package}_stub"
    ModuleStub.__qualname__ = f"{package}_stub"

    return ModuleStub()


def x_create_module_stub__mutmut_2(package: str, feature: str) -> Any:
    """Create a stub module-like object that raises DependencyError on attribute access.

    Args:
        package: Name of the missing package (e.g., "httpx")
        feature: Foundation feature name (e.g., "transport")

    Returns:
        A stub object that raises DependencyError on any attribute access

    Example:
        >>> httpx = create_module_stub("httpx", "transport")
        >>> httpx.AsyncClient()  # Raises DependencyError with install instructions
    """

    class ModuleStub:
        """Stub module for missing optional dependency."""

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=None)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

    ModuleStub.__name__ = f"{package}_stub"
    ModuleStub.__qualname__ = f"{package}_stub"

    return ModuleStub()


def x_create_module_stub__mutmut_3(package: str, feature: str) -> Any:
    """Create a stub module-like object that raises DependencyError on attribute access.

    Args:
        package: Name of the missing package (e.g., "httpx")
        feature: Foundation feature name (e.g., "transport")

    Returns:
        A stub object that raises DependencyError on any attribute access

    Example:
        >>> httpx = create_module_stub("httpx", "transport")
        >>> httpx.AsyncClient()  # Raises DependencyError with install instructions
    """

    class ModuleStub:
        """Stub module for missing optional dependency."""

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

    ModuleStub.__name__ = f"{package}_stub"
    ModuleStub.__qualname__ = f"{package}_stub"

    return ModuleStub()


def x_create_module_stub__mutmut_4(package: str, feature: str) -> Any:
    """Create a stub module-like object that raises DependencyError on attribute access.

    Args:
        package: Name of the missing package (e.g., "httpx")
        feature: Foundation feature name (e.g., "transport")

    Returns:
        A stub object that raises DependencyError on any attribute access

    Example:
        >>> httpx = create_module_stub("httpx", "transport")
        >>> httpx.AsyncClient()  # Raises DependencyError with install instructions
    """

    class ModuleStub:
        """Stub module for missing optional dependency."""

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(
                package,
            )

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

    ModuleStub.__name__ = f"{package}_stub"
    ModuleStub.__qualname__ = f"{package}_stub"

    return ModuleStub()


def x_create_module_stub__mutmut_5(package: str, feature: str) -> Any:
    """Create a stub module-like object that raises DependencyError on attribute access.

    Args:
        package: Name of the missing package (e.g., "httpx")
        feature: Foundation feature name (e.g., "transport")

    Returns:
        A stub object that raises DependencyError on any attribute access

    Example:
        >>> httpx = create_module_stub("httpx", "transport")
        >>> httpx.AsyncClient()  # Raises DependencyError with install instructions
    """

    class ModuleStub:
        """Stub module for missing optional dependency."""

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(None, feature=feature)

    ModuleStub.__name__ = f"{package}_stub"
    ModuleStub.__qualname__ = f"{package}_stub"

    return ModuleStub()


def x_create_module_stub__mutmut_6(package: str, feature: str) -> Any:
    """Create a stub module-like object that raises DependencyError on attribute access.

    Args:
        package: Name of the missing package (e.g., "httpx")
        feature: Foundation feature name (e.g., "transport")

    Returns:
        A stub object that raises DependencyError on any attribute access

    Example:
        >>> httpx = create_module_stub("httpx", "transport")
        >>> httpx.AsyncClient()  # Raises DependencyError with install instructions
    """

    class ModuleStub:
        """Stub module for missing optional dependency."""

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=None)

    ModuleStub.__name__ = f"{package}_stub"
    ModuleStub.__qualname__ = f"{package}_stub"

    return ModuleStub()


def x_create_module_stub__mutmut_7(package: str, feature: str) -> Any:
    """Create a stub module-like object that raises DependencyError on attribute access.

    Args:
        package: Name of the missing package (e.g., "httpx")
        feature: Foundation feature name (e.g., "transport")

    Returns:
        A stub object that raises DependencyError on any attribute access

    Example:
        >>> httpx = create_module_stub("httpx", "transport")
        >>> httpx.AsyncClient()  # Raises DependencyError with install instructions
    """

    class ModuleStub:
        """Stub module for missing optional dependency."""

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(feature=feature)

    ModuleStub.__name__ = f"{package}_stub"
    ModuleStub.__qualname__ = f"{package}_stub"

    return ModuleStub()


def x_create_module_stub__mutmut_8(package: str, feature: str) -> Any:
    """Create a stub module-like object that raises DependencyError on attribute access.

    Args:
        package: Name of the missing package (e.g., "httpx")
        feature: Foundation feature name (e.g., "transport")

    Returns:
        A stub object that raises DependencyError on any attribute access

    Example:
        >>> httpx = create_module_stub("httpx", "transport")
        >>> httpx.AsyncClient()  # Raises DependencyError with install instructions
    """

    class ModuleStub:
        """Stub module for missing optional dependency."""

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(
                package,
            )

    ModuleStub.__name__ = f"{package}_stub"
    ModuleStub.__qualname__ = f"{package}_stub"

    return ModuleStub()


def x_create_module_stub__mutmut_9(package: str, feature: str) -> Any:
    """Create a stub module-like object that raises DependencyError on attribute access.

    Args:
        package: Name of the missing package (e.g., "httpx")
        feature: Foundation feature name (e.g., "transport")

    Returns:
        A stub object that raises DependencyError on any attribute access

    Example:
        >>> httpx = create_module_stub("httpx", "transport")
        >>> httpx.AsyncClient()  # Raises DependencyError with install instructions
    """

    class ModuleStub:
        """Stub module for missing optional dependency."""

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

    ModuleStub.__name__ = None
    ModuleStub.__qualname__ = f"{package}_stub"

    return ModuleStub()


def x_create_module_stub__mutmut_10(package: str, feature: str) -> Any:
    """Create a stub module-like object that raises DependencyError on attribute access.

    Args:
        package: Name of the missing package (e.g., "httpx")
        feature: Foundation feature name (e.g., "transport")

    Returns:
        A stub object that raises DependencyError on any attribute access

    Example:
        >>> httpx = create_module_stub("httpx", "transport")
        >>> httpx.AsyncClient()  # Raises DependencyError with install instructions
    """

    class ModuleStub:
        """Stub module for missing optional dependency."""

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

    ModuleStub.__name__ = f"{package}_stub"
    ModuleStub.__qualname__ = None

    return ModuleStub()


x_create_module_stub__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_module_stub__mutmut_1": x_create_module_stub__mutmut_1,
    "x_create_module_stub__mutmut_2": x_create_module_stub__mutmut_2,
    "x_create_module_stub__mutmut_3": x_create_module_stub__mutmut_3,
    "x_create_module_stub__mutmut_4": x_create_module_stub__mutmut_4,
    "x_create_module_stub__mutmut_5": x_create_module_stub__mutmut_5,
    "x_create_module_stub__mutmut_6": x_create_module_stub__mutmut_6,
    "x_create_module_stub__mutmut_7": x_create_module_stub__mutmut_7,
    "x_create_module_stub__mutmut_8": x_create_module_stub__mutmut_8,
    "x_create_module_stub__mutmut_9": x_create_module_stub__mutmut_9,
    "x_create_module_stub__mutmut_10": x_create_module_stub__mutmut_10,
}


def create_module_stub(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_module_stub__mutmut_orig, x_create_module_stub__mutmut_mutants, args, kwargs
    )
    return result


create_module_stub.__signature__ = _mutmut_signature(x_create_module_stub__mutmut_orig)
x_create_module_stub__mutmut_orig.__name__ = "x_create_module_stub"


__all__ = [
    "create_dependency_stub",
    "create_function_stub",
    "create_module_stub",
]


# <3 🧱🤝🧰🪄
