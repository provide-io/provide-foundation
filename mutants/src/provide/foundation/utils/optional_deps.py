# provide/foundation/utils/optional_deps.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

"""Centralized optional dependency handling with automatic stub creation.

This module provides utilities to handle optional dependencies in a DRY way,
reducing the repetitive try/except ImportError pattern across deps.py files.
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


class OptionalDependency:
    """Handles loading of optional dependencies with automatic stub generation.

    This centralizes the try/except ImportError pattern and provides
    automatic stub creation when dependencies are missing.

    Examples:
        >>> # Simple package import
        >>> click_dep = OptionalDependency("click", "cli")
        >>> click = click_dep.import_package()
        >>> has_click = click_dep.is_available()

        >>> # Import specific symbols from a module
        >>> crypto_dep = OptionalDependency("cryptography", "crypto")
        >>> Certificate, create_self_signed = crypto_dep.import_symbols(
        ...     "provide.foundation.crypto.certificates",
        ...     ["Certificate", "create_self_signed"]
        ... )
    """

    def xǁOptionalDependencyǁ__init____mutmut_orig(self, package_name: str, feature_name: str) -> None:
        """Initialize optional dependency handler.

        Args:
            package_name: Name of the optional package (e.g., "click", "cryptography")
            feature_name: Foundation feature name (e.g., "cli", "crypto")
        """
        self.package_name = package_name
        self.feature_name = feature_name
        self._available: bool | None = None

    def xǁOptionalDependencyǁ__init____mutmut_1(self, package_name: str, feature_name: str) -> None:
        """Initialize optional dependency handler.

        Args:
            package_name: Name of the optional package (e.g., "click", "cryptography")
            feature_name: Foundation feature name (e.g., "cli", "crypto")
        """
        self.package_name = None
        self.feature_name = feature_name
        self._available: bool | None = None

    def xǁOptionalDependencyǁ__init____mutmut_2(self, package_name: str, feature_name: str) -> None:
        """Initialize optional dependency handler.

        Args:
            package_name: Name of the optional package (e.g., "click", "cryptography")
            feature_name: Foundation feature name (e.g., "cli", "crypto")
        """
        self.package_name = package_name
        self.feature_name = None
        self._available: bool | None = None

    def xǁOptionalDependencyǁ__init____mutmut_3(self, package_name: str, feature_name: str) -> None:
        """Initialize optional dependency handler.

        Args:
            package_name: Name of the optional package (e.g., "click", "cryptography")
            feature_name: Foundation feature name (e.g., "cli", "crypto")
        """
        self.package_name = package_name
        self.feature_name = feature_name
        self._available: bool | None = ""
    
    xǁOptionalDependencyǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOptionalDependencyǁ__init____mutmut_1': xǁOptionalDependencyǁ__init____mutmut_1, 
        'xǁOptionalDependencyǁ__init____mutmut_2': xǁOptionalDependencyǁ__init____mutmut_2, 
        'xǁOptionalDependencyǁ__init____mutmut_3': xǁOptionalDependencyǁ__init____mutmut_3
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOptionalDependencyǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁOptionalDependencyǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁOptionalDependencyǁ__init____mutmut_orig)
    xǁOptionalDependencyǁ__init____mutmut_orig.__name__ = 'xǁOptionalDependencyǁ__init__'

    def xǁOptionalDependencyǁis_available__mutmut_orig(self) -> bool:
        """Check if the optional dependency is available.

        Returns:
            True if package can be imported, False otherwise
        """
        if self._available is None:
            try:
                __import__(self.package_name)
                self._available = True
            except ImportError:
                self._available = False
        return self._available

    def xǁOptionalDependencyǁis_available__mutmut_1(self) -> bool:
        """Check if the optional dependency is available.

        Returns:
            True if package can be imported, False otherwise
        """
        if self._available is not None:
            try:
                __import__(self.package_name)
                self._available = True
            except ImportError:
                self._available = False
        return self._available

    def xǁOptionalDependencyǁis_available__mutmut_2(self) -> bool:
        """Check if the optional dependency is available.

        Returns:
            True if package can be imported, False otherwise
        """
        if self._available is None:
            try:
                __import__(None)
                self._available = True
            except ImportError:
                self._available = False
        return self._available

    def xǁOptionalDependencyǁis_available__mutmut_3(self) -> bool:
        """Check if the optional dependency is available.

        Returns:
            True if package can be imported, False otherwise
        """
        if self._available is None:
            try:
                __import__(self.package_name)
                self._available = None
            except ImportError:
                self._available = False
        return self._available

    def xǁOptionalDependencyǁis_available__mutmut_4(self) -> bool:
        """Check if the optional dependency is available.

        Returns:
            True if package can be imported, False otherwise
        """
        if self._available is None:
            try:
                __import__(self.package_name)
                self._available = False
            except ImportError:
                self._available = False
        return self._available

    def xǁOptionalDependencyǁis_available__mutmut_5(self) -> bool:
        """Check if the optional dependency is available.

        Returns:
            True if package can be imported, False otherwise
        """
        if self._available is None:
            try:
                __import__(self.package_name)
                self._available = True
            except ImportError:
                self._available = None
        return self._available

    def xǁOptionalDependencyǁis_available__mutmut_6(self) -> bool:
        """Check if the optional dependency is available.

        Returns:
            True if package can be imported, False otherwise
        """
        if self._available is None:
            try:
                __import__(self.package_name)
                self._available = True
            except ImportError:
                self._available = True
        return self._available
    
    xǁOptionalDependencyǁis_available__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOptionalDependencyǁis_available__mutmut_1': xǁOptionalDependencyǁis_available__mutmut_1, 
        'xǁOptionalDependencyǁis_available__mutmut_2': xǁOptionalDependencyǁis_available__mutmut_2, 
        'xǁOptionalDependencyǁis_available__mutmut_3': xǁOptionalDependencyǁis_available__mutmut_3, 
        'xǁOptionalDependencyǁis_available__mutmut_4': xǁOptionalDependencyǁis_available__mutmut_4, 
        'xǁOptionalDependencyǁis_available__mutmut_5': xǁOptionalDependencyǁis_available__mutmut_5, 
        'xǁOptionalDependencyǁis_available__mutmut_6': xǁOptionalDependencyǁis_available__mutmut_6
    }
    
    def is_available(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOptionalDependencyǁis_available__mutmut_orig"), object.__getattribute__(self, "xǁOptionalDependencyǁis_available__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_available.__signature__ = _mutmut_signature(xǁOptionalDependencyǁis_available__mutmut_orig)
    xǁOptionalDependencyǁis_available__mutmut_orig.__name__ = 'xǁOptionalDependencyǁis_available'

    def xǁOptionalDependencyǁimport_package__mutmut_orig(self) -> Any:
        """Import the package or return a stub module.

        Returns:
            The actual package if available, otherwise a stub that raises DependencyError

        Example:
            >>> dep = OptionalDependency("click", "cli")
            >>> click = dep.import_package()  # Real click module or stub
        """
        if self.is_available():
            return __import__(self.package_name)

        # Return stub module
        from provide.foundation.utils.stubs import create_module_stub

        return create_module_stub(self.package_name, self.feature_name)

    def xǁOptionalDependencyǁimport_package__mutmut_1(self) -> Any:
        """Import the package or return a stub module.

        Returns:
            The actual package if available, otherwise a stub that raises DependencyError

        Example:
            >>> dep = OptionalDependency("click", "cli")
            >>> click = dep.import_package()  # Real click module or stub
        """
        if self.is_available():
            return __import__(None)

        # Return stub module
        from provide.foundation.utils.stubs import create_module_stub

        return create_module_stub(self.package_name, self.feature_name)

    def xǁOptionalDependencyǁimport_package__mutmut_2(self) -> Any:
        """Import the package or return a stub module.

        Returns:
            The actual package if available, otherwise a stub that raises DependencyError

        Example:
            >>> dep = OptionalDependency("click", "cli")
            >>> click = dep.import_package()  # Real click module or stub
        """
        if self.is_available():
            return __import__(self.package_name)

        # Return stub module
        from provide.foundation.utils.stubs import create_module_stub

        return create_module_stub(None, self.feature_name)

    def xǁOptionalDependencyǁimport_package__mutmut_3(self) -> Any:
        """Import the package or return a stub module.

        Returns:
            The actual package if available, otherwise a stub that raises DependencyError

        Example:
            >>> dep = OptionalDependency("click", "cli")
            >>> click = dep.import_package()  # Real click module or stub
        """
        if self.is_available():
            return __import__(self.package_name)

        # Return stub module
        from provide.foundation.utils.stubs import create_module_stub

        return create_module_stub(self.package_name, None)

    def xǁOptionalDependencyǁimport_package__mutmut_4(self) -> Any:
        """Import the package or return a stub module.

        Returns:
            The actual package if available, otherwise a stub that raises DependencyError

        Example:
            >>> dep = OptionalDependency("click", "cli")
            >>> click = dep.import_package()  # Real click module or stub
        """
        if self.is_available():
            return __import__(self.package_name)

        # Return stub module
        from provide.foundation.utils.stubs import create_module_stub

        return create_module_stub(self.feature_name)

    def xǁOptionalDependencyǁimport_package__mutmut_5(self) -> Any:
        """Import the package or return a stub module.

        Returns:
            The actual package if available, otherwise a stub that raises DependencyError

        Example:
            >>> dep = OptionalDependency("click", "cli")
            >>> click = dep.import_package()  # Real click module or stub
        """
        if self.is_available():
            return __import__(self.package_name)

        # Return stub module
        from provide.foundation.utils.stubs import create_module_stub

        return create_module_stub(self.package_name, )
    
    xǁOptionalDependencyǁimport_package__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOptionalDependencyǁimport_package__mutmut_1': xǁOptionalDependencyǁimport_package__mutmut_1, 
        'xǁOptionalDependencyǁimport_package__mutmut_2': xǁOptionalDependencyǁimport_package__mutmut_2, 
        'xǁOptionalDependencyǁimport_package__mutmut_3': xǁOptionalDependencyǁimport_package__mutmut_3, 
        'xǁOptionalDependencyǁimport_package__mutmut_4': xǁOptionalDependencyǁimport_package__mutmut_4, 
        'xǁOptionalDependencyǁimport_package__mutmut_5': xǁOptionalDependencyǁimport_package__mutmut_5
    }
    
    def import_package(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOptionalDependencyǁimport_package__mutmut_orig"), object.__getattribute__(self, "xǁOptionalDependencyǁimport_package__mutmut_mutants"), args, kwargs, self)
        return result 
    
    import_package.__signature__ = _mutmut_signature(xǁOptionalDependencyǁimport_package__mutmut_orig)
    xǁOptionalDependencyǁimport_package__mutmut_orig.__name__ = 'xǁOptionalDependencyǁimport_package'

    def xǁOptionalDependencyǁimport_symbols__mutmut_orig(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_1(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = False,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_2(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = None
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_3(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(None, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_4(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=None)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_5(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_6(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, )
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_7(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(None, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_8(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, None) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_9(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_10(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, ) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_11(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_12(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = None
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_13(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[1].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_14(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(None)
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_15(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(None, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_16(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, None))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_17(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_18(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, ))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_19(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(None)

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_20(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(None, self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_21(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, None))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_22(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.feature_name))

            return stubs

    def xǁOptionalDependencyǁimport_symbols__mutmut_23(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, ))

            return stubs
    
    xǁOptionalDependencyǁimport_symbols__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOptionalDependencyǁimport_symbols__mutmut_1': xǁOptionalDependencyǁimport_symbols__mutmut_1, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_2': xǁOptionalDependencyǁimport_symbols__mutmut_2, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_3': xǁOptionalDependencyǁimport_symbols__mutmut_3, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_4': xǁOptionalDependencyǁimport_symbols__mutmut_4, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_5': xǁOptionalDependencyǁimport_symbols__mutmut_5, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_6': xǁOptionalDependencyǁimport_symbols__mutmut_6, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_7': xǁOptionalDependencyǁimport_symbols__mutmut_7, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_8': xǁOptionalDependencyǁimport_symbols__mutmut_8, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_9': xǁOptionalDependencyǁimport_symbols__mutmut_9, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_10': xǁOptionalDependencyǁimport_symbols__mutmut_10, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_11': xǁOptionalDependencyǁimport_symbols__mutmut_11, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_12': xǁOptionalDependencyǁimport_symbols__mutmut_12, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_13': xǁOptionalDependencyǁimport_symbols__mutmut_13, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_14': xǁOptionalDependencyǁimport_symbols__mutmut_14, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_15': xǁOptionalDependencyǁimport_symbols__mutmut_15, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_16': xǁOptionalDependencyǁimport_symbols__mutmut_16, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_17': xǁOptionalDependencyǁimport_symbols__mutmut_17, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_18': xǁOptionalDependencyǁimport_symbols__mutmut_18, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_19': xǁOptionalDependencyǁimport_symbols__mutmut_19, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_20': xǁOptionalDependencyǁimport_symbols__mutmut_20, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_21': xǁOptionalDependencyǁimport_symbols__mutmut_21, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_22': xǁOptionalDependencyǁimport_symbols__mutmut_22, 
        'xǁOptionalDependencyǁimport_symbols__mutmut_23': xǁOptionalDependencyǁimport_symbols__mutmut_23
    }
    
    def import_symbols(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOptionalDependencyǁimport_symbols__mutmut_orig"), object.__getattribute__(self, "xǁOptionalDependencyǁimport_symbols__mutmut_mutants"), args, kwargs, self)
        return result 
    
    import_symbols.__signature__ = _mutmut_signature(xǁOptionalDependencyǁimport_symbols__mutmut_orig)
    xǁOptionalDependencyǁimport_symbols__mutmut_orig.__name__ = 'xǁOptionalDependencyǁimport_symbols'


def x_load_optional_dependency__mutmut_orig(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = OptionalDependency(package_name, feature_name)
    is_available = dep.is_available()

    if module_path and symbols:
        # Import specific symbols
        imported = dep.import_symbols(module_path, symbols)
        return is_available, imported

    # Import entire package
    imported = dep.import_package()
    return is_available, imported


def x_load_optional_dependency__mutmut_1(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = None
    is_available = dep.is_available()

    if module_path and symbols:
        # Import specific symbols
        imported = dep.import_symbols(module_path, symbols)
        return is_available, imported

    # Import entire package
    imported = dep.import_package()
    return is_available, imported


def x_load_optional_dependency__mutmut_2(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = OptionalDependency(None, feature_name)
    is_available = dep.is_available()

    if module_path and symbols:
        # Import specific symbols
        imported = dep.import_symbols(module_path, symbols)
        return is_available, imported

    # Import entire package
    imported = dep.import_package()
    return is_available, imported


def x_load_optional_dependency__mutmut_3(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = OptionalDependency(package_name, None)
    is_available = dep.is_available()

    if module_path and symbols:
        # Import specific symbols
        imported = dep.import_symbols(module_path, symbols)
        return is_available, imported

    # Import entire package
    imported = dep.import_package()
    return is_available, imported


def x_load_optional_dependency__mutmut_4(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = OptionalDependency(feature_name)
    is_available = dep.is_available()

    if module_path and symbols:
        # Import specific symbols
        imported = dep.import_symbols(module_path, symbols)
        return is_available, imported

    # Import entire package
    imported = dep.import_package()
    return is_available, imported


def x_load_optional_dependency__mutmut_5(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = OptionalDependency(package_name, )
    is_available = dep.is_available()

    if module_path and symbols:
        # Import specific symbols
        imported = dep.import_symbols(module_path, symbols)
        return is_available, imported

    # Import entire package
    imported = dep.import_package()
    return is_available, imported


def x_load_optional_dependency__mutmut_6(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = OptionalDependency(package_name, feature_name)
    is_available = None

    if module_path and symbols:
        # Import specific symbols
        imported = dep.import_symbols(module_path, symbols)
        return is_available, imported

    # Import entire package
    imported = dep.import_package()
    return is_available, imported


def x_load_optional_dependency__mutmut_7(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = OptionalDependency(package_name, feature_name)
    is_available = dep.is_available()

    if module_path or symbols:
        # Import specific symbols
        imported = dep.import_symbols(module_path, symbols)
        return is_available, imported

    # Import entire package
    imported = dep.import_package()
    return is_available, imported


def x_load_optional_dependency__mutmut_8(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = OptionalDependency(package_name, feature_name)
    is_available = dep.is_available()

    if module_path and symbols:
        # Import specific symbols
        imported = None
        return is_available, imported

    # Import entire package
    imported = dep.import_package()
    return is_available, imported


def x_load_optional_dependency__mutmut_9(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = OptionalDependency(package_name, feature_name)
    is_available = dep.is_available()

    if module_path and symbols:
        # Import specific symbols
        imported = dep.import_symbols(None, symbols)
        return is_available, imported

    # Import entire package
    imported = dep.import_package()
    return is_available, imported


def x_load_optional_dependency__mutmut_10(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = OptionalDependency(package_name, feature_name)
    is_available = dep.is_available()

    if module_path and symbols:
        # Import specific symbols
        imported = dep.import_symbols(module_path, None)
        return is_available, imported

    # Import entire package
    imported = dep.import_package()
    return is_available, imported


def x_load_optional_dependency__mutmut_11(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = OptionalDependency(package_name, feature_name)
    is_available = dep.is_available()

    if module_path and symbols:
        # Import specific symbols
        imported = dep.import_symbols(symbols)
        return is_available, imported

    # Import entire package
    imported = dep.import_package()
    return is_available, imported


def x_load_optional_dependency__mutmut_12(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = OptionalDependency(package_name, feature_name)
    is_available = dep.is_available()

    if module_path and symbols:
        # Import specific symbols
        imported = dep.import_symbols(module_path, )
        return is_available, imported

    # Import entire package
    imported = dep.import_package()
    return is_available, imported


def x_load_optional_dependency__mutmut_13(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = OptionalDependency(package_name, feature_name)
    is_available = dep.is_available()

    if module_path and symbols:
        # Import specific symbols
        imported = dep.import_symbols(module_path, symbols)
        return is_available, imported

    # Import entire package
    imported = None
    return is_available, imported

x_load_optional_dependency__mutmut_mutants : ClassVar[MutantDict] = {
'x_load_optional_dependency__mutmut_1': x_load_optional_dependency__mutmut_1, 
    'x_load_optional_dependency__mutmut_2': x_load_optional_dependency__mutmut_2, 
    'x_load_optional_dependency__mutmut_3': x_load_optional_dependency__mutmut_3, 
    'x_load_optional_dependency__mutmut_4': x_load_optional_dependency__mutmut_4, 
    'x_load_optional_dependency__mutmut_5': x_load_optional_dependency__mutmut_5, 
    'x_load_optional_dependency__mutmut_6': x_load_optional_dependency__mutmut_6, 
    'x_load_optional_dependency__mutmut_7': x_load_optional_dependency__mutmut_7, 
    'x_load_optional_dependency__mutmut_8': x_load_optional_dependency__mutmut_8, 
    'x_load_optional_dependency__mutmut_9': x_load_optional_dependency__mutmut_9, 
    'x_load_optional_dependency__mutmut_10': x_load_optional_dependency__mutmut_10, 
    'x_load_optional_dependency__mutmut_11': x_load_optional_dependency__mutmut_11, 
    'x_load_optional_dependency__mutmut_12': x_load_optional_dependency__mutmut_12, 
    'x_load_optional_dependency__mutmut_13': x_load_optional_dependency__mutmut_13
}

def load_optional_dependency(*args, **kwargs):
    result = _mutmut_trampoline(x_load_optional_dependency__mutmut_orig, x_load_optional_dependency__mutmut_mutants, args, kwargs)
    return result 

load_optional_dependency.__signature__ = _mutmut_signature(x_load_optional_dependency__mutmut_orig)
x_load_optional_dependency__mutmut_orig.__name__ = 'x_load_optional_dependency'


__all__ = [
    "OptionalDependency",
    "load_optional_dependency",
]


# <3 🧱🤝🧰🪄
