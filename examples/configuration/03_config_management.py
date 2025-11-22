#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Configuration Management Example - Complete Configuration System

This comprehensive example demonstrates all aspects of provide.foundation's
configuration system:

1. Configuration Classes:
   - BaseConfig for simple configurations
   - RuntimeConfig for environment variable loading
   - Nested configuration structures

2. Loading from Multiple Sources:
   - Environment variables with PROVIDE_ prefix
   - JSON and TOML configuration files
   - Runtime dictionary updates
   - Multi-source merging with precedence

3. Validation and Schemas:
   - Type validation with attrs
   - Custom validation methods
   - Schema definitions with constraints
   - Pattern matching for strings

4. Configuration Management:
   - ConfigManager for centralized management
   - Registration and retrieval
   - Bulk updates and exports

Usage:
    python examples/configuration/03_config_management.py

    # With environment variables
    DB_HOST=prod.example.com DB_PORT=5433 python examples/configuration/03_config_management.py

Expected output:
    Demonstration of various configuration loading, validation, and management patterns.

See Also:
    - examples/02_custom_configuration.py for custom telemetry configuration
    - examples/08_env_variables_config.py for environment-specific patterns"""

from __future__ import annotations

import os
from pathlib import Path
import sys

from attrs import define

# Add src to path for examples
example_dir = Path(__file__).resolve().parent
project_root = example_dir.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import using the new simplified imports
from provide.foundation import logger, pout
from provide.foundation.config import (
    BaseConfig,
    ConfigManager,
    ConfigSchema,
    DictConfigLoader,
    FileConfigLoader,
    MultiSourceLoader,
    RuntimeConfig,
    SchemaField,
    env_field,
    field,
    parse_bool,
)
from provide.foundation.file import temp_dir


# Example 1: Simple configuration class
@define
class AppConfig(BaseConfig):
    """Application configuration."""

    app_name: str = field(default="my-app", description="Application name")
    version: str = field(default="1.0.0", description="Application version")
    debug: bool = field(default=False, description="Debug mode")
    port: int = field(default=8080, description="Server port")

    def validate(self) -> None:
        """Custom validation logic."""
        if self.port < 1 or self.port > 65535:
            raise ValueError(f"Invalid port: {self.port}")


# Example 2: Environment-aware configuration
@define
class DatabaseConfig(RuntimeConfig):
    """Database configuration that loads from environment."""

    host: str = env_field(
        default="localhost",
        env_var="DB_HOST",
        description="Database host",
    )
    port: int = env_field(
        default=5432,
        env_var="DB_PORT",
        parser=int,
        description="Database port",
    )
    database: str = env_field(
        default="mydb",
        env_var="DB_NAME",
        description="Database name",
    )
    username: str = env_field(
        default="user",
        env_var="DB_USER",
        description="Database username",
    )
    password: str = env_field(
        default="",
        env_var="DB_PASSWORD",
        sensitive=True,
        description="Database password",
    )
    ssl_enabled: bool = env_field(
        default=False,
        env_var="DB_SSL",
        parser=parse_bool,
        description="Enable SSL connection",
    )


# Example 3: Complex nested configuration
@define
class ServerConfig(BaseConfig):
    """Server configuration with nested components."""

    host: str = field(default="0.0.0.0")
    port: int = field(default=8000)
    workers: int = field(default=4)
    timeout: int = field(default=30)
    cors_origins: list[str] | None = None

    def __attrs_post_init__(self) -> None:
        if self.cors_origins is None:
            object.__setattr__(self, "cors_origins", ["http://localhost:3000"])


@define
class FullConfig(RuntimeConfig):
    """Complete application configuration."""

    app: AppConfig | None = None
    database: DatabaseConfig | None = None
    server: ServerConfig | None = None

    features: dict[str, bool] | None = None

    def __attrs_post_init__(self) -> None:
        if self.app is None:
            object.__setattr__(self, "app", AppConfig())
        if self.database is None:
            object.__setattr__(self, "database", DatabaseConfig())
        if self.server is None:
            object.__setattr__(self, "server", ServerConfig())
        if self.features is None:
            object.__setattr__(self, "features", {"new_ui": False, "analytics": True})


def example_basic_usage() -> None:
    """Example: Basic configuration usage."""
    pout("\n" + "=" * 60)
    pout("Example 1: Basic Configuration Usage")
    pout("=" * 60)

    # Create configuration
    config = AppConfig(app_name="example-app", version="2.0.0", debug=True, port=3000)

    logger.info("Created config", config=config.to_dict())

    # Update configuration
    config.update({"port": 4000})
    logger.info("Updated port", new_port=config.port)

    # Clone configuration
    config_copy = config.clone()
    config_copy.app_name = "cloned-app"
    logger.info("Original", name=config.app_name)
    logger.info("Clone", name=config_copy.app_name)

    # Compare configurations
    diff = config.diff(config_copy)
    logger.info("Differences", diff=diff)


def example_env_loading() -> None:
    """Example: Loading from environment variables."""
    pout("\n" + "=" * 60)
    pout("Example 2: Environment Variable Loading")
    pout("=" * 60)

    # Set some environment variables
    os.environ["DB_HOST"] = "prod.db.example.com"
    os.environ["DB_PORT"] = "5433"
    os.environ["DB_USER"] = "admin"
    os.environ["DB_PASSWORD"] = "secret123"
    os.environ["DB_SSL"] = "true"

    # Load configuration from environment
    db_config = DatabaseConfig.from_env()

    logger.info(
        "Database config loaded from env",
        host=db_config.host,
        port=db_config.port,
        ssl=db_config.ssl_enabled,
        # Password is sensitive, not shown
    )

    # Export to environment format
    env_dict = db_config.to_env_dict(prefix="NEW")
    logger.info("Exported env vars", vars=list(env_dict.keys()))


def example_file_loading() -> None:
    """Example: Loading from configuration files."""
    pout("\n" + "=" * 60)
    pout("Example 3: File-based Configuration")
    pout("=" * 60)

    # Create temporary config files using Foundation utilities
    with temp_dir() as tmppath:
        # JSON config
        json_file = tmppath / "config.json"
        json_file.write_text("""{
            "app_name": "json-app",
            "version": "3.0.0",
            "debug": false,
            "port": 8080
        }""")

        # TOML config
        toml_file = tmppath / "config.toml"
        toml_file.write_text("""
app_name = "toml-app"
version = "3.1.0"
debug = true
port = 9000
""")

        # Load from JSON
        json_loader = FileConfigLoader(json_file)
        json_config = json_loader.load(AppConfig)
        logger.info("JSON config", **json_config.to_dict())

        # Load from TOML
        toml_loader = FileConfigLoader(toml_file)
        toml_config = toml_loader.load(AppConfig)
        logger.info("TOML config", **toml_config.to_dict())


def example_multi_source() -> None:
    """Example: Multi-source configuration with precedence."""
    pout("\n" + "=" * 60)
    pout("Example 4: Multi-source Configuration")
    pout("=" * 60)

    with temp_dir() as tmppath:
        # Create default config file
        default_file = tmppath / "defaults.json"
        default_file.write_text("""{
            "app_name": "default-app",
            "version": "1.0.0",
            "debug": false,
            "port": 8080
        }""")

        # Set environment variable (higher precedence)
        os.environ["APP_NAME"] = "env-app"
        os.environ["DEBUG"] = "true"

        # Create loaders
        file_loader = FileConfigLoader(default_file)
        dict_loader = DictConfigLoader({"port": 3000})  # Runtime override

        # Multi-source loader (later sources override earlier)
        multi_loader = MultiSourceLoader(file_loader, dict_loader)

        # Load and merge
        config = multi_loader.load(AppConfig)

        logger.info(
            "Multi-source config",
            app_name=config.app_name,  # From file
            port=config.port,  # From dict override
            debug=config.debug,  # From file
            version=config.version,  # From file
        )


def example_schema_validation() -> None:
    """Example: Schema definition and validation."""
    pout("\n" + "=" * 60)
    pout("Example 5: Schema Validation")
    pout("=" * 60)

    # Define schema
    schema = ConfigSchema(
        [
            SchemaField(
                name="app_name",
                required=True,
                pattern=r"^[a-z][a-z0-9-]*$",
                description="App name (lowercase, alphanumeric, hyphens)",
            ),
            SchemaField(
                name="port",
                required=True,
                min_value=1024,
                max_value=65535,
                description="Port number",
            ),
            SchemaField(
                name="debug",
                default=False,
                description="Debug mode",
            ),
            SchemaField(
                name="version",
                required=True,
                pattern=r"^\d+\.\d+\.\d+$",
                description="Semantic version",
            ),
        ],
    )

    # Valid configuration
    valid_data = {"app_name": "my-app", "port": 3000, "debug": True, "version": "1.2.3"}

    try:
        schema.validate(valid_data)
        logger.info("Valid configuration passed schema validation")
    except Exception as e:
        logger.error("Validation failed", error=str(e))

    # Invalid configuration
    invalid_data = {
        "app_name": "MyApp",  # Invalid: uppercase
        "port": 80,  # Invalid: below 1024
        "version": "1.2",  # Invalid: not semantic version
    }

    try:
        schema.validate(invalid_data)
    except Exception as e:
        logger.warning("Expected validation failure", error=str(e))


def example_config_manager() -> None:
    """Example: Using ConfigManager for centralized management."""
    pout("\n" + "=" * 60)
    pout("Example 6: Configuration Manager")
    pout("=" * 60)

    # Create manager
    manager = ConfigManager()

    # Register configurations
    app_config = AppConfig(app_name="managed-app")
    db_config = DatabaseConfig(host="localhost")

    manager.register("app", config=app_config)
    manager.register("database", config=db_config)

    # List configurations
    configs = manager.list_configs()
    logger.info("Registered configs", configs=configs)

    # Get configuration
    retrieved = manager.get("app")
    logger.info("Retrieved app config", name=retrieved.app_name)

    # Update configuration
    manager.update("app", {"debug": True, "port": 5000})
    logger.info("Updated app config", debug=retrieved.debug, port=retrieved.port)

    # Export all configurations
    all_configs = manager.export_all()
    logger.info("All configurations", count=len(all_configs))


def main() -> None:
    """Run all examples."""
    # Setup logging
    from provide.foundation import get_hub

    get_hub().initialize_foundation()

    logger.info("🚀 Starting configuration examples")

    # Run examples
    example_basic_usage()
    example_env_loading()
    example_file_loading()
    example_multi_source()
    example_schema_validation()
    example_config_manager()


if __name__ == "__main__":
    main()

# 🧱🏗️🔚
