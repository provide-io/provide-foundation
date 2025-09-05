"""
Configuration sources for registry-based component management.

This module provides configuration source implementations that integrate
with Foundation's component registry system.
"""

import os
from typing import Any, Protocol

from attrs import define, field

from provide.foundation.logger import get_logger

log = get_logger(__name__)


class ConfigSource(Protocol):
    """Protocol for configuration sources."""
    
    name: str
    
    async def load_config(self) -> dict[str, Any]:
        """Load configuration data asynchronously."""
        ...
    
    def get_value(self, key: str) -> Any:
        """Get a specific configuration value."""
        ...


@define(slots=True)
class EnvironmentConfigSource:
    """Configuration source that reads from environment variables."""
    
    name: str = field(default="environment")
    prefix: str = field(default="FOUNDATION_")
    
    async def load_config(self) -> dict[str, Any]:
        """Load all environment variables with the prefix."""
        config = {}
        
        for key, value in os.environ.items():
            if key.startswith(self.prefix):
                config_key = key[len(self.prefix):].lower()
                config[config_key] = value
        
        log.debug("Loaded environment config", count=len(config))
        return config
    
    def get_value(self, key: str) -> Any:
        """Get a specific environment variable value."""
        env_key = f"{self.prefix}{key.upper()}"
        return os.environ.get(env_key)


@define(slots=True)
class FileConfigSource:
    """Configuration source that reads from files."""
    
    name: str = field(default="file")
    file_path: str = field()
    format: str = field(default="yaml")
    
    async def load_config(self) -> dict[str, Any]:
        """Load configuration from file."""
        try:
            import aiofiles
            
            async with aiofiles.open(self.file_path, 'r') as f:
                content = await f.read()
            
            if self.format == "yaml":
                import yaml
                config = yaml.safe_load(content)
            elif self.format == "json":
                import json
                config = json.loads(content)
            else:
                raise ValueError(f"Unsupported format: {self.format}")
            
            log.debug("Loaded file config", path=self.file_path, count=len(config))
            return config or {}
            
        except Exception as e:
            log.warning("Failed to load file config", path=self.file_path, error=str(e))
            return {}
    
    def get_value(self, key: str) -> Any:
        """Get value from cached config (not implemented for file source)."""
        return None