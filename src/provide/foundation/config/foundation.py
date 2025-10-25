# provide/foundation/config/foundation.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from attrs import define

from provide.foundation.config.base import field
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.process.defaults import DEFAULT_PROCESS_TITLE

"""FoundationConfig - Top-level configuration for Foundation applications.

This configuration class serves as the primary entry point for configuring
Foundation-based applications. It composes subsystem-specific configurations
(telemetry, logging, tracing) with application-level settings (process title, etc.).

Design Pattern:
    Composition over inheritance - FoundationConfig contains TelemetryConfig
    rather than inheriting from it, providing clear separation between
    telemetry-specific and application-level concerns.

Usage:
    # Load from environment variables
    config = FoundationConfig.from_env()

    # Initialize Foundation with the config
    from provide.foundation.hub import get_hub
    hub = get_hub()
    hub.initialize_foundation(config=config)

    # Or use environment variable directly
    # PROVIDE_PROCESS_TITLE="my-app" python app.py

Environment Variables:
    PROVIDE_PROCESS_TITLE: Process title to set on initialization
    All TelemetryConfig environment variables (OTEL_*, PROVIDE_*)
"""


@define(slots=True, repr=False)
class FoundationConfig(RuntimeConfig):
    """Top-level Foundation application configuration.

    This configuration class composes all Foundation subsystem configurations
    and provides application-level settings like process title management.

    Attributes:
        telemetry: Telemetry configuration (logging, tracing, metrics)
        process_title: Process title to set on initialization (optional)

    Example:
        >>> config = FoundationConfig.from_env()
        >>> config.process_title
        'my-application'
        >>> config.telemetry.service_name
        'my-service'
    """

    telemetry: TelemetryConfig = field(
        factory=lambda: TelemetryConfig.from_env(),
        description="Telemetry configuration (logging, tracing, metrics)",
    )

    process_title: str | None = field(
        default=DEFAULT_PROCESS_TITLE,
        env_var="PROVIDE_PROCESS_TITLE",
        description="Process title to set on initialization",
    )

    @classmethod
    def from_env(
        cls,
        prefix: str = "",
        delimiter: str = "_",
        case_sensitive: bool = False,
    ) -> FoundationConfig:
        """Load configuration from environment variables.

        Loads both application-level settings and nested telemetry configuration
        from environment variables.

        Args:
            prefix: Prefix for environment variables (default: "")
            delimiter: Delimiter for nested keys (default: "_")
            case_sensitive: Whether environment variable names are case-sensitive

        Returns:
            Fully configured FoundationConfig instance

        Example:
            >>> import os
            >>> os.environ["PROVIDE_PROCESS_TITLE"] = "my-app"
            >>> os.environ["PROVIDE_SERVICE_NAME"] = "my-service"
            >>> config = FoundationConfig.from_env()
            >>> config.process_title
            'my-app'
            >>> config.telemetry.service_name
            'my-service'
        """
        # Load telemetry config first
        telemetry_config = TelemetryConfig.from_env(
            prefix=prefix,
            delimiter=delimiter,
            case_sensitive=case_sensitive,
        )

        # Load foundation-level config (process_title, etc.)
        # Use parent from_env for the foundation-level fields
        config_dict = cls._load_env_vars(prefix=prefix, delimiter=delimiter, case_sensitive=case_sensitive)

        # Create FoundationConfig with both
        return cls(
            telemetry=telemetry_config,
            process_title=config_dict.get("process_title"),
        )

    @classmethod
    def _load_env_vars(
        cls,
        prefix: str = "",
        delimiter: str = "_",
        case_sensitive: bool = False,
    ) -> dict[str, str | None]:
        """Internal helper to load environment variables for foundation-level fields."""
        import os

        result = {}

        # Load process_title from PROVIDE_PROCESS_TITLE
        process_title_key = f"{prefix}PROVIDE_PROCESS_TITLE" if prefix else "PROVIDE_PROCESS_TITLE"
        result["process_title"] = os.getenv(process_title_key)

        return result


__all__ = [
    "FoundationConfig",
]


# <3 🧱🤝⚙️🪄
