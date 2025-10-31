#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from attrs import define, field

"""Error context management for rich diagnostic information.

Provides structured context for errors that can be used for logging,
monitoring, and diagnostic purposes.
"""


class ErrorSeverity(str, Enum):
    """Error severity levels for prioritization and alerting."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(str, Enum):
    """Error categorization for routing and handling."""

    USER = "user"  # User error (bad input, etc.)
    SYSTEM = "system"  # System/infrastructure error
    EXTERNAL = "external"  # External service error


@define(kw_only=True, slots=True)
class ErrorContext:
    """Rich error context for diagnostics and monitoring.

    Provides a flexible container for error metadata that can be used
    by different systems (logging, monitoring, Terraform, etc.).

    Attributes:
        timestamp: When the error occurred.
        severity: Error severity level.
        category: Error category for classification.
        metadata: Namespace-based metadata storage.
        tags: Set of tags for categorization and filtering.
        trace_id: Optional trace ID for distributed tracing.
        span_id: Optional span ID for distributed tracing.

    Examples:
        >>> ctx = ErrorContext(severity=ErrorSeverity.HIGH)
        >>> ctx.add_namespace("aws", {"region": "us-east-1", "account": "123456"})
        >>> ctx.add_tag("production")

    """

    timestamp: datetime = field(factory=datetime.now)
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    category: ErrorCategory = ErrorCategory.SYSTEM
    metadata: dict[str, dict[str, Any]] = field(factory=dict)
    tags: set[str] = field(factory=set)
    trace_id: str | None = None
    span_id: str | None = None

    def add_namespace(self, namespace: str, data: dict[str, Any]) -> ErrorContext:
        """Add namespaced metadata.

        Args:
            namespace: Namespace key (e.g., 'terraform', 'aws', 'http').
            data: Metadata for this namespace.

        Returns:
            Self for method chaining.

        Examples:
            >>> ctx.add_namespace("terraform", {"provider": "aws", "version": "5.0"})
            >>> ctx.add_namespace("http", {"method": POST, "status": 500})

        """
        self.metadata[namespace] = data
        return self

    def update_namespace(self, namespace: str, data: dict[str, Any]) -> ErrorContext:
        """Update existing namespace metadata.

        Args:
            namespace: Namespace key to update.
            data: Metadata to merge into namespace.

        Returns:
            Self for method chaining.

        """
        if namespace not in self.metadata:
            self.metadata[namespace] = {}
        self.metadata[namespace].update(data)
        return self

    def get_namespace(self, namespace: str) -> dict[str, Any] | None:
        """Get metadata for a specific namespace.

        Args:
            namespace: Namespace key to retrieve.

        Returns:
            Namespace metadata or None if not found.

        """
        return self.metadata.get(namespace)

    def add_tag(self, tag: str) -> ErrorContext:
        """Add a tag for categorization.

        Args:
            tag: Tag to add.

        Returns:
            Self for method chaining.

        """
        self.tags.add(tag)
        return self

    def add_tags(self, *tags: str) -> ErrorContext:
        """Add multiple tags.

        Args:
            *tags: Tags to add.

        Returns:
            Self for method chaining.

        """
        self.tags.update(tags)
        return self

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for logging and serialization.

        Returns:
            Flattened dictionary with namespaced keys.

        Examples:
            >>> ctx.to_dict()
            {'timestamp': '2024-01-01T12:00:00', 'severity': 'high', ...}

        """
        result: dict[str, Any] = {
            "timestamp": self.timestamp.isoformat(),
            "severity": self.severity.value,
            "category": self.category.value,
        }

        # Add tracing if present
        if self.trace_id:
            result["trace_id"] = self.trace_id
        if self.span_id:
            result["span_id"] = self.span_id

        # Flatten namespaced metadata
        for namespace, data in self.metadata.items():
            for key, value in data.items():
                result[f"{namespace}.{key}"] = value

        # Add tags if present
        if self.tags:
            result["tags"] = sorted(list(self.tags))

        return result

    def to_logging_context(self) -> dict[str, Any]:
        """Convert to context suitable for structured logging.

        Returns:
            Dictionary formatted for logger context.

        """
        return self.to_dict()

    def to_terraform_diagnostic(self) -> dict[str, Any]:
        """Convert to Terraform diagnostic format.

        Returns:
            Dictionary formatted for Terraform diagnostics.

        Examples:
            >>> ctx.to_terraform_diagnostic()
            {'severity': 'error', 'summary': '...', 'detail': {...}}

        """
        # Map our severity to Terraform severity
        severity_map = {
            ErrorSeverity.LOW: "warning",
            ErrorSeverity.MEDIUM: "warning",
            ErrorSeverity.HIGH: "error",
            ErrorSeverity.CRITICAL: "error",
        }

        diagnostic: dict[str, Any] = {
            "severity": severity_map[self.severity],
            "detail": {},
        }

        # Add Terraform-specific metadata if present
        tf_meta = self.get_namespace("terraform")
        if tf_meta:
            diagnostic["detail"].update(tf_meta)

        # Add other relevant metadata
        for namespace, data in self.metadata.items():
            if namespace != "terraform":
                diagnostic["detail"][namespace] = data

        return diagnostic


def _determine_error_severity(error: Exception) -> ErrorSeverity:
    """Determine error severity based on exception type."""
    if isinstance(error, AssertionError | ValueError | TypeError):
        return ErrorSeverity.MEDIUM
    elif isinstance(error, KeyError | IndexError | AttributeError):
        return ErrorSeverity.LOW
    else:
        return ErrorSeverity.HIGH


def _determine_error_category(error: Exception) -> ErrorCategory:
    """Determine error category based on exception type."""
    # Import here to avoid circular dependency
    from provide.foundation.errors.auth import (
        AuthenticationError,
        AuthorizationError,
    )
    from provide.foundation.errors.config import ValidationError
    from provide.foundation.errors.integration import IntegrationError, NetworkError

    if isinstance(error, ValidationError | AuthenticationError | AuthorizationError):
        return ErrorCategory.USER
    elif isinstance(error, IntegrationError | NetworkError):
        return ErrorCategory.EXTERNAL
    else:
        return ErrorCategory.SYSTEM


def _group_foundation_error_context(error_context: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Group FoundationError context items by namespace."""
    grouped: dict[str, dict[str, Any]] = {}

    for key, value in error_context.items():
        if "." in key:
            namespace, subkey = key.split(".", 1)
            if namespace not in grouped:
                grouped[namespace] = {}
            grouped[namespace][subkey] = value
        else:
            # Put non-namespaced items in 'context' namespace
            if "context" not in grouped:
                grouped["context"] = {}
            grouped["context"][key] = value

    return grouped


def capture_error_context(
    error: Exception,
    severity: ErrorSeverity | None = None,
    category: ErrorCategory | None = None,
    **namespaces: dict[str, Any],
) -> ErrorContext:
    """Capture error context from an exception.

    Args:
        error: Exception to capture context from.
        severity: Optional severity override.
        category: Optional category override.
        **namespaces: Namespace data to add to context.

    Returns:
        ErrorContext with captured information.

    Examples:
        >>> try:
        ...     risky_operation()
        ... except Exception as e:
        ...     ctx = capture_error_context(
        ...         e,
        ...         severity=ErrorSeverity.HIGH,
        ...         aws={"region": "us-east-1"},
        ...         http={"status": 500}
        ...     )

    """
    # Determine severity and category if not provided
    if severity is None:
        severity = _determine_error_severity(error)
    if category is None:
        category = _determine_error_category(error)

    # Create context
    ctx = ErrorContext(severity=severity, category=category)

    # Add error details
    ctx.add_namespace(
        "error",
        {
            "type": type(error).__name__,
            "message": str(error),
        },
    )

    # Add any namespaces provided
    for namespace, data in namespaces.items():
        ctx.add_namespace(namespace, data)

    # Add context from FoundationError if applicable
    from provide.foundation.errors.base import FoundationError

    if isinstance(error, FoundationError) and error.context:
        grouped = _group_foundation_error_context(error.context)
        for namespace, data in grouped.items():
            ctx.update_namespace(namespace, data)

    return ctx


# 🧱🏗️🔚
