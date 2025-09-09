"""Unified context for configuration and CLI state management."""

import copy
import json
import os
from pathlib import Path
from typing import Any

from attrs import define, field, fields, validators

from provide.foundation.config.env import RuntimeConfig
from provide.foundation.config.base import field as config_field, ConfigSource
from provide.foundation.config.converters import parse_bool_strict
from provide.foundation.logger import get_logger
from provide.foundation.logger.config import TelemetryConfig

try:
    import tomli as tomllib
except ImportError:
    try:
        import tomllib
    except ImportError:
        tomllib = None

try:
    import yaml
except ImportError:
    yaml = None


VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


@define(slots=True, repr=False)
class CLIContext(RuntimeConfig):
    """
    Runtime context for CLI execution and state management.

    Manages CLI-specific settings, output formatting, and runtime state
    during command execution. Supports loading from files, environment variables,
    and programmatic updates during CLI command execution.
    """

    log_level: str = config_field(
        default="INFO",
        env_var="PROVIDE_LOG_LEVEL",
        converter=str.upper,
        validator=validators.in_(VALID_LOG_LEVELS),
        description="Logging level for CLI output"
    )
    profile: str = config_field(
        default="default",
        env_var="PROVIDE_PROFILE",
        description="Configuration profile to use"
    )
    debug: bool = config_field(
        default=False,
        env_var="PROVIDE_DEBUG",
        converter=parse_bool_strict,
        description="Enable debug mode"
    )
    json_output: bool = config_field(
        default=False,
        env_var="PROVIDE_JSON_OUTPUT",
        converter=parse_bool_strict,
        description="Output in JSON format"
    )
    config_file: Path | None = config_field(
        default=None,
        env_var="PROVIDE_CONFIG_FILE",
        converter=lambda x: Path(x) if x else None,
        description="Path to configuration file"
    )
    log_file: Path | None = config_field(
        default=None,
        env_var="PROVIDE_LOG_FILE",
        converter=lambda x: Path(x) if x else None,
        description="Path to log file"
    )
    log_format: str = config_field(
        default="key_value",
        env_var="PROVIDE_LOG_FORMAT",
        description="Log output format (key_value or json)"
    )
    no_color: bool = config_field(
        default=False,
        env_var="NO_COLOR",
        converter=parse_bool_strict,
        description="Disable colored output"
    )
    no_emoji: bool = config_field(
        default=False,
        env_var="PROVIDE_NO_EMOJI",
        converter=parse_bool_strict,
        description="Disable emoji in output"
    )

    # Private fields - using Factory for mutable defaults
    _logger: Any = field(init=False, factory=lambda: None, repr=False)
    _frozen: bool = field(init=False, default=False, repr=False)

    def __attrs_post_init__(self) -> None:
        """Post-initialization hook."""
        pass  # Validation is handled by attrs validators

    def update_from_env(self, prefix: str = "PROVIDE") -> None:
        """
        Update context from environment variables.

        Args:
            prefix: Environment variable prefix (default: PROVIDE)
        """
        if self._frozen:
            raise RuntimeError("Context is frozen and cannot be modified")

        # Create default instance and environment instance
        default_ctx = self.__class__()  # All defaults
        env_ctx = self.from_env(prefix=prefix)  # Environment + defaults
        
        # Only update fields where environment differs from default
        for attr in fields(self.__class__):
            if not attr.name.startswith("_"):  # Skip private fields
                default_value = getattr(default_ctx, attr.name)
                env_value = getattr(env_ctx, attr.name)
                
                # If environment value differs from default, it came from env
                if env_value != default_value:
                    setattr(self, attr.name, env_value)

    def to_dict(self) -> dict[str, Any]:
        """Convert context to dictionary."""
        return {
            "log_level": self.log_level,
            "profile": self.profile,
            "debug": self.debug,
            "json_output": self.json_output,
            "config_file": str(self.config_file) if self.config_file else None,
            "log_file": str(self.log_file) if self.log_file else None,
            "log_format": self.log_format,
            "no_color": self.no_color,
            "no_emoji": self.no_emoji,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], source: ConfigSource = ConfigSource.RUNTIME) -> "CLIContext":
        """
        Create context from dictionary.

        Args:
            data: Dictionary with context values
            source: Source of the configuration data

        Returns:
            New CLIContext instance
        """
        kwargs = {}

        if "log_level" in data:
            kwargs["log_level"] = data["log_level"]
        if "profile" in data:
            kwargs["profile"] = data["profile"]
        if "debug" in data:
            kwargs["debug"] = data["debug"]
        if "json_output" in data:
            kwargs["json_output"] = data["json_output"]
        if data.get("config_file"):
            kwargs["config_file"] = Path(data["config_file"])
        if data.get("log_file"):
            kwargs["log_file"] = Path(data["log_file"])
        if "log_format" in data:
            kwargs["log_format"] = data["log_format"]
        if "no_color" in data:
            kwargs["no_color"] = data["no_color"]
        if "no_emoji" in data:
            kwargs["no_emoji"] = data["no_emoji"]

        return cls(**kwargs)

    def load_config(self, path: str | Path) -> None:
        """
        Load configuration from file.

        Supports TOML, JSON, and YAML formats based on file extension.

        Args:
            path: Path to configuration file
        """
        # CLIContext is not frozen, so we can modify it
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        content = path.read_text()

        if path.suffix in (".toml", ".tml"):
            if tomllib is None:
                raise ImportError("tomli/tomllib required for TOML support")
            data = tomllib.loads(content)
        elif path.suffix == ".json":
            data = json.loads(content)
        elif path.suffix in (".yaml", ".yml"):
            if yaml is None:
                raise ImportError("PyYAML required for YAML support")
            data = yaml.safe_load(content)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")

        # Update context from loaded data
        if "log_level" in data:
            self.log_level = data["log_level"]
        if "profile" in data:
            self.profile = data["profile"]
        if "debug" in data:
            self.debug = data["debug"]
        if "json_output" in data:
            self.json_output = data["json_output"]
        if data.get("config_file"):
            self.config_file = Path(data["config_file"])
        if data.get("log_file"):
            self.log_file = Path(data["log_file"])
        if "log_format" in data:
            self.log_format = data["log_format"]
        if "no_color" in data:
            self.no_color = data["no_color"]
        if "no_emoji" in data:
            self.no_emoji = data["no_emoji"]

        self._validate()

    def save_config(self, path: str | Path) -> None:
        """
        Save configuration to file.

        Format is determined by file extension.

        Args:
            path: Path to save configuration
        """
        path = Path(path)
        data = self.to_dict()

        # Remove None values for cleaner output
        data = {k: v for k, v in data.items() if v is not None}

        if path.suffix in (".toml", ".tml"):
            try:
                import tomli_w

                content = tomli_w.dumps(data)
            except ImportError:
                raise ImportError("tomli_w required for TOML writing")
        elif path.suffix == ".json":
            content = json.dumps(data, indent=2)
        elif path.suffix in (".yaml", ".yml"):
            if yaml is None:
                raise ImportError("PyYAML required for YAML support")
            content = yaml.safe_dump(data, default_flow_style=False)
        else:
            if not path.suffix:
                raise ValueError(
                    f"Unsupported config format: no file extension for {path}"
                )
            else:
                raise ValueError(f"Unsupported config format: {path.suffix}")

        path.write_text(content)

    def merge(self, other: "CLIContext", override_defaults: bool = False) -> "CLIContext":
        """
        Merge with another context, with other taking precedence.

        Args:
            other: CLIContext to merge with
            override_defaults: If False, only override if other's value differs from its class default

        Returns:
            New merged CLIContext instance
        """
        merged_data = self.to_dict()
        other_data = other.to_dict()

        if override_defaults:
            # Update with non-None values from other
            for key, value in other_data.items():
                if value is not None:
                    merged_data[key] = value
        else:
            # Only override if the value differs from the default
            from attrs import Factory

            defaults = {}
            for f in fields(CLIContext):
                if not f.name.startswith("_"):  # Skip private fields
                    if isinstance(f.default, Factory):
                        defaults[f.name] = f.default.factory()
                    elif f.default is not None:
                        defaults[f.name] = f.default

            for key, value in other_data.items():
                if value is not None:
                    # Check if this is different from the default
                    if key in defaults and value == defaults[key]:
                        # Skip default values
                        continue
                    merged_data[key] = value

        return CLIContext.from_dict(merged_data)

    def freeze(self) -> None:
        """Freeze context to prevent further modifications."""
        # Note: With attrs, we can't dynamically freeze an instance
        # This is kept for API compatibility but does nothing
        self._frozen = True

    def copy(self) -> "CLIContext":
        """Create a deep copy of the context."""
        return copy.deepcopy(self)

    @property
    def logger(self) -> Any:
        """Get or create a logger for this context."""
        if self._logger is None:
            self._logger = get_logger("context").bind(
                log_level=self.log_level,
                profile=self.profile,
            )
        return self._logger

    def _validate(self) -> None:
        """Validate context values. For attrs compatibility."""
        # Validation is handled by attrs validators automatically
        pass
