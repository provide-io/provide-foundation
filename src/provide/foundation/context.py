"""Unified context for configuration and CLI state management."""

import copy
import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from provide.foundation.logger import get_logger

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


@dataclass
class Context:
    """
    Unified context for configuration and CLI state.
    
    Combines configuration management with runtime state for CLI tools
    and services. Supports loading from files, environment variables,
    and programmatic updates.
    """
    
    log_level: str = "INFO"
    profile: str = "default"
    debug: bool = False
    json_output: bool = False
    config_file: Path | None = None
    log_file: Path | None = None
    
    # Private fields
    _logger: Any = field(init=False, default=None, repr=False)
    _frozen: bool = field(init=False, default=False, repr=False)
    
    def __post_init__(self) -> None:
        """Validate context after initialization."""
        self._validate()
    
    def _validate(self) -> None:
        """Validate context values."""
        if self.log_level.upper() not in VALID_LOG_LEVELS:
            raise ValueError(f"Invalid log level: {self.log_level}")
        
        # Normalize log level to uppercase
        self.log_level = self.log_level.upper()
        
        # Validate types
        if not isinstance(self.debug, bool):
            raise TypeError(f"debug must be bool, got {type(self.debug)}")
        
        if not isinstance(self.json_output, bool):
            raise TypeError(f"json_output must be bool, got {type(self.json_output)}")
    
    @classmethod
    def from_env(cls, prefix: str = "PROVIDE") -> "Context":
        """
        Create context from environment variables.
        
        Args:
            prefix: Environment variable prefix (default: PROVIDE)
            
        Returns:
            New Context instance with values from environment
        """
        kwargs = {}
        
        log_level = os.environ.get(f"{prefix}_LOG_LEVEL")
        if log_level:
            kwargs["log_level"] = log_level
        
        profile = os.environ.get(f"{prefix}_PROFILE")
        if profile:
            kwargs["profile"] = profile
        
        debug = os.environ.get(f"{prefix}_DEBUG")
        if debug:
            kwargs["debug"] = debug.lower() in ("true", "1", "yes", "on")
        
        json_output = os.environ.get(f"{prefix}_JSON_OUTPUT")
        if json_output:
            kwargs["json_output"] = json_output.lower() in ("true", "1", "yes", "on")
        
        config_file = os.environ.get(f"{prefix}_CONFIG_FILE")
        if config_file:
            kwargs["config_file"] = Path(config_file)
        
        log_file = os.environ.get(f"{prefix}_LOG_FILE")
        if log_file:
            kwargs["log_file"] = Path(log_file)
        
        return cls(**kwargs)
    
    def update_from_env(self, prefix: str = "PROVIDE") -> None:
        """
        Update context from environment variables.
        
        Args:
            prefix: Environment variable prefix (default: PROVIDE)
        """
        if self._frozen:
            raise RuntimeError("Context is frozen and cannot be modified")
        
        env_ctx = self.from_env(prefix)
        
        # Update only the values that were set in environment
        if os.environ.get(f"{prefix}_LOG_LEVEL"):
            self.log_level = env_ctx.log_level
        if os.environ.get(f"{prefix}_PROFILE"):
            self.profile = env_ctx.profile
        if os.environ.get(f"{prefix}_DEBUG"):
            self.debug = env_ctx.debug
        if os.environ.get(f"{prefix}_JSON_OUTPUT"):
            self.json_output = env_ctx.json_output
        if os.environ.get(f"{prefix}_CONFIG_FILE"):
            self.config_file = env_ctx.config_file
        if os.environ.get(f"{prefix}_LOG_FILE"):
            self.log_file = env_ctx.log_file
        
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
        if "config_file" in data and data["config_file"]:
            kwargs["config_file"] = Path(data["config_file"])
        if "log_file" in data and data["log_file"]:
            kwargs["log_file"] = Path(data["log_file"])
        
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
        if "config_file" in data and data["config_file"]:
            self.config_file = Path(data["config_file"])
        if "log_file" in data and data["log_file"]:
            self.log_file = Path(data["log_file"])
        
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
            raise ValueError(f"Unsupported config format: {path.suffix}")
        
        path.write_text(content)
    
    def merge(self, other: "Context") -> "Context":
        """
        Merge with another context, with other taking precedence.
        
        Args:
            other: Context to merge with
            
        Returns:
            New merged Context instance
        """
        merged_data = self.to_dict()
        other_data = other.to_dict()
        
        # Update with non-None values from other
        for key, value in other_data.items():
            if value is not None:
                merged_data[key] = value
        
        return Context.from_dict(merged_data)
    
    def freeze(self) -> None:
        """Freeze context to prevent further modifications."""
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
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Override setattr to check frozen state."""
        if hasattr(self, "_frozen") and self._frozen and not name.startswith("_"):
            raise RuntimeError("Context is frozen and cannot be modified")
        super().__setattr__(name, value)