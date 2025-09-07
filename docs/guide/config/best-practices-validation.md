# Validation & Performance

Configuration validation strategies and performance optimization.

### 1. Lazy Loading

Don't load configuration until needed:

```python
from functools import lru_cache
from provide.foundation.config import Config

@lru_cache(maxsize=1)
def get_config() -> Config:
    """Lazily load and cache configuration."""
    return Config.from_file("config.yaml").merge_env()

# Usage
def process_request(request):
    config = get_config()  # Loaded once, cached
    # ...
```

### 2. Async Configuration for High Throughput

```python
import asyncio
from provide.foundation.config import AsyncConfig

class PerformantConfig(AsyncConfig):
    """High-performance async configuration."""
    
    async def load(self):
        """Load configuration asynchronously."""
        # Load multiple sources in parallel
        tasks = [
            self.load_file("config/base.yaml"),
            self.load_file("config/app.yaml"),
            self.load_env(),
            self.load_secrets()
        ]
        
        configs = await asyncio.gather(*tasks)
        return self.merge_all(configs)
```

### 3. Configuration Caching

```python
from provide.foundation.config import Config
import hashlib
import pickle

class CachedConfig(Config):
    """Configuration with disk caching."""
    
    @classmethod
    def from_file_cached(cls, path: str, cache_dir: str = ".cache"):
        """Load config with caching."""
        
        # Generate cache key
        with open(path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        
        cache_path = f"{cache_dir}/config_{file_hash}.pkl"
        
        # Try cache first
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        
        # Load and cache
        config = cls.from_file(path)
        os.makedirs(cache_dir, exist_ok=True)
        with open(cache_path, 'wb') as f:
            pickle.dump(config, f)
        
        return config
```

## Validation Best Practices

### 1. Fail Fast

Validate configuration at startup:

```python
from provide.foundation.config import Config, ValidationError
from provide.foundation import logger
import sys

def startup():
    """Application startup with config validation."""
    try:
        # Load configuration
        config = Config.from_file("config.yaml").merge_env()
        
        # Validate immediately
        config.validate()
        
        # Additional business logic validation
        if config.otel.enabled and not config.otel.endpoint:
            raise ValidationError("OTEL enabled but no endpoint configured")
        
        logger.info("config_loaded",
            environment=config.app.environment,
            log_level=config.logging.level
        )
        
    except ValidationError as e:
        logger.error("config_invalid", error=str(e))
        sys.exit(1)
    except Exception as e:
        logger.error("config_load_failed", error=str(e))
        sys.exit(2)
    
    return config
```

### 2. Schema Validation

Use schemas for type safety:

```python
from pydantic import BaseModel, Field, validator
from provide.foundation.config import Config

class LoggingConfig(BaseModel):
    level: str = Field(
        default="INFO",
        regex="^(TRACE|DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )
    format: str = Field(
        default="pretty",
        regex="^(pretty|json|compact|plain)$"
    )
    file: str | None = None
    
    @validator("file")
    def validate_file_path(cls, v):
        if v:
            # Ensure directory exists
            os.makedirs(os.path.dirname(v), exist_ok=True)
        return v

class AppConfig(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    version: str = Field(regex=r"^\d+\.\d+\.\d+$")
    environment: str = Field(regex="^(development|staging|production)$")

class ValidatedConfig(Config):
    logging: LoggingConfig
    app: AppConfig
    
    class Config:
        validate_assignment = True
        validate_default = True
```

### 3. Runtime Validation

Continuously validate configuration:

```python
from provide.foundation.config import Config
from provide.foundation import logger
import threading
import time

class MonitoredConfig(Config):
    """Configuration with runtime monitoring."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_monitoring()
    
    def start_monitoring(self):
        """Monitor configuration health."""
        def monitor():
            while True:
                try:
                    # Validate configuration
                    self.validate()
                    
                    # Check external dependencies
                    if self.otel.enabled:
                        self.check_otel_connectivity()
                    
                    if self.database.enabled:
                        self.check_database_connectivity()
                    
                except Exception as e:
                    logger.error("config_validation_failed",
                        error=str(e),
                        action="degraded_mode"
                    )
                
                time.sleep(60)  # Check every minute
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
```

## Testing Configuration

### 1. Test Fixtures

Create test configurations:

```python
# tests/conftest.py
import pytest
from provide.foundation.config import Config

@pytest.fixture
def test_config():
    """Test configuration fixture."""
    return Config(
        logging={
            "level": "DEBUG",
            "format": "plain",
            "no_emoji": True,
            "no_color": True
        },
        app={
            "name": "test-app",
            "version": "0.0.1",
            "environment": "test"
        }
    )

@pytest.fixture
def prod_like_config():
    """Production-like configuration for integration tests."""
    return Config.from_file("tests/fixtures/prod.yaml")
```

### 2. Configuration Mocking

```python
import unittest.mock as mock
from provide.foundation.config import Config

def test_with_mock_config():
    """Test with mocked configuration."""
    
    mock_config = mock.MagicMock(spec=Config)
    mock_config.logging.level = "INFO"
    mock_config.otel.enabled = False
    
    with mock.patch('myapp.get_config', return_value=mock_config):
        # Test your application
        result = process_data()
        assert result.success
```

### 3. Environment Variable Testing

```python
import os
import pytest
from provide.foundation.config import Config

def test_env_override(monkeypatch):
    """Test environment variable override."""
    
    # Set test environment variables
    monkeypatch.setenv("PROVIDE_LOG_LEVEL", "ERROR")
    monkeypatch.setenv("PROVIDE_LOG_FORMAT", "json")
    
    # Load config
    config = Config.from_file("config.yaml").merge_env()
    
    # Verify override
    assert config.logging.level == "ERROR"
    assert config.logging.format == "json"
```

