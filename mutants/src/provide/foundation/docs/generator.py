# provide/foundation/docs/generator.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""API documentation generator for MkDocs with mkdocstrings."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from provide.foundation.errors import DependencyError
from provide.foundation.logger import get_logger

log = get_logger(__name__)

try:
    import mkdocs_gen_files

    _HAS_MKDOCS = True
except ImportError:
    mkdocs_gen_files = None  # type: ignore[assignment]
    _HAS_MKDOCS = False
    log.warning("mkdocs_gen_files not available - doc generation disabled")
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


class APIDocGenerator:
    """Generate API reference documentation for MkDocs."""

    def xǁAPIDocGeneratorǁ__init____mutmut_orig(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_1(
        self,
        src_root: str = "XXsrcXX",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_2(
        self,
        src_root: str = "SRC",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_3(
        self,
        src_root: str = "src",
        api_dir: str = "XXapi/referenceXX",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_4(
        self,
        src_root: str = "src",
        api_dir: str = "API/REFERENCE",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_5(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 101,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_6(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = False,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_7(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = False,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_8(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = None
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_9(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(None)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_10(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = None
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_11(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = None
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_12(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns and {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_13(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"XX__pycache__XX", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_14(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__PYCACHE__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_15(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "XXtestXX", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_16(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "TEST", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_17(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "XXtestsXX"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_18(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "TESTS"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_19(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = None
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_20(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = None
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_21(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = None
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_22(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = None
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_23(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = None

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_24(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is not None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_25(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError(None, feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_26(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature=None)

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_27(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError(feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_28(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError(
                "mkdocs-gen-files",
            )

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_29(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("XXmkdocs-gen-filesXX", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_30(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("MKDOCS-GEN-FILES", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_31(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="XXdocsXX")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_32(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="DOCS")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_33(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = None
        self._processed_files: set[Path] = set()

    def xǁAPIDocGeneratorǁ__init____mutmut_34(
        self,
        src_root: str = "src",
        api_dir: str = "api/reference",
        skip_patterns: set[str] | None = None,
        package_prefix: str | None = None,
        min_init_size: int = 100,
        show_source: bool = True,
        show_inheritance: bool = True,
        custom_index_content: str | None = None,
    ) -> None:
        """Initialize the API documentation generator.

        Args:
            src_root: Root directory of source code
            api_dir: Output directory for API docs
            skip_patterns: Patterns to skip (e.g., {"test", "__pycache__"})
            package_prefix: Package prefix to use (e.g., "flavor" or "provide.foundation")
            min_init_size: Minimum size for __init__.py files to include (bytes)
            show_source: Whether to show source code links
            show_inheritance: Whether to show inheritance information
            custom_index_content: Custom content for the API index page
        """
        self.src_root = Path(src_root)
        self.api_dir = api_dir
        self.skip_patterns = skip_patterns or {"__pycache__", "test", "tests"}
        self.package_prefix = package_prefix
        self.min_init_size = min_init_size
        self.show_source = show_source
        self.show_inheritance = show_inheritance
        self.custom_index_content = custom_index_content

        if mkdocs_gen_files is None:
            raise DependencyError("mkdocs-gen-files", feature="docs")

        self.nav = mkdocs_gen_files.Nav()
        self._processed_files: set[Path] = None

    xǁAPIDocGeneratorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAPIDocGeneratorǁ__init____mutmut_1": xǁAPIDocGeneratorǁ__init____mutmut_1,
        "xǁAPIDocGeneratorǁ__init____mutmut_2": xǁAPIDocGeneratorǁ__init____mutmut_2,
        "xǁAPIDocGeneratorǁ__init____mutmut_3": xǁAPIDocGeneratorǁ__init____mutmut_3,
        "xǁAPIDocGeneratorǁ__init____mutmut_4": xǁAPIDocGeneratorǁ__init____mutmut_4,
        "xǁAPIDocGeneratorǁ__init____mutmut_5": xǁAPIDocGeneratorǁ__init____mutmut_5,
        "xǁAPIDocGeneratorǁ__init____mutmut_6": xǁAPIDocGeneratorǁ__init____mutmut_6,
        "xǁAPIDocGeneratorǁ__init____mutmut_7": xǁAPIDocGeneratorǁ__init____mutmut_7,
        "xǁAPIDocGeneratorǁ__init____mutmut_8": xǁAPIDocGeneratorǁ__init____mutmut_8,
        "xǁAPIDocGeneratorǁ__init____mutmut_9": xǁAPIDocGeneratorǁ__init____mutmut_9,
        "xǁAPIDocGeneratorǁ__init____mutmut_10": xǁAPIDocGeneratorǁ__init____mutmut_10,
        "xǁAPIDocGeneratorǁ__init____mutmut_11": xǁAPIDocGeneratorǁ__init____mutmut_11,
        "xǁAPIDocGeneratorǁ__init____mutmut_12": xǁAPIDocGeneratorǁ__init____mutmut_12,
        "xǁAPIDocGeneratorǁ__init____mutmut_13": xǁAPIDocGeneratorǁ__init____mutmut_13,
        "xǁAPIDocGeneratorǁ__init____mutmut_14": xǁAPIDocGeneratorǁ__init____mutmut_14,
        "xǁAPIDocGeneratorǁ__init____mutmut_15": xǁAPIDocGeneratorǁ__init____mutmut_15,
        "xǁAPIDocGeneratorǁ__init____mutmut_16": xǁAPIDocGeneratorǁ__init____mutmut_16,
        "xǁAPIDocGeneratorǁ__init____mutmut_17": xǁAPIDocGeneratorǁ__init____mutmut_17,
        "xǁAPIDocGeneratorǁ__init____mutmut_18": xǁAPIDocGeneratorǁ__init____mutmut_18,
        "xǁAPIDocGeneratorǁ__init____mutmut_19": xǁAPIDocGeneratorǁ__init____mutmut_19,
        "xǁAPIDocGeneratorǁ__init____mutmut_20": xǁAPIDocGeneratorǁ__init____mutmut_20,
        "xǁAPIDocGeneratorǁ__init____mutmut_21": xǁAPIDocGeneratorǁ__init____mutmut_21,
        "xǁAPIDocGeneratorǁ__init____mutmut_22": xǁAPIDocGeneratorǁ__init____mutmut_22,
        "xǁAPIDocGeneratorǁ__init____mutmut_23": xǁAPIDocGeneratorǁ__init____mutmut_23,
        "xǁAPIDocGeneratorǁ__init____mutmut_24": xǁAPIDocGeneratorǁ__init____mutmut_24,
        "xǁAPIDocGeneratorǁ__init____mutmut_25": xǁAPIDocGeneratorǁ__init____mutmut_25,
        "xǁAPIDocGeneratorǁ__init____mutmut_26": xǁAPIDocGeneratorǁ__init____mutmut_26,
        "xǁAPIDocGeneratorǁ__init____mutmut_27": xǁAPIDocGeneratorǁ__init____mutmut_27,
        "xǁAPIDocGeneratorǁ__init____mutmut_28": xǁAPIDocGeneratorǁ__init____mutmut_28,
        "xǁAPIDocGeneratorǁ__init____mutmut_29": xǁAPIDocGeneratorǁ__init____mutmut_29,
        "xǁAPIDocGeneratorǁ__init____mutmut_30": xǁAPIDocGeneratorǁ__init____mutmut_30,
        "xǁAPIDocGeneratorǁ__init____mutmut_31": xǁAPIDocGeneratorǁ__init____mutmut_31,
        "xǁAPIDocGeneratorǁ__init____mutmut_32": xǁAPIDocGeneratorǁ__init____mutmut_32,
        "xǁAPIDocGeneratorǁ__init____mutmut_33": xǁAPIDocGeneratorǁ__init____mutmut_33,
        "xǁAPIDocGeneratorǁ__init____mutmut_34": xǁAPIDocGeneratorǁ__init____mutmut_34,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAPIDocGeneratorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁAPIDocGeneratorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁAPIDocGeneratorǁ__init____mutmut_orig)
    xǁAPIDocGeneratorǁ__init____mutmut_orig.__name__ = "xǁAPIDocGeneratorǁ__init__"

    def xǁAPIDocGeneratorǁshould_skip__mutmut_orig(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_1(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = None
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_2(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(None)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_3(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern not in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_4(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(None)
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_5(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return False

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_6(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name != "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_7(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "XX__init__.pyXX":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_8(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__INIT__.PY":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_9(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size <= self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_10(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(None)
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_11(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return False
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_12(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(None)
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_13(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return False

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_14(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = None
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_15(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(None).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_16(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") or part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_17(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith(None) and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_18(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("XX_XX") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_19(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part == "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_20(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "XX__init__.pyXX":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_21(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__INIT__.PY":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_22(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(None)
                return True

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_23(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return False

        return False

    def xǁAPIDocGeneratorǁshould_skip__mutmut_24(self, path: Path) -> bool:
        """Check if a path should be skipped.

        Args:
            path: Path to check

        Returns:
            True if path should be skipped
        """
        # Skip patterns
        path_str = str(path)
        for pattern in self.skip_patterns:
            if pattern in path_str:
                log.debug(f"Skipping {path} - matches pattern '{pattern}'")
                return True

        # Skip empty __init__.py files
        if path.name == "__init__.py":
            try:
                if path.stat().st_size < self.min_init_size:
                    log.debug(f"Skipping {path} - too small ({path.stat().st_size} bytes)")
                    return True
            except OSError:
                log.warning(f"Could not stat {path}")
                return True

        # Skip private modules (but allow __init__.py)
        parts = path.relative_to(self.src_root).parts
        for part in parts:
            if part.startswith("_") and part != "__init__.py":
                log.debug(f"Skipping {path} - contains private module '{part}'")
                return True

        return True

    xǁAPIDocGeneratorǁshould_skip__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAPIDocGeneratorǁshould_skip__mutmut_1": xǁAPIDocGeneratorǁshould_skip__mutmut_1,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_2": xǁAPIDocGeneratorǁshould_skip__mutmut_2,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_3": xǁAPIDocGeneratorǁshould_skip__mutmut_3,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_4": xǁAPIDocGeneratorǁshould_skip__mutmut_4,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_5": xǁAPIDocGeneratorǁshould_skip__mutmut_5,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_6": xǁAPIDocGeneratorǁshould_skip__mutmut_6,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_7": xǁAPIDocGeneratorǁshould_skip__mutmut_7,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_8": xǁAPIDocGeneratorǁshould_skip__mutmut_8,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_9": xǁAPIDocGeneratorǁshould_skip__mutmut_9,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_10": xǁAPIDocGeneratorǁshould_skip__mutmut_10,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_11": xǁAPIDocGeneratorǁshould_skip__mutmut_11,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_12": xǁAPIDocGeneratorǁshould_skip__mutmut_12,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_13": xǁAPIDocGeneratorǁshould_skip__mutmut_13,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_14": xǁAPIDocGeneratorǁshould_skip__mutmut_14,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_15": xǁAPIDocGeneratorǁshould_skip__mutmut_15,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_16": xǁAPIDocGeneratorǁshould_skip__mutmut_16,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_17": xǁAPIDocGeneratorǁshould_skip__mutmut_17,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_18": xǁAPIDocGeneratorǁshould_skip__mutmut_18,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_19": xǁAPIDocGeneratorǁshould_skip__mutmut_19,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_20": xǁAPIDocGeneratorǁshould_skip__mutmut_20,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_21": xǁAPIDocGeneratorǁshould_skip__mutmut_21,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_22": xǁAPIDocGeneratorǁshould_skip__mutmut_22,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_23": xǁAPIDocGeneratorǁshould_skip__mutmut_23,
        "xǁAPIDocGeneratorǁshould_skip__mutmut_24": xǁAPIDocGeneratorǁshould_skip__mutmut_24,
    }

    def should_skip(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAPIDocGeneratorǁshould_skip__mutmut_orig"),
            object.__getattribute__(self, "xǁAPIDocGeneratorǁshould_skip__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    should_skip.__signature__ = _mutmut_signature(xǁAPIDocGeneratorǁshould_skip__mutmut_orig)
    xǁAPIDocGeneratorǁshould_skip__mutmut_orig.__name__ = "xǁAPIDocGeneratorǁshould_skip"

    def xǁAPIDocGeneratorǁget_module_identifier__mutmut_orig(self, parts: list[str]) -> str:
        """Get the full module identifier for a set of path parts.

        Args:
            parts: Module path parts

        Returns:
            Full module identifier
        """
        if self.package_prefix:
            # If package prefix is provided, prepend it
            return f"{self.package_prefix}.{'.'.join(parts)}"
        return ".".join(parts)

    def xǁAPIDocGeneratorǁget_module_identifier__mutmut_1(self, parts: list[str]) -> str:
        """Get the full module identifier for a set of path parts.

        Args:
            parts: Module path parts

        Returns:
            Full module identifier
        """
        if self.package_prefix:
            # If package prefix is provided, prepend it
            return f"{self.package_prefix}.{'.'.join(None)}"
        return ".".join(parts)

    def xǁAPIDocGeneratorǁget_module_identifier__mutmut_2(self, parts: list[str]) -> str:
        """Get the full module identifier for a set of path parts.

        Args:
            parts: Module path parts

        Returns:
            Full module identifier
        """
        if self.package_prefix:
            # If package prefix is provided, prepend it
            return f"{self.package_prefix}.{'XX.XX'.join(parts)}"
        return ".".join(parts)

    def xǁAPIDocGeneratorǁget_module_identifier__mutmut_3(self, parts: list[str]) -> str:
        """Get the full module identifier for a set of path parts.

        Args:
            parts: Module path parts

        Returns:
            Full module identifier
        """
        if self.package_prefix:
            # If package prefix is provided, prepend it
            return f"{self.package_prefix}.{'.'.join(parts)}"
        return ".".join(None)

    def xǁAPIDocGeneratorǁget_module_identifier__mutmut_4(self, parts: list[str]) -> str:
        """Get the full module identifier for a set of path parts.

        Args:
            parts: Module path parts

        Returns:
            Full module identifier
        """
        if self.package_prefix:
            # If package prefix is provided, prepend it
            return f"{self.package_prefix}.{'.'.join(parts)}"
        return "XX.XX".join(parts)

    xǁAPIDocGeneratorǁget_module_identifier__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAPIDocGeneratorǁget_module_identifier__mutmut_1": xǁAPIDocGeneratorǁget_module_identifier__mutmut_1,
        "xǁAPIDocGeneratorǁget_module_identifier__mutmut_2": xǁAPIDocGeneratorǁget_module_identifier__mutmut_2,
        "xǁAPIDocGeneratorǁget_module_identifier__mutmut_3": xǁAPIDocGeneratorǁget_module_identifier__mutmut_3,
        "xǁAPIDocGeneratorǁget_module_identifier__mutmut_4": xǁAPIDocGeneratorǁget_module_identifier__mutmut_4,
    }

    def get_module_identifier(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAPIDocGeneratorǁget_module_identifier__mutmut_orig"),
            object.__getattribute__(self, "xǁAPIDocGeneratorǁget_module_identifier__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_module_identifier.__signature__ = _mutmut_signature(
        xǁAPIDocGeneratorǁget_module_identifier__mutmut_orig
    )
    xǁAPIDocGeneratorǁget_module_identifier__mutmut_orig.__name__ = "xǁAPIDocGeneratorǁget_module_identifier"

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_orig(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_1(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(None, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_2(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, None) as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_3(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open("w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_4(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(
            doc_path,
        ) as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_5(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "XXwXX") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_6(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "W") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_7(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(None)
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_8(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(None)

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_9(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source and not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_10(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_11(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_12(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write(None)
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_13(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("XX    options:\nXX")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_14(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    OPTIONS:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_15(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_16(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write(None)
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_17(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("XX      show_source: false\nXX")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_18(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      SHOW_SOURCE: FALSE\n")
                if not self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_19(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if self.show_inheritance:
                    fd.write("      show_bases: false\n")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_20(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write(None)

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_21(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("XX      show_bases: false\nXX")

    def xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_22(
        self, doc_path: Path, identifier: str, title: str
    ) -> None:
        """Generate documentation for a single module.

        Args:
            doc_path: Path where documentation should be written
            identifier: Module identifier for mkdocstrings
            title: Title for the documentation page
        """
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            fd.write(f"# {title}\n\n")
            fd.write(f"::: {identifier}\n")

            # Add configuration options
            if not self.show_source or not self.show_inheritance:
                fd.write("    options:\n")
                if not self.show_source:
                    fd.write("      show_source: false\n")
                if not self.show_inheritance:
                    fd.write("      SHOW_BASES: FALSE\n")

    xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_1": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_1,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_2": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_2,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_3": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_3,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_4": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_4,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_5": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_5,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_6": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_6,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_7": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_7,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_8": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_8,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_9": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_9,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_10": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_10,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_11": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_11,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_12": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_12,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_13": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_13,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_14": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_14,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_15": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_15,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_16": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_16,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_17": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_17,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_18": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_18,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_19": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_19,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_20": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_20,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_21": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_21,
        "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_22": xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_22,
    }

    def generate_module_doc(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_orig"),
            object.__getattribute__(self, "xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    generate_module_doc.__signature__ = _mutmut_signature(xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_orig)
    xǁAPIDocGeneratorǁgenerate_module_doc__mutmut_orig.__name__ = "xǁAPIDocGeneratorǁgenerate_module_doc"

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_orig(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_1(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path not in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_2(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(None)

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_3(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = None
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_4(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix(None)
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_5(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(None).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_6(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("XXXX")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_7(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = None

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_8(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) * module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_9(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(None) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_10(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(None)

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_11(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix("XX.mdXX")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_12(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".MD")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_13(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = None
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_14(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(None)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_15(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[+1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_16(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-2] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_17(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] != "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_18(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "XX__init__XX":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_19(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__INIT__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_20(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = None
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_21(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:+1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_22(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-2]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_23(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = None

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_24(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name(None)

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_25(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("XXindex.mdXX")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_26(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("INDEX.MD")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_27(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_28(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = None

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_29(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(None)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_30(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = None
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_31(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(None)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_32(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = None

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_33(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(None, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_34(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, None, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_35(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, None)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_36(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_37(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_38(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(
            doc_path,
            identifier,
        )

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_39(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(None, path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_40(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, None)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_41(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(path)

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_42(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(
            doc_path,
        )

        self._processed_files.add(path)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_43(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(None)
        log.debug(f"Generated documentation for {identifier} -> {doc_path}")

    def xǁAPIDocGeneratorǁprocess_python_file__mutmut_44(self, path: Path) -> None:
        """Process a single Python file for documentation.

        Args:
            path: Python file to process
        """
        if path in self._processed_files:
            return

        log.debug(f"Processing {path}")

        # Convert to module path
        module_path = path.relative_to(self.src_root).with_suffix("")
        doc_path = Path(self.api_dir) / module_path.with_suffix(".md")

        # Handle __init__.py files
        parts = list(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")

        if not parts:
            return

        # Add to navigation
        self.nav[tuple(parts)] = doc_path.as_posix()

        # Generate markdown file
        identifier = self.get_module_identifier(parts)
        title = f"`{identifier}`"

        self.generate_module_doc(doc_path, identifier, title)

        # Set edit path for the generated file
        mkdocs_gen_files.set_edit_path(doc_path, path)

        self._processed_files.add(path)
        log.debug(None)

    xǁAPIDocGeneratorǁprocess_python_file__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_1": xǁAPIDocGeneratorǁprocess_python_file__mutmut_1,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_2": xǁAPIDocGeneratorǁprocess_python_file__mutmut_2,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_3": xǁAPIDocGeneratorǁprocess_python_file__mutmut_3,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_4": xǁAPIDocGeneratorǁprocess_python_file__mutmut_4,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_5": xǁAPIDocGeneratorǁprocess_python_file__mutmut_5,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_6": xǁAPIDocGeneratorǁprocess_python_file__mutmut_6,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_7": xǁAPIDocGeneratorǁprocess_python_file__mutmut_7,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_8": xǁAPIDocGeneratorǁprocess_python_file__mutmut_8,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_9": xǁAPIDocGeneratorǁprocess_python_file__mutmut_9,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_10": xǁAPIDocGeneratorǁprocess_python_file__mutmut_10,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_11": xǁAPIDocGeneratorǁprocess_python_file__mutmut_11,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_12": xǁAPIDocGeneratorǁprocess_python_file__mutmut_12,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_13": xǁAPIDocGeneratorǁprocess_python_file__mutmut_13,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_14": xǁAPIDocGeneratorǁprocess_python_file__mutmut_14,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_15": xǁAPIDocGeneratorǁprocess_python_file__mutmut_15,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_16": xǁAPIDocGeneratorǁprocess_python_file__mutmut_16,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_17": xǁAPIDocGeneratorǁprocess_python_file__mutmut_17,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_18": xǁAPIDocGeneratorǁprocess_python_file__mutmut_18,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_19": xǁAPIDocGeneratorǁprocess_python_file__mutmut_19,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_20": xǁAPIDocGeneratorǁprocess_python_file__mutmut_20,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_21": xǁAPIDocGeneratorǁprocess_python_file__mutmut_21,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_22": xǁAPIDocGeneratorǁprocess_python_file__mutmut_22,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_23": xǁAPIDocGeneratorǁprocess_python_file__mutmut_23,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_24": xǁAPIDocGeneratorǁprocess_python_file__mutmut_24,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_25": xǁAPIDocGeneratorǁprocess_python_file__mutmut_25,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_26": xǁAPIDocGeneratorǁprocess_python_file__mutmut_26,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_27": xǁAPIDocGeneratorǁprocess_python_file__mutmut_27,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_28": xǁAPIDocGeneratorǁprocess_python_file__mutmut_28,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_29": xǁAPIDocGeneratorǁprocess_python_file__mutmut_29,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_30": xǁAPIDocGeneratorǁprocess_python_file__mutmut_30,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_31": xǁAPIDocGeneratorǁprocess_python_file__mutmut_31,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_32": xǁAPIDocGeneratorǁprocess_python_file__mutmut_32,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_33": xǁAPIDocGeneratorǁprocess_python_file__mutmut_33,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_34": xǁAPIDocGeneratorǁprocess_python_file__mutmut_34,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_35": xǁAPIDocGeneratorǁprocess_python_file__mutmut_35,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_36": xǁAPIDocGeneratorǁprocess_python_file__mutmut_36,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_37": xǁAPIDocGeneratorǁprocess_python_file__mutmut_37,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_38": xǁAPIDocGeneratorǁprocess_python_file__mutmut_38,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_39": xǁAPIDocGeneratorǁprocess_python_file__mutmut_39,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_40": xǁAPIDocGeneratorǁprocess_python_file__mutmut_40,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_41": xǁAPIDocGeneratorǁprocess_python_file__mutmut_41,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_42": xǁAPIDocGeneratorǁprocess_python_file__mutmut_42,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_43": xǁAPIDocGeneratorǁprocess_python_file__mutmut_43,
        "xǁAPIDocGeneratorǁprocess_python_file__mutmut_44": xǁAPIDocGeneratorǁprocess_python_file__mutmut_44,
    }

    def process_python_file(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAPIDocGeneratorǁprocess_python_file__mutmut_orig"),
            object.__getattribute__(self, "xǁAPIDocGeneratorǁprocess_python_file__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    process_python_file.__signature__ = _mutmut_signature(xǁAPIDocGeneratorǁprocess_python_file__mutmut_orig)
    xǁAPIDocGeneratorǁprocess_python_file__mutmut_orig.__name__ = "xǁAPIDocGeneratorǁprocess_python_file"

    def xǁAPIDocGeneratorǁgenerate_navigation__mutmut_orig(self) -> None:
        """Generate the navigation summary file."""
        nav_path = f"{self.api_dir}/SUMMARY.md"
        with mkdocs_gen_files.open(nav_path, "w") as nav_file:
            nav_file.writelines(self.nav.build_literate_nav())
        log.debug(f"Generated navigation file: {nav_path}")

    def xǁAPIDocGeneratorǁgenerate_navigation__mutmut_1(self) -> None:
        """Generate the navigation summary file."""
        nav_path = None
        with mkdocs_gen_files.open(nav_path, "w") as nav_file:
            nav_file.writelines(self.nav.build_literate_nav())
        log.debug(f"Generated navigation file: {nav_path}")

    def xǁAPIDocGeneratorǁgenerate_navigation__mutmut_2(self) -> None:
        """Generate the navigation summary file."""
        nav_path = f"{self.api_dir}/SUMMARY.md"
        with mkdocs_gen_files.open(None, "w") as nav_file:
            nav_file.writelines(self.nav.build_literate_nav())
        log.debug(f"Generated navigation file: {nav_path}")

    def xǁAPIDocGeneratorǁgenerate_navigation__mutmut_3(self) -> None:
        """Generate the navigation summary file."""
        nav_path = f"{self.api_dir}/SUMMARY.md"
        with mkdocs_gen_files.open(nav_path, None) as nav_file:
            nav_file.writelines(self.nav.build_literate_nav())
        log.debug(f"Generated navigation file: {nav_path}")

    def xǁAPIDocGeneratorǁgenerate_navigation__mutmut_4(self) -> None:
        """Generate the navigation summary file."""
        nav_path = f"{self.api_dir}/SUMMARY.md"
        with mkdocs_gen_files.open("w") as nav_file:
            nav_file.writelines(self.nav.build_literate_nav())
        log.debug(f"Generated navigation file: {nav_path}")

    def xǁAPIDocGeneratorǁgenerate_navigation__mutmut_5(self) -> None:
        """Generate the navigation summary file."""
        nav_path = f"{self.api_dir}/SUMMARY.md"
        with mkdocs_gen_files.open(
            nav_path,
        ) as nav_file:
            nav_file.writelines(self.nav.build_literate_nav())
        log.debug(f"Generated navigation file: {nav_path}")

    def xǁAPIDocGeneratorǁgenerate_navigation__mutmut_6(self) -> None:
        """Generate the navigation summary file."""
        nav_path = f"{self.api_dir}/SUMMARY.md"
        with mkdocs_gen_files.open(nav_path, "XXwXX") as nav_file:
            nav_file.writelines(self.nav.build_literate_nav())
        log.debug(f"Generated navigation file: {nav_path}")

    def xǁAPIDocGeneratorǁgenerate_navigation__mutmut_7(self) -> None:
        """Generate the navigation summary file."""
        nav_path = f"{self.api_dir}/SUMMARY.md"
        with mkdocs_gen_files.open(nav_path, "W") as nav_file:
            nav_file.writelines(self.nav.build_literate_nav())
        log.debug(f"Generated navigation file: {nav_path}")

    def xǁAPIDocGeneratorǁgenerate_navigation__mutmut_8(self) -> None:
        """Generate the navigation summary file."""
        nav_path = f"{self.api_dir}/SUMMARY.md"
        with mkdocs_gen_files.open(nav_path, "w") as nav_file:
            nav_file.writelines(None)
        log.debug(f"Generated navigation file: {nav_path}")

    def xǁAPIDocGeneratorǁgenerate_navigation__mutmut_9(self) -> None:
        """Generate the navigation summary file."""
        nav_path = f"{self.api_dir}/SUMMARY.md"
        with mkdocs_gen_files.open(nav_path, "w") as nav_file:
            nav_file.writelines(self.nav.build_literate_nav())
        log.debug(None)

    xǁAPIDocGeneratorǁgenerate_navigation__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAPIDocGeneratorǁgenerate_navigation__mutmut_1": xǁAPIDocGeneratorǁgenerate_navigation__mutmut_1,
        "xǁAPIDocGeneratorǁgenerate_navigation__mutmut_2": xǁAPIDocGeneratorǁgenerate_navigation__mutmut_2,
        "xǁAPIDocGeneratorǁgenerate_navigation__mutmut_3": xǁAPIDocGeneratorǁgenerate_navigation__mutmut_3,
        "xǁAPIDocGeneratorǁgenerate_navigation__mutmut_4": xǁAPIDocGeneratorǁgenerate_navigation__mutmut_4,
        "xǁAPIDocGeneratorǁgenerate_navigation__mutmut_5": xǁAPIDocGeneratorǁgenerate_navigation__mutmut_5,
        "xǁAPIDocGeneratorǁgenerate_navigation__mutmut_6": xǁAPIDocGeneratorǁgenerate_navigation__mutmut_6,
        "xǁAPIDocGeneratorǁgenerate_navigation__mutmut_7": xǁAPIDocGeneratorǁgenerate_navigation__mutmut_7,
        "xǁAPIDocGeneratorǁgenerate_navigation__mutmut_8": xǁAPIDocGeneratorǁgenerate_navigation__mutmut_8,
        "xǁAPIDocGeneratorǁgenerate_navigation__mutmut_9": xǁAPIDocGeneratorǁgenerate_navigation__mutmut_9,
    }

    def generate_navigation(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAPIDocGeneratorǁgenerate_navigation__mutmut_orig"),
            object.__getattribute__(self, "xǁAPIDocGeneratorǁgenerate_navigation__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    generate_navigation.__signature__ = _mutmut_signature(xǁAPIDocGeneratorǁgenerate_navigation__mutmut_orig)
    xǁAPIDocGeneratorǁgenerate_navigation__mutmut_orig.__name__ = "xǁAPIDocGeneratorǁgenerate_navigation"

    def xǁAPIDocGeneratorǁgenerate_index__mutmut_orig(self) -> None:
        """Generate the API index page."""
        index_path = f"{self.api_dir}/index.md"

        content = self.custom_index_content or self._generate_default_index_content()

        with mkdocs_gen_files.open(index_path, "w") as f:
            f.write(content)
        log.debug(f"Generated API index: {index_path}")

    def xǁAPIDocGeneratorǁgenerate_index__mutmut_1(self) -> None:
        """Generate the API index page."""
        index_path = None

        content = self.custom_index_content or self._generate_default_index_content()

        with mkdocs_gen_files.open(index_path, "w") as f:
            f.write(content)
        log.debug(f"Generated API index: {index_path}")

    def xǁAPIDocGeneratorǁgenerate_index__mutmut_2(self) -> None:
        """Generate the API index page."""
        index_path = f"{self.api_dir}/index.md"

        content = None

        with mkdocs_gen_files.open(index_path, "w") as f:
            f.write(content)
        log.debug(f"Generated API index: {index_path}")

    def xǁAPIDocGeneratorǁgenerate_index__mutmut_3(self) -> None:
        """Generate the API index page."""
        index_path = f"{self.api_dir}/index.md"

        content = self.custom_index_content and self._generate_default_index_content()

        with mkdocs_gen_files.open(index_path, "w") as f:
            f.write(content)
        log.debug(f"Generated API index: {index_path}")

    def xǁAPIDocGeneratorǁgenerate_index__mutmut_4(self) -> None:
        """Generate the API index page."""
        index_path = f"{self.api_dir}/index.md"

        content = self.custom_index_content or self._generate_default_index_content()

        with mkdocs_gen_files.open(None, "w") as f:
            f.write(content)
        log.debug(f"Generated API index: {index_path}")

    def xǁAPIDocGeneratorǁgenerate_index__mutmut_5(self) -> None:
        """Generate the API index page."""
        index_path = f"{self.api_dir}/index.md"

        content = self.custom_index_content or self._generate_default_index_content()

        with mkdocs_gen_files.open(index_path, None) as f:
            f.write(content)
        log.debug(f"Generated API index: {index_path}")

    def xǁAPIDocGeneratorǁgenerate_index__mutmut_6(self) -> None:
        """Generate the API index page."""
        index_path = f"{self.api_dir}/index.md"

        content = self.custom_index_content or self._generate_default_index_content()

        with mkdocs_gen_files.open("w") as f:
            f.write(content)
        log.debug(f"Generated API index: {index_path}")

    def xǁAPIDocGeneratorǁgenerate_index__mutmut_7(self) -> None:
        """Generate the API index page."""
        index_path = f"{self.api_dir}/index.md"

        content = self.custom_index_content or self._generate_default_index_content()

        with mkdocs_gen_files.open(
            index_path,
        ) as f:
            f.write(content)
        log.debug(f"Generated API index: {index_path}")

    def xǁAPIDocGeneratorǁgenerate_index__mutmut_8(self) -> None:
        """Generate the API index page."""
        index_path = f"{self.api_dir}/index.md"

        content = self.custom_index_content or self._generate_default_index_content()

        with mkdocs_gen_files.open(index_path, "XXwXX") as f:
            f.write(content)
        log.debug(f"Generated API index: {index_path}")

    def xǁAPIDocGeneratorǁgenerate_index__mutmut_9(self) -> None:
        """Generate the API index page."""
        index_path = f"{self.api_dir}/index.md"

        content = self.custom_index_content or self._generate_default_index_content()

        with mkdocs_gen_files.open(index_path, "W") as f:
            f.write(content)
        log.debug(f"Generated API index: {index_path}")

    def xǁAPIDocGeneratorǁgenerate_index__mutmut_10(self) -> None:
        """Generate the API index page."""
        index_path = f"{self.api_dir}/index.md"

        content = self.custom_index_content or self._generate_default_index_content()

        with mkdocs_gen_files.open(index_path, "w") as f:
            f.write(None)
        log.debug(f"Generated API index: {index_path}")

    def xǁAPIDocGeneratorǁgenerate_index__mutmut_11(self) -> None:
        """Generate the API index page."""
        index_path = f"{self.api_dir}/index.md"

        content = self.custom_index_content or self._generate_default_index_content()

        with mkdocs_gen_files.open(index_path, "w") as f:
            f.write(content)
        log.debug(None)

    xǁAPIDocGeneratorǁgenerate_index__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAPIDocGeneratorǁgenerate_index__mutmut_1": xǁAPIDocGeneratorǁgenerate_index__mutmut_1,
        "xǁAPIDocGeneratorǁgenerate_index__mutmut_2": xǁAPIDocGeneratorǁgenerate_index__mutmut_2,
        "xǁAPIDocGeneratorǁgenerate_index__mutmut_3": xǁAPIDocGeneratorǁgenerate_index__mutmut_3,
        "xǁAPIDocGeneratorǁgenerate_index__mutmut_4": xǁAPIDocGeneratorǁgenerate_index__mutmut_4,
        "xǁAPIDocGeneratorǁgenerate_index__mutmut_5": xǁAPIDocGeneratorǁgenerate_index__mutmut_5,
        "xǁAPIDocGeneratorǁgenerate_index__mutmut_6": xǁAPIDocGeneratorǁgenerate_index__mutmut_6,
        "xǁAPIDocGeneratorǁgenerate_index__mutmut_7": xǁAPIDocGeneratorǁgenerate_index__mutmut_7,
        "xǁAPIDocGeneratorǁgenerate_index__mutmut_8": xǁAPIDocGeneratorǁgenerate_index__mutmut_8,
        "xǁAPIDocGeneratorǁgenerate_index__mutmut_9": xǁAPIDocGeneratorǁgenerate_index__mutmut_9,
        "xǁAPIDocGeneratorǁgenerate_index__mutmut_10": xǁAPIDocGeneratorǁgenerate_index__mutmut_10,
        "xǁAPIDocGeneratorǁgenerate_index__mutmut_11": xǁAPIDocGeneratorǁgenerate_index__mutmut_11,
    }

    def generate_index(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAPIDocGeneratorǁgenerate_index__mutmut_orig"),
            object.__getattribute__(self, "xǁAPIDocGeneratorǁgenerate_index__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    generate_index.__signature__ = _mutmut_signature(xǁAPIDocGeneratorǁgenerate_index__mutmut_orig)
    xǁAPIDocGeneratorǁgenerate_index__mutmut_orig.__name__ = "xǁAPIDocGeneratorǁgenerate_index"

    def xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_orig(self) -> str:
        """Generate default index content."""
        title = self.package_prefix or "API"
        return f"""# {title} Reference

This section contains automatically generated API documentation.

## Modules

Browse the complete API documentation by module using the navigation menu.

## Usage

All modules are documented with their public APIs, including:

- Classes and their methods
- Functions and their parameters
- Type annotations and return types
- Docstrings with examples where available

"""

    def xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_1(self) -> str:
        """Generate default index content."""
        title = None
        return f"""# {title} Reference

This section contains automatically generated API documentation.

## Modules

Browse the complete API documentation by module using the navigation menu.

## Usage

All modules are documented with their public APIs, including:

- Classes and their methods
- Functions and their parameters
- Type annotations and return types
- Docstrings with examples where available

"""

    def xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_2(self) -> str:
        """Generate default index content."""
        title = self.package_prefix and "API"
        return f"""# {title} Reference

This section contains automatically generated API documentation.

## Modules

Browse the complete API documentation by module using the navigation menu.

## Usage

All modules are documented with their public APIs, including:

- Classes and their methods
- Functions and their parameters
- Type annotations and return types
- Docstrings with examples where available

"""

    def xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_3(self) -> str:
        """Generate default index content."""
        title = self.package_prefix or "XXAPIXX"
        return f"""# {title} Reference

This section contains automatically generated API documentation.

## Modules

Browse the complete API documentation by module using the navigation menu.

## Usage

All modules are documented with their public APIs, including:

- Classes and their methods
- Functions and their parameters
- Type annotations and return types
- Docstrings with examples where available

"""

    def xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_4(self) -> str:
        """Generate default index content."""
        title = self.package_prefix or "api"
        return f"""# {title} Reference

This section contains automatically generated API documentation.

## Modules

Browse the complete API documentation by module using the navigation menu.

## Usage

All modules are documented with their public APIs, including:

- Classes and their methods
- Functions and their parameters
- Type annotations and return types
- Docstrings with examples where available

"""

    xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_1": xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_1,
        "xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_2": xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_2,
        "xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_3": xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_3,
        "xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_4": xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_4,
    }

    def _generate_default_index_content(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_orig"),
            object.__getattribute__(self, "xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _generate_default_index_content.__signature__ = _mutmut_signature(
        xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_orig
    )
    xǁAPIDocGeneratorǁ_generate_default_index_content__mutmut_orig.__name__ = (
        "xǁAPIDocGeneratorǁ_generate_default_index_content"
    )

    def xǁAPIDocGeneratorǁgenerate__mutmut_orig(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_1(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(None)

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_2(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = None

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_3(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "XXprocessed_filesXX": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_4(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "PROCESSED_FILES": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_5(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 1,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_6(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "XXskipped_filesXX": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_7(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "SKIPPED_FILES": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_8(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 1,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_9(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "XXtotal_filesXX": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_10(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "TOTAL_FILES": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_11(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 1,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_12(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = None
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_13(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(None)
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_14(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob(None))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_15(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("XX*.pyXX"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_16(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.PY"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_17(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = None

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_18(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["XXtotal_filesXX"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_19(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["TOTAL_FILES"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_20(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(None):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_21(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(None):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_22(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] = 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_23(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] -= 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_24(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["XXskipped_filesXX"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_25(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["SKIPPED_FILES"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_26(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 2
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_27(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                break

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_28(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(None)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_29(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] = 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_30(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] -= 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_31(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["XXprocessed_filesXX"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_32(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["PROCESSED_FILES"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_33(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 2

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_34(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(None)

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_35(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['XXprocessed_filesXX']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_36(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['PROCESSED_FILES']} processed, {stats['skipped_files']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_37(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['XXskipped_filesXX']} skipped"
        )

        return stats

    def xǁAPIDocGeneratorǁgenerate__mutmut_38(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """
        log.info(f"🏗️ Generating API documentation from {self.src_root}")

        stats = {
            "processed_files": 0,
            "skipped_files": 0,
            "total_files": 0,
        }

        # Process all Python files
        python_files = list(self.src_root.rglob("*.py"))
        stats["total_files"] = len(python_files)

        for path in sorted(python_files):
            if self.should_skip(path):
                stats["skipped_files"] += 1
                continue

            self.process_python_file(path)
            stats["processed_files"] += 1

        # Generate navigation and index
        self.generate_navigation()
        self.generate_index()

        log.info(
            f"✅ Documentation generation complete: "
            f"{stats['processed_files']} processed, {stats['SKIPPED_FILES']} skipped"
        )

        return stats

    xǁAPIDocGeneratorǁgenerate__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAPIDocGeneratorǁgenerate__mutmut_1": xǁAPIDocGeneratorǁgenerate__mutmut_1,
        "xǁAPIDocGeneratorǁgenerate__mutmut_2": xǁAPIDocGeneratorǁgenerate__mutmut_2,
        "xǁAPIDocGeneratorǁgenerate__mutmut_3": xǁAPIDocGeneratorǁgenerate__mutmut_3,
        "xǁAPIDocGeneratorǁgenerate__mutmut_4": xǁAPIDocGeneratorǁgenerate__mutmut_4,
        "xǁAPIDocGeneratorǁgenerate__mutmut_5": xǁAPIDocGeneratorǁgenerate__mutmut_5,
        "xǁAPIDocGeneratorǁgenerate__mutmut_6": xǁAPIDocGeneratorǁgenerate__mutmut_6,
        "xǁAPIDocGeneratorǁgenerate__mutmut_7": xǁAPIDocGeneratorǁgenerate__mutmut_7,
        "xǁAPIDocGeneratorǁgenerate__mutmut_8": xǁAPIDocGeneratorǁgenerate__mutmut_8,
        "xǁAPIDocGeneratorǁgenerate__mutmut_9": xǁAPIDocGeneratorǁgenerate__mutmut_9,
        "xǁAPIDocGeneratorǁgenerate__mutmut_10": xǁAPIDocGeneratorǁgenerate__mutmut_10,
        "xǁAPIDocGeneratorǁgenerate__mutmut_11": xǁAPIDocGeneratorǁgenerate__mutmut_11,
        "xǁAPIDocGeneratorǁgenerate__mutmut_12": xǁAPIDocGeneratorǁgenerate__mutmut_12,
        "xǁAPIDocGeneratorǁgenerate__mutmut_13": xǁAPIDocGeneratorǁgenerate__mutmut_13,
        "xǁAPIDocGeneratorǁgenerate__mutmut_14": xǁAPIDocGeneratorǁgenerate__mutmut_14,
        "xǁAPIDocGeneratorǁgenerate__mutmut_15": xǁAPIDocGeneratorǁgenerate__mutmut_15,
        "xǁAPIDocGeneratorǁgenerate__mutmut_16": xǁAPIDocGeneratorǁgenerate__mutmut_16,
        "xǁAPIDocGeneratorǁgenerate__mutmut_17": xǁAPIDocGeneratorǁgenerate__mutmut_17,
        "xǁAPIDocGeneratorǁgenerate__mutmut_18": xǁAPIDocGeneratorǁgenerate__mutmut_18,
        "xǁAPIDocGeneratorǁgenerate__mutmut_19": xǁAPIDocGeneratorǁgenerate__mutmut_19,
        "xǁAPIDocGeneratorǁgenerate__mutmut_20": xǁAPIDocGeneratorǁgenerate__mutmut_20,
        "xǁAPIDocGeneratorǁgenerate__mutmut_21": xǁAPIDocGeneratorǁgenerate__mutmut_21,
        "xǁAPIDocGeneratorǁgenerate__mutmut_22": xǁAPIDocGeneratorǁgenerate__mutmut_22,
        "xǁAPIDocGeneratorǁgenerate__mutmut_23": xǁAPIDocGeneratorǁgenerate__mutmut_23,
        "xǁAPIDocGeneratorǁgenerate__mutmut_24": xǁAPIDocGeneratorǁgenerate__mutmut_24,
        "xǁAPIDocGeneratorǁgenerate__mutmut_25": xǁAPIDocGeneratorǁgenerate__mutmut_25,
        "xǁAPIDocGeneratorǁgenerate__mutmut_26": xǁAPIDocGeneratorǁgenerate__mutmut_26,
        "xǁAPIDocGeneratorǁgenerate__mutmut_27": xǁAPIDocGeneratorǁgenerate__mutmut_27,
        "xǁAPIDocGeneratorǁgenerate__mutmut_28": xǁAPIDocGeneratorǁgenerate__mutmut_28,
        "xǁAPIDocGeneratorǁgenerate__mutmut_29": xǁAPIDocGeneratorǁgenerate__mutmut_29,
        "xǁAPIDocGeneratorǁgenerate__mutmut_30": xǁAPIDocGeneratorǁgenerate__mutmut_30,
        "xǁAPIDocGeneratorǁgenerate__mutmut_31": xǁAPIDocGeneratorǁgenerate__mutmut_31,
        "xǁAPIDocGeneratorǁgenerate__mutmut_32": xǁAPIDocGeneratorǁgenerate__mutmut_32,
        "xǁAPIDocGeneratorǁgenerate__mutmut_33": xǁAPIDocGeneratorǁgenerate__mutmut_33,
        "xǁAPIDocGeneratorǁgenerate__mutmut_34": xǁAPIDocGeneratorǁgenerate__mutmut_34,
        "xǁAPIDocGeneratorǁgenerate__mutmut_35": xǁAPIDocGeneratorǁgenerate__mutmut_35,
        "xǁAPIDocGeneratorǁgenerate__mutmut_36": xǁAPIDocGeneratorǁgenerate__mutmut_36,
        "xǁAPIDocGeneratorǁgenerate__mutmut_37": xǁAPIDocGeneratorǁgenerate__mutmut_37,
        "xǁAPIDocGeneratorǁgenerate__mutmut_38": xǁAPIDocGeneratorǁgenerate__mutmut_38,
    }

    def generate(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAPIDocGeneratorǁgenerate__mutmut_orig"),
            object.__getattribute__(self, "xǁAPIDocGeneratorǁgenerate__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    generate.__signature__ = _mutmut_signature(xǁAPIDocGeneratorǁgenerate__mutmut_orig)
    xǁAPIDocGeneratorǁgenerate__mutmut_orig.__name__ = "xǁAPIDocGeneratorǁgenerate"


def x_generate_api_docs__mutmut_orig(
    src_root: str = "src",
    api_dir: str = "api/reference",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = APIDocGenerator(
        src_root=src_root,
        api_dir=api_dir,
        skip_patterns=skip_patterns,
        package_prefix=package_prefix,
        **kwargs,
    )
    return generator.generate()


def x_generate_api_docs__mutmut_1(
    src_root: str = "XXsrcXX",
    api_dir: str = "api/reference",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = APIDocGenerator(
        src_root=src_root,
        api_dir=api_dir,
        skip_patterns=skip_patterns,
        package_prefix=package_prefix,
        **kwargs,
    )
    return generator.generate()


def x_generate_api_docs__mutmut_2(
    src_root: str = "SRC",
    api_dir: str = "api/reference",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = APIDocGenerator(
        src_root=src_root,
        api_dir=api_dir,
        skip_patterns=skip_patterns,
        package_prefix=package_prefix,
        **kwargs,
    )
    return generator.generate()


def x_generate_api_docs__mutmut_3(
    src_root: str = "src",
    api_dir: str = "XXapi/referenceXX",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = APIDocGenerator(
        src_root=src_root,
        api_dir=api_dir,
        skip_patterns=skip_patterns,
        package_prefix=package_prefix,
        **kwargs,
    )
    return generator.generate()


def x_generate_api_docs__mutmut_4(
    src_root: str = "src",
    api_dir: str = "API/REFERENCE",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = APIDocGenerator(
        src_root=src_root,
        api_dir=api_dir,
        skip_patterns=skip_patterns,
        package_prefix=package_prefix,
        **kwargs,
    )
    return generator.generate()


def x_generate_api_docs__mutmut_5(
    src_root: str = "src",
    api_dir: str = "api/reference",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = None
    return generator.generate()


def x_generate_api_docs__mutmut_6(
    src_root: str = "src",
    api_dir: str = "api/reference",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = APIDocGenerator(
        src_root=None,
        api_dir=api_dir,
        skip_patterns=skip_patterns,
        package_prefix=package_prefix,
        **kwargs,
    )
    return generator.generate()


def x_generate_api_docs__mutmut_7(
    src_root: str = "src",
    api_dir: str = "api/reference",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = APIDocGenerator(
        src_root=src_root,
        api_dir=None,
        skip_patterns=skip_patterns,
        package_prefix=package_prefix,
        **kwargs,
    )
    return generator.generate()


def x_generate_api_docs__mutmut_8(
    src_root: str = "src",
    api_dir: str = "api/reference",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = APIDocGenerator(
        src_root=src_root,
        api_dir=api_dir,
        skip_patterns=None,
        package_prefix=package_prefix,
        **kwargs,
    )
    return generator.generate()


def x_generate_api_docs__mutmut_9(
    src_root: str = "src",
    api_dir: str = "api/reference",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = APIDocGenerator(
        src_root=src_root,
        api_dir=api_dir,
        skip_patterns=skip_patterns,
        package_prefix=None,
        **kwargs,
    )
    return generator.generate()


def x_generate_api_docs__mutmut_10(
    src_root: str = "src",
    api_dir: str = "api/reference",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = APIDocGenerator(
        api_dir=api_dir,
        skip_patterns=skip_patterns,
        package_prefix=package_prefix,
        **kwargs,
    )
    return generator.generate()


def x_generate_api_docs__mutmut_11(
    src_root: str = "src",
    api_dir: str = "api/reference",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = APIDocGenerator(
        src_root=src_root,
        skip_patterns=skip_patterns,
        package_prefix=package_prefix,
        **kwargs,
    )
    return generator.generate()


def x_generate_api_docs__mutmut_12(
    src_root: str = "src",
    api_dir: str = "api/reference",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = APIDocGenerator(
        src_root=src_root,
        api_dir=api_dir,
        package_prefix=package_prefix,
        **kwargs,
    )
    return generator.generate()


def x_generate_api_docs__mutmut_13(
    src_root: str = "src",
    api_dir: str = "api/reference",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = APIDocGenerator(
        src_root=src_root,
        api_dir=api_dir,
        skip_patterns=skip_patterns,
        **kwargs,
    )
    return generator.generate()


def x_generate_api_docs__mutmut_14(
    src_root: str = "src",
    api_dir: str = "api/reference",
    skip_patterns: set[str] | None = None,
    package_prefix: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Convenience function to generate API docs.

    Args:
        src_root: Root directory of source code
        api_dir: Output directory for API docs
        skip_patterns: Patterns to skip
        package_prefix: Package prefix to use
        **kwargs: Additional arguments passed to APIDocGenerator

    Returns:
        Dictionary with generation statistics
    """
    generator = APIDocGenerator(
        src_root=src_root,
        api_dir=api_dir,
        skip_patterns=skip_patterns,
        package_prefix=package_prefix,
    )
    return generator.generate()


x_generate_api_docs__mutmut_mutants: ClassVar[MutantDict] = {
    "x_generate_api_docs__mutmut_1": x_generate_api_docs__mutmut_1,
    "x_generate_api_docs__mutmut_2": x_generate_api_docs__mutmut_2,
    "x_generate_api_docs__mutmut_3": x_generate_api_docs__mutmut_3,
    "x_generate_api_docs__mutmut_4": x_generate_api_docs__mutmut_4,
    "x_generate_api_docs__mutmut_5": x_generate_api_docs__mutmut_5,
    "x_generate_api_docs__mutmut_6": x_generate_api_docs__mutmut_6,
    "x_generate_api_docs__mutmut_7": x_generate_api_docs__mutmut_7,
    "x_generate_api_docs__mutmut_8": x_generate_api_docs__mutmut_8,
    "x_generate_api_docs__mutmut_9": x_generate_api_docs__mutmut_9,
    "x_generate_api_docs__mutmut_10": x_generate_api_docs__mutmut_10,
    "x_generate_api_docs__mutmut_11": x_generate_api_docs__mutmut_11,
    "x_generate_api_docs__mutmut_12": x_generate_api_docs__mutmut_12,
    "x_generate_api_docs__mutmut_13": x_generate_api_docs__mutmut_13,
    "x_generate_api_docs__mutmut_14": x_generate_api_docs__mutmut_14,
}


def generate_api_docs(*args, **kwargs):
    result = _mutmut_trampoline(
        x_generate_api_docs__mutmut_orig, x_generate_api_docs__mutmut_mutants, args, kwargs
    )
    return result


generate_api_docs.__signature__ = _mutmut_signature(x_generate_api_docs__mutmut_orig)
x_generate_api_docs__mutmut_orig.__name__ = "x_generate_api_docs"


# <3 🧱🤝📚🪄
