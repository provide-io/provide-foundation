#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

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


class APIDocGenerator:
    """Generate API reference documentation for MkDocs."""

    def __init__(
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

    def should_skip(self, path: Path) -> bool:
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

    def get_module_identifier(self, parts: list[str]) -> str:
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

    def generate_module_doc(self, doc_path: Path, identifier: str, title: str) -> None:
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

    def process_python_file(self, path: Path) -> None:
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

    def generate_navigation(self) -> None:
        """Generate the navigation summary file."""
        nav_path = f"{self.api_dir}/SUMMARY.md"
        with mkdocs_gen_files.open(nav_path, "w") as nav_file:
            nav_file.writelines(self.nav.build_literate_nav())
        log.debug(f"Generated navigation file: {nav_path}")

    def generate_index(self) -> None:
        """Generate the API index page."""
        index_path = f"{self.api_dir}/index.md"

        content = self.custom_index_content or self._generate_default_index_content()

        with mkdocs_gen_files.open(index_path, "w") as f:
            f.write(content)
        log.debug(f"Generated API index: {index_path}")

    def _generate_default_index_content(self) -> str:
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

    def generate(self) -> dict[str, Any]:
        """Generate API documentation files.

        Returns:
            Dictionary with generation statistics
        """

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

        log.info(f"{stats['processed_files']} processed, {stats['skipped_files']} skipped")

        return stats


def generate_api_docs(
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


# 🧱🏗️🔚
