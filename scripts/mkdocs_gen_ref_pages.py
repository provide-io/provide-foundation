"""Wrapper script to invoke provide.foundry API reference generation."""

from __future__ import annotations

from provide.foundry.docs import generate_reference_pages  # type: ignore[import-untyped]

# Execute the generation
generate_reference_pages()
