#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Output formatters for configuration schema display.

This module provides various formatters for displaying configuration schemas
in different output formats: human-readable tables, JSON, YAML, and Markdown."""

from __future__ import annotations

from abc import ABC, abstractmethod
import json
from typing import Any

from provide.foundation.config.discovery import ConsolidatedSchema


class SchemaFormatter(ABC):
    """Abstract base class for schema formatters."""

    @abstractmethod
    def format(
        self,
        schema: ConsolidatedSchema,
        env_only: bool = False,
        show_sensitive: bool = False,
        category: str | None = None,
    ) -> str:
        """Format schema for output.

        Args:
            schema: Consolidated schema to format
            env_only: Show only environment variables
            show_sensitive: Include sensitive fields
            category: Filter by category

        Returns:
            Formatted schema string

        """


class HumanFormatter(SchemaFormatter):
    """Human-readable table format."""

    def format(  # noqa: C901
        self,
        schema: ConsolidatedSchema,
        env_only: bool = False,
        show_sensitive: bool = False,
        category: str | None = None,
    ) -> str:
        """Format schema as human-readable tables.

        Args:
            schema: Consolidated schema to format
            env_only: Show only environment variables
            show_sensitive: Include sensitive fields
            category: Filter by category

        Returns:
            Human-readable formatted string

        """
        output_lines = []
        output_lines.append("FOUNDATION CONFIGURATION SCHEMA")
        output_lines.append("=" * 80)
        output_lines.append("")

        # Filter schemas if category specified
        schemas_to_display = schema.get_by_category(category) if category else schema.schemas

        # Group by category
        by_category: dict[str, list[tuple[str, Any]]] = {}
        for config_name, config_schema in schemas_to_display.items():
            meta = schema.metadata.get(config_name, {})
            cat = meta.get("category", "core")
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append((config_name, config_schema))

        # Display each category
        for cat in sorted(by_category.keys()):
            output_lines.append(f"{cat.upper()} CONFIGURATION")
            output_lines.append("-" * 80)
            output_lines.append("")

            for config_name, config_schema in sorted(by_category[cat]):
                output_lines.append(f"  {config_name}")
                meta = schema.metadata.get(config_name, {})
                doc = meta.get("doc", "").strip()
                if doc:
                    # Get first line of doc
                    first_line = doc.split("\n")[0].strip()
                    output_lines.append(f"    {first_line}")
                output_lines.append("")

                # Display fields
                for field in config_schema.fields:
                    # Skip if env_only and no env var
                    if env_only and not field.env_var:
                        continue

                    # Skip sensitive unless requested
                    if field.sensitive and not show_sensitive:
                        continue

                    # Format field
                    field_lines = []
                    if field.env_var:
                        field_lines.append(f"    {field.env_var}")
                        field_lines.append(f"      Field: {field.name}")
                    else:
                        field_lines.append(f"    {field.name}")

                    # Type
                    type_name = "Any"
                    if field.field_type:
                        type_name = getattr(field.field_type, "__name__", str(field.field_type))
                    field_lines.append(f"      Type: {type_name}")

                    # Required/Default
                    if field.required:
                        field_lines.append("      Required: Yes")
                    elif field.default is not None:
                        default_str = str(field.default)
                        if field.sensitive:
                            default_str = "***SENSITIVE***"
                        field_lines.append(f"      Default: {default_str}")

                    # Description
                    if field.description:
                        field_lines.append(f"      Description: {field.description}")

                    output_lines.extend(field_lines)
                    output_lines.append("")

            output_lines.append("")

        return "\n".join(output_lines)


class JSONFormatter(SchemaFormatter):
    """Machine-readable JSON format."""

    def format(  # noqa: C901
        self,
        schema: ConsolidatedSchema,
        env_only: bool = False,
        show_sensitive: bool = False,
        category: str | None = None,
    ) -> str:
        """Format schema as JSON.

        Args:
            schema: Consolidated schema to format
            env_only: Show only environment variables
            show_sensitive: Include sensitive fields
            category: Filter by category

        Returns:
            JSON formatted string

        """
        # Filter schemas if category specified
        schemas_to_display = schema.get_by_category(category) if category else schema.schemas

        output: dict[str, Any] = {
            "version": "1.0.0",
            "configs": {},
        }

        for config_name, config_schema in schemas_to_display.items():
            meta = schema.metadata.get(config_name, {})

            config_data: dict[str, Any] = {
                "module": meta.get("module", ""),
                "category": meta.get("category", "core"),
                "fields": {},
            }

            for field in config_schema.fields:
                # Skip if env_only and no env var
                if env_only and not field.env_var:
                    continue

                # Skip sensitive unless requested
                if field.sensitive and not show_sensitive:
                    continue

                # Get type name
                type_name = "Any"
                if field.field_type:
                    type_name = getattr(field.field_type, "__name__", str(field.field_type))

                # Build field data
                field_data: dict[str, Any] = {
                    "type": type_name,
                    "required": field.required,
                }

                if field.env_var:
                    field_data["env_var"] = field.env_var
                if field.default is not None:
                    if field.sensitive:
                        field_data["default"] = "***SENSITIVE***"
                    else:
                        # Handle non-serializable defaults (like Factory objects)
                        try:
                            json.dumps(field.default)
                            field_data["default"] = field.default
                        except (TypeError, ValueError):
                            field_data["default"] = str(field.default)
                if field.description:
                    field_data["description"] = field.description
                if field.sensitive:
                    field_data["sensitive"] = True

                config_data["fields"][field.name] = field_data

            output["configs"][config_name] = config_data

        return json.dumps(output, indent=2)


class YAMLFormatter(SchemaFormatter):
    """YAML format for configuration files."""

    def format(  # noqa: C901
        self,
        schema: ConsolidatedSchema,
        env_only: bool = False,
        show_sensitive: bool = False,
        category: str | None = None,
    ) -> str:
        """Format schema as YAML.

        Args:
            schema: Consolidated schema to format
            env_only: Show only environment variables
            show_sensitive: Include sensitive fields
            category: Filter by category

        Returns:
            YAML formatted string

        """
        # Filter schemas if category specified
        schemas_to_display = schema.get_by_category(category) if category else schema.schemas

        output_lines = []
        output_lines.append("# Foundation Configuration Schema")
        output_lines.append("version: '1.0.0'")
        output_lines.append("")
        output_lines.append("configs:")

        for config_name, config_schema in sorted(schemas_to_display.items()):
            meta = schema.metadata.get(config_name, {})

            output_lines.append(f"  {config_name}:")
            output_lines.append(f"    module: {meta.get('module', '')}")
            output_lines.append(f"    category: {meta.get('category', 'core')}")
            output_lines.append("    fields:")

            for field in config_schema.fields:
                # Skip if env_only and no env var
                if env_only and not field.env_var:
                    continue

                # Skip sensitive unless requested
                if field.sensitive and not show_sensitive:
                    continue

                # Get type name
                type_name = "Any"
                if field.field_type:
                    type_name = getattr(field.field_type, "__name__", str(field.field_type))

                output_lines.append(f"      {field.name}:")
                output_lines.append(f"        type: {type_name}")
                output_lines.append(f"        required: {str(field.required).lower()}")

                if field.env_var:
                    output_lines.append(f"        env_var: {field.env_var}")
                if field.default is not None:
                    if field.sensitive:
                        output_lines.append("        default: '***SENSITIVE***'")
                    else:
                        output_lines.append(f"        default: {field.default}")
                if field.description:
                    output_lines.append(f"        description: '{field.description}'")
                if field.sensitive:
                    output_lines.append("        sensitive: true")

        output_lines.append("")
        return "\n".join(output_lines)


class MarkdownFormatter(SchemaFormatter):
    """Markdown tables for documentation."""

    def format(  # noqa: C901
        self,
        schema: ConsolidatedSchema,
        env_only: bool = False,
        show_sensitive: bool = False,
        category: str | None = None,
    ) -> str:
        """Format schema as Markdown tables.

        Args:
            schema: Consolidated schema to format
            env_only: Show only environment variables
            show_sensitive: Include sensitive fields
            category: Filter by category

        Returns:
            Markdown formatted string

        """
        output_lines = []
        output_lines.append("# Foundation Configuration Schema")
        output_lines.append("")

        # Filter schemas if category specified
        schemas_to_display = schema.get_by_category(category) if category else schema.schemas

        # Group by category
        by_category: dict[str, list[tuple[str, Any]]] = {}
        for config_name, config_schema in schemas_to_display.items():
            meta = schema.metadata.get(config_name, {})
            cat = meta.get("category", "core")
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append((config_name, config_schema))

        # Display each category
        for cat in sorted(by_category.keys()):
            output_lines.append(f"## {cat.capitalize()} Configuration")
            output_lines.append("")

            for config_name, config_schema in sorted(by_category[cat]):
                output_lines.append(f"### {config_name}")
                output_lines.append("")

                meta = schema.metadata.get(config_name, {})
                doc = meta.get("doc", "").strip()
                if doc:
                    output_lines.append(doc)
                    output_lines.append("")

                # Table header
                if env_only:
                    output_lines.append("| Environment Variable | Type | Required | Default | Description |")
                    output_lines.append("|---------------------|------|----------|---------|-------------|")
                else:
                    output_lines.append("| Field | Type | Required | Default | Description |")
                    output_lines.append("|-------|------|----------|---------|-------------|")

                # Table rows
                for field in config_schema.fields:
                    # Skip if env_only and no env var
                    if env_only and not field.env_var:
                        continue

                    # Skip sensitive unless requested
                    if field.sensitive and not show_sensitive:
                        continue

                    # Get type name
                    type_name = "Any"
                    if field.field_type:
                        type_name = getattr(field.field_type, "__name__", str(field.field_type))

                    # Field name or env var
                    name = field.env_var if env_only and field.env_var else field.name

                    # Required/Default
                    required = "Yes" if field.required else "No"
                    default = ""
                    if field.default is not None:
                        default = "***SENSITIVE***" if field.sensitive else str(field.default)

                    # Description
                    desc = field.description or ""

                    output_lines.append(f"| {name} | {type_name} | {required} | {default} | {desc} |")

                output_lines.append("")

        return "\n".join(output_lines)


def get_formatter(format_name: str) -> SchemaFormatter:
    """Get formatter by name.

    Args:
        format_name: Name of formatter (human, json, yaml, markdown)

    Returns:
        Formatter instance

    Raises:
        ValueError: If format name is unknown

    """
    formatters: dict[str, SchemaFormatter] = {
        "human": HumanFormatter(),
        "json": JSONFormatter(),
        "yaml": YAMLFormatter(),
        "markdown": MarkdownFormatter(),
    }

    formatter = formatters.get(format_name)
    if not formatter:
        raise ValueError(f"Unknown format: {format_name}. Must be one of: {', '.join(formatters.keys())}")

    return formatter


# 🧱🏗️🔚
