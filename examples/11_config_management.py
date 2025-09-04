#!/usr/bin/env python3
# examples/11_config_management.py
"""
Configuration Management Example - Complete Configuration System

This comprehensive example demonstrates all aspects of provide.foundation's
configuration system:

1. Configuration Classes:
   - BaseConfig for simple configurations
   - EnvConfig for environment variable loading
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
    python examples/11_config_management.py
    
    # With environment variables
    DB_HOST=prod.example.com DB_PORT=5433 python examples/11_config_management.py

Expected output:
    Demonstration of various configuration loading, validation, and management patterns.

See also:
    - examples/02_custom_configuration.py for custom telemetry configuration
    - examples/08_env_variables_config.py for environment-specific patterns
"""

from __future__ import annotations

import os
from pathlib import Path
import sys
import tempfile

# Add src to path for examples
example_dir = Path(__file__).resolve().parent
project_root = example_dir.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from attrs import define

# Import using the new simplified imports
from provide.foundation import logger
from provide.foundation.config import (
    BaseConfig,
    ConfigManager,
    ConfigSchema,
    DictConfigLoader,
    EnvConfig,
    FileConfigLoader,
    MultiSourceLoader,
    SchemaField,
    env_field,
    field,
    parse_bool,
    parse_list,
)


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
class DatabaseConfig(EnvConfig):
    """Database configuration that loads from environment."""

    host: str = env_field(
        default="localhost", env_var="DB_HOST", description="Database host"
    )
    port: int = env_field(
        default=5432, env_var="DB_PORT", parser=int, description="Database port"
    )
    database: str = env_field(
        default="mydb", env_var="DB_NAME", description="Database name"
    )
    username: str = env_field(
        default="user", env_var="DB_USER", description="Database username"
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
    cors_origins: list[str] = field(
        factory=lambda: ["http://localhost:3000"], metadata={"parser": parse_list}
    )


@define
class FullConfig(EnvConfig):
    """Complete application configuration."""

    app: AppConfig = field(factory=AppConfig)
    database: DatabaseConfig = field(factory=DatabaseConfig)
    server: ServerConfig = field(factory=ServerConfig)

    features: dict[str, bool] = field(
        factory=lambda: {"new_ui": False, "analytics": True}
    )


def example_basic_usage() -> None:
    """Example: Basic configuration usage."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Configuration Usage")
    print("=" * 60)

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
    print("\n" + "=" * 60)
    print("Example 2: Environment Variable Loading")
    print("=" * 60)

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
    print("\n" + "=" * 60)
    print("Example 3: File-based Configuration")
    print("=" * 60)

    # Create temporary config files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

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

        # Note: FileConfigLoader is async, so we use asyncio.run
        import asyncio
        
        # Load from JSON
        json_loader = FileConfigLoader(json_file)
        json_config = asyncio.run(json_loader.load(AppConfig))
        logger.info("JSON config", **json_config.to_dict())

        # Load from TOML
        toml_loader = FileConfigLoader(toml_file)
        toml_config = asyncio.run(toml_loader.load(AppConfig))
        logger.info("TOML config", **toml_config.to_dict())


def example_multi_source() -> None:
    """Example: Multi-source configuration with precedence."""
    print("\n" + "=" * 60)
    print("Example 4: Multi-source Configuration")
    print("=" * 60)

    import asyncio
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create default config file
        default_file = Path(tmpdir) / "defaults.json"
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

        # Load and merge (async)
        config = asyncio.run(multi_loader.load(AppConfig))

        logger.info(
            "Multi-source config",
            app_name=config.app_name,  # From file
            port=config.port,  # From dict override
            debug=config.debug,  # From file
            version=config.version,  # From file
        )


def example_schema_validation() -> None:
    """Example: Schema definition and validation."""
    print("\n" + "=" * 60)
    print("Example 5: Schema Validation")
    print("=" * 60)

    import asyncio
    
    # Define schema
    schema = ConfigSchema(
        [
            SchemaField(
                name="app_name",
                type=str,
                required=True,
                pattern=r"^[a-z][a-z0-9-]*$",
                description="App name (lowercase, alphanumeric, hyphens)",
            ),
            SchemaField(
                name="port",
                type=int,
                required=True,
                min_value=1024,
                max_value=65535,
                description="Port number",
            ),
            SchemaField(
                name="debug", type=bool, default=False, description="Debug mode"
            ),
            SchemaField(
                name="version",
                type=str,
                required=True,
                pattern=r"^\d+\.\d+\.\d+$",
                description="Semantic version",
            ),
        ]
    )

    # Valid configuration
    valid_data = {"app_name": "my-app", "port": 3000, "debug": True, "version": "1.2.3"}

    try:
        asyncio.run(schema.validate(valid_data))
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
        asyncio.run(schema.validate(invalid_data))
    except Exception as e:
        logger.warning("Expected validation failure", error=str(e))


def example_config_manager() -> None:
    """Example: Using ConfigManager for centralized management."""
    print("\n" + "=" * 60)
    print("Example 6: Configuration Manager")
    print("=" * 60)

    import asyncio
    
    async def async_example():
        # Create manager
        manager = ConfigManager()

        # Register configurations
        app_config = AppConfig(app_name="managed-app")
        db_config = DatabaseConfig(host="localhost")

        await manager.register("app", config=app_config)
        await manager.register("database", config=db_config)

        # List configurations
        configs = await manager.list_configs()
        logger.info("Registered configs", configs=configs)

        # Get configuration
        retrieved = await manager.get("app")
        logger.info("Retrieved app config", name=retrieved.app_name)

        # Update configuration
        await manager.update("app", {"debug": True, "port": 5000})
        logger.info("Updated app config", debug=retrieved.debug, port=retrieved.port)

        # Export all configurations
        all_configs = await manager.export_all()
        logger.info("All configurations", count=len(all_configs))
    
    asyncio.run(async_example())


def main() -> None:
    """Run all examples."""
    # Setup logging
    from provide.foundation import setup_telemetry

    setup_telemetry()

    logger.info("🚀 Starting configuration examples")

    # Run examples
    example_basic_usage()
    example_env_loading()
    example_file_loading()
    example_multi_source()
    example_schema_validation()
    example_config_manager()

    logger.info("✅ Configuration examples completed")


if __name__ == "__main__":
    main()
