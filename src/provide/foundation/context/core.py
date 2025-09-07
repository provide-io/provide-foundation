"""Unified context for configuration and CLI state management."""

import copy
import json
import os
from pathlib import Path
from typing import Any

from attrs import define, field, fields, validators

from provide.foundation.logger import get_logger
from provide.foundation.logger.config import TelemetryConfig
from provide.foundation.utils.parsing import parse_bool

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


@define(slots=True, frozen=False)
class Context:
    """
    Unified context for configuration and CLI state.

    Combines configuration management with runtime state for CLI tools
    and services. Supports loading from files, environment variables,
    and programmatic updates.
    """

    log_level: str = field(
        default="INFO", validator=validators.in_(VALID_LOG_LEVELS), converter=str.upper
    )
    profile: str = field(default="default")
    debug: bool = field(default=False, converter=lambda x: parse_bool(x, strict=True))
    json_output: bool = field(
        default=False, converter=lambda x: parse_bool(x, strict=True)
    )
    config_file: Path | None = field(
        default=None, converter=lambda x: Path(x) if x else None
    )
    log_file: Path | None = field(
        default=None, converter=lambda x: Path(x) if x else None
    )
    log_format: str = field(default="key_value")
    no_color: bool = field(
        default=False, converter=lambda x: parse_bool(x, strict=True)
    )
    no_emoji: bool = field(
        default=False, converter=lambda x: parse_bool(x, strict=True)
    )

    # Private fields - using Factory for mutable defaults
    _logger: Any = field(init=False, factory=lambda: None, repr=False)
    _frozen: bool = field(init=False, default=False, repr=False)

    def __attrs_post_init__(self) -> None:
        """Post-initialization hook."""
        pass  # Validation is handled by attrs validators

    def _validate(self) -> None:
        """Validate context values. For attrs compatibility."""
        # Validation is handled by attrs validators automatically
        pass

    @classmethod
    def from_env(cls, prefix: str = "PROVIDE") -> "Context":
        """
        Create context from environment variables using TelemetryConfig system.

        Args:
            prefix: Environment variable prefix (default: PROVIDE)

        Returns:
            New Context instance with values from environment
        """
        # Use the main TelemetryConfig system for parsing
        telemetry_config = TelemetryConfig.from_env(strict=False)

        kwargs = {}

        # Map telemetry config values to CLI context
        kwargs["log_level"] = telemetry_config.logging.default_level
        if telemetry_config.logging.console_formatter:
            kwargs["log_format"] = telemetry_config.logging.console_formatter
        if telemetry_config.logging.log_file:
            kwargs["log_file"] = telemetry_config.logging.log_file

        # CLI-specific environment variables that don't exist in TelemetryConfig
        if profile := os.environ.get(f"{prefix}_PROFILE"):
            kwargs["profile"] = profile

        if debug := os.environ.get(f"{prefix}_DEBUG"):
            kwargs["debug"] = debug.lower() in ("true", "1", "yes", "on")

        if json_output := os.environ.get(f"{prefix}_JSON_OUTPUT"):
            kwargs["json_output"] = json_output.lower() in ("true", "1", "yes", "on")

        if config_file := os.environ.get(f"{prefix}_CONFIG_FILE"):
            kwargs["config_file"] = Path(config_file)

        # Map emoji settings to no_emoji (inverted)
        kwargs["no_emoji"] = not (
            telemetry_config.logging.logger_name_emoji_prefix_enabled
            and telemetry_config.logging.das_emoji_prefix_enabled
        )

        # Check for explicit NO_COLOR override
        if no_color := os.environ.get(f"{prefix}_NO_COLOR"):
            kwargs["no_color"] = no_color.lower() in ("true", "1", "yes", "on")

        return cls(**kwargs)

    def update_from_env(self, prefix: str = "PROVIDE") -> None:
        """
        Update context from environment variables using TelemetryConfig system.

        Args:
            prefix: Environment variable prefix (default: PROVIDE)
        """
        if self._frozen:
            raise RuntimeError("Context is frozen and cannot be modified")

        env_ctx = self.from_env(prefix)

        # Update values from TelemetryConfig (these are always updated since they're the primary source)
        self.log_level = env_ctx.log_level
        self.log_format = env_ctx.log_format
        if env_ctx.log_file:
            self.log_file = env_ctx.log_file
        self.no_emoji = env_ctx.no_emoji

        # Update CLI-specific values only if explicitly set in environment
        if os.environ.get(f"{prefix}_PROFILE"):
            self.profile = env_ctx.profile
        if os.environ.get(f"{prefix}_DEBUG"):
            self.debug = env_ctx.debug
        if os.environ.get(f"{prefix}_JSON_OUTPUT"):
            self.json_output = env_ctx.json_output
        if os.environ.get(f"{prefix}_CONFIG_FILE"):
            self.config_file = env_ctx.config_file
        if os.environ.get(f"{prefix}_NO_COLOR"):
            self.no_color = env_ctx.no_color

        self._validate()

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
    def from_dict(cls, data: dict[str, Any]) -> "Context":
        """
        Create context from dictionary.

        Args:
            data: Dictionary with context values

        Returns:
            New Context instance
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
        if self._frozen:
            raise RuntimeError("Context is frozen and cannot be modified")

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

    def merge(self, other: "Context", override_defaults: bool = False) -> "Context":
        """
        Merge with another context, with other taking precedence.

        Args:
            other: Context to merge with
            override_defaults: If False, only override if other's value differs from its class default

        Returns:
            New merged Context instance
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
            for f in fields(Context):
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

        return Context.from_dict(merged_data)

    def freeze(self) -> None:
        """Freeze context to prevent further modifications."""
        # Note: With attrs, we can't dynamically freeze an instance
        # This is kept for API compatibility but does nothing
        self._frozen = True

    def copy(self) -> "Context":
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
