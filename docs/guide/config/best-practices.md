# Configuration Best Practices

Production-ready configuration strategies for provide.foundation applications.

## Environment-Specific Configuration

### Development Environment

Optimize for developer experience and debugging:

```bash
# .env.development
PROVIDE_LOG_LEVEL=DEBUG
PROVIDE_LOG_FORMAT=pretty
PROVIDE_NO_EMOJI=false
PROVIDE_NO_COLOR=false
PROVIDE_LOG_CALLER_INFO=true
PROVIDE_EMOJI_SETS=true
PROVIDE_LAYER_EMOJI=true
PROVIDE_CONFIG_RELOAD=true
PROVIDE_VERBOSE=2
```

```yaml
# config.development.yaml
logging:
  level: DEBUG
  format: pretty
  no_emoji: false
  caller_info: true
  
emoji_sets:
  enabled: true
  emoji: true
  validation: true
  
debug:
  show_config: true
  trace_processors: true
  profile: false
```

### Staging Environment

Balance between debugging and production-like behavior:

```bash
# .env.staging
PROVIDE_LOG_LEVEL=INFO
PROVIDE_LOG_FORMAT=json
PROVIDE_NO_EMOJI=true
PROVIDE_LOG_FILE=/var/log/app.staging.log
PROVIDE_OTEL_ENDPOINT=http://staging-otel:4317
PROVIDE_OTEL_SAMPLE_RATE=0.5
PROVIDE_APP_ENVIRONMENT=staging
```

```yaml
# config.staging.yaml
logging:
  level: INFO
  format: json
  no_emoji: true
  file: /var/log/app.staging.log
  
otel:
  endpoint: http://staging-otel:4317
  sample_rate: 0.5
  traces: true
  metrics: true
  
app:
  environment: staging
  debug: false
```

### Production Environment

Optimize for performance, reliability, and observability:

```bash
# .env.production
PROVIDE_LOG_LEVEL=WARNING
PROVIDE_LOG_FORMAT=json
PROVIDE_NO_EMOJI=true
PROVIDE_NO_COLOR=true
PROVIDE_LOG_FILE=/var/log/app.log
PROVIDE_ASYNC_LOGGING=true
PROVIDE_BUFFER_SIZE=10000
PROVIDE_OTEL_ENDPOINT=https://prod-otel:4317
PROVIDE_OTEL_SAMPLE_RATE=0.1
PROVIDE_OTEL_COMPRESSION=gzip
PROVIDE_APP_ENVIRONMENT=production
PROVIDE_DROP_ON_OVERFLOW=true
```

```yaml
# config.production.yaml
logging:
  level: WARNING
  format: json
  no_emoji: true
  no_color: true
  file: /var/log/app.log
  
performance:
  async_logging: true
  buffer_size: 10000
  batch_size: 500
  drop_on_overflow: true
  
otel:
  endpoint: https://prod-otel:4317
  sample_rate: 0.1
  compression: gzip
  timeout_ms: 5000
  
app:
  environment: production
  debug: false
```

## Configuration Hierarchy

### 1. Use Multiple Layers

Structure configuration in layers for flexibility:

```
config/
├── defaults.yaml      # Built-in defaults (don't modify)
├── base.yaml         # Company-wide standards
├── app.yaml          # Application-specific
├── local.yaml        # Local overrides (gitignored)
└── secrets.yaml      # Secret references (gitignored)
```

```python
from provide.foundation.config import Config

def load_config() -> Config:
    """Load configuration with proper hierarchy."""
    # Start with base
    config = Config.from_file("config/base.yaml")
    
    # Add app-specific
    if os.path.exists("config/app.yaml"):
        app_config = Config.from_file("config/app.yaml")
        config = config.merge(app_config)
    
    # Add local overrides
    if os.path.exists("config/local.yaml"):
        local_config = Config.from_file("config/local.yaml")
        config = config.merge(local_config)
    
    # Environment variables override everything
    config = config.merge_env()
    
    return config
```

### 2. Profile-Based Loading

Use profiles for clean environment separation:

```yaml
# config.yaml
default:
  logging:
    timestamp: true
    timestamp_format: ISO8601
  app:
    name: my-service

profiles:
  development:
    extends: default
    logging:
      level: DEBUG
      format: pretty
      no_emoji: false
    debug:
      enabled: true
      profiling: false

  production:
    extends: default
    logging:
      level: WARNING
      format: json
      no_emoji: true
      file: /var/log/app.log
    performance:
      async_logging: true
      buffer_size: 10000
    otel:
      endpoint: ${OTEL_ENDPOINT}
      sample_rate: 0.1
```

## Security Best Practices

### 1. Never Commit Secrets

```yaml
# ❌ BAD: config.yaml
database:
  password: "super-secret-password"
api:
  key: "sk-1234567890abcdef"

# ✅ GOOD: config.yaml
database:
  password: ${DB_PASSWORD}        # From environment
api:
  key: !vault secret/api/key     # From secret manager
```

### 2. Use Secret Management Systems

```python
from provide.foundation.config import Config
from provide.foundation.secrets import (
    VaultProvider,
    AWSSecretsProvider,
    AzureKeyVaultProvider
)

def load_secure_config() -> Config:
    """Load config with secret resolution."""
    
    # Choose provider based on environment
    if os.getenv("VAULT_ADDR"):
        secret_provider = VaultProvider()
    elif os.getenv("AWS_REGION"):
        secret_provider = AWSSecretsProvider()
    elif os.getenv("AZURE_TENANT_ID"):
        secret_provider = AzureKeyVaultProvider()
    else:
        # Development: use environment variables
        secret_provider = EnvSecretProvider()
    
    # Load with secret resolution
    config = Config.from_file(
        "config.yaml",
        secret_resolver=secret_provider
    )
    
    return config
```

### 3. Validate Sensitive Data

```python
from provide.foundation.config import Config, SensitiveField

class SecureConfig(Config):
    """Configuration with sensitive field protection."""
    
    database_password = SensitiveField()
    api_key = SensitiveField()
    oauth_secret = SensitiveField()
    
    def validate(self):
        """Ensure sensitive fields are properly set."""
        super().validate()
        
        # Check sensitive fields aren't exposed
        for field in self.sensitive_fields():
            value = getattr(self, field)
            if value and value.startswith("sk-"):
                raise ValueError(f"Sensitive field {field} appears to contain actual secret")
```

### 4. Audit Configuration Access

```python
from provide.foundation import logger
from provide.foundation.config import Config

class AuditedConfig(Config):
    """Configuration with audit logging."""
    
    def __getattribute__(self, name):
        value = super().__getattribute__(name)
        
        # Log access to sensitive fields
        if name in ["database_password", "api_key"]:
            logger.info("config_access",
                field=name,
                accessor=get_caller_info(),
                timestamp=time.time()
            )
        
        return value
```

## Performance Optimization

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

## Documentation Standards

### 1. Document All Settings

```yaml
# config.yaml - Well-documented configuration

# Logging configuration
logging:
  # Minimum log level to output
  # Options: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
  # Default: INFO
  # Production recommendation: WARNING
  level: INFO
  
  # Output format for logs
  # Options:
  #   - pretty: Human-readable with colors and emoji (development)
  #   - json: Structured JSON for log aggregation (production)
  #   - compact: Single-line human-readable (CI/CD)
  #   - plain: No formatting (debugging)
  # Default: pretty
  format: pretty
  
  # Path to log file (optional)
  # If not specified, logs only go to stderr
  # Ensure the directory exists and is writable
  # Example: /var/log/myapp/app.log
  file: null
```

### 2. Provide Examples

Create example configurations:

```bash
# config.example.yaml
# Example configuration file
# Copy to config.yaml and modify as needed

logging:
  level: INFO          # Change to DEBUG for development
  format: pretty       # Change to json for production

otel:
  endpoint: ${OTEL_ENDPOINT}  # Set via environment variable
  service_name: my-service
  traces: true
  metrics: true

app:
  name: my-service
  version: 1.0.0
  environment: development  # Set to production when deploying
```

### 3. Migration Guides

Document migration from other systems:

```markdown
# Migration from Python logging

## Step 1: Map log levels
- logging.DEBUG → PROVIDE_LOG_LEVEL=DEBUG
- logging.INFO → PROVIDE_LOG_LEVEL=INFO
- logging.WARNING → PROVIDE_LOG_LEVEL=WARNING
- logging.ERROR → PROVIDE_LOG_LEVEL=ERROR

## Step 2: Update configuration files
Old (logging.conf):
```ini
[loggers]
keys=root

[logger_root]
level=INFO
```

New (config.yaml):
```yaml
logging:
  level: INFO
```
```

## Common Patterns

### 1. Feature Flags

```yaml
# config.yaml
features:
  new_payment_flow: false
  enhanced_monitoring: true
  beta_features: false
  
  # Gradual rollout
  rollout:
    new_ui:
      enabled: true
      percentage: 10  # 10% of users
      whitelist:
        - user123
        - user456
```

```python
from provide.foundation.config import Config

def should_use_feature(config: Config, feature: str, user_id: str) -> bool:
    """Check if feature is enabled for user."""
    
    feature_config = config.features.rollout.get(feature)
    if not feature_config or not feature_config.enabled:
        return False
    
    # Check whitelist
    if user_id in feature_config.whitelist:
        return True
    
    # Check percentage rollout
    if hash(user_id) % 100 < feature_config.percentage:
        return True
    
    return False
```

### 2. Multi-Tenant Configuration

```yaml
# config.yaml
tenants:
  default:
    logging:
      level: INFO
    rate_limit: 1000
    
  premium:
    logging:
      level: DEBUG
    rate_limit: 10000
    features:
      - advanced_analytics
      - priority_support
    
  enterprise:
    logging:
      level: TRACE
    rate_limit: -1  # Unlimited
    features:
      - all
```

### 3. Circuit Breaker Configuration

```yaml
# config.yaml
resilience:
  circuit_breaker:
    failure_threshold: 5
    recovery_timeout: 60
    half_open_requests: 3
    
  retry:
    max_attempts: 3
    backoff_multiplier: 2
    max_backoff: 60
    
  timeout:
    default: 30
    database: 10
    api_calls: 5
```

## Monitoring Configuration

### 1. Configuration Metrics

```python
from provide.foundation.config import Config
from provide.foundation.metrics import gauge, counter

# Track configuration values
config_gauge = gauge("config_values")
config_changes = counter("config_changes")

class MetricizedConfig(Config):
    """Configuration with metrics."""
    
    def __setattr__(self, name, value):
        old_value = getattr(self, name, None)
        super().__setattr__(name, value)
        
        # Track changes
        if old_value != value:
            config_changes.inc(labels={"field": name})
            
        # Update gauges for numeric values
        if isinstance(value, (int, float)):
            config_gauge.set(value, labels={"field": name})
```

### 2. Configuration Health Checks

```python
from provide.foundation.config import Config
from provide.foundation.health import HealthCheck

class ConfigHealthCheck(HealthCheck):
    """Health check for configuration."""
    
    def check(self, config: Config) -> dict:
        """Check configuration health."""
        
        issues = []
        
        # Check required fields
        if not config.app.name:
            issues.append("Missing app.name")
            
        # Check value ranges
        if config.logging.level not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            issues.append(f"Invalid log level: {config.logging.level}")
            
        # Check external dependencies
        if config.otel.enabled and not self.check_otel_connectivity(config.otel.endpoint):
            issues.append("OTEL endpoint unreachable")
        
        return {
            "healthy": len(issues) == 0,
            "issues": issues,
            "config_version": config.version
        }
```

## Next Steps

- 🔧 [Runtime Configuration](runtime.md) - Dynamic configuration updates
- 🌍 [Environment Variables](environment.md) - Complete variable reference
- 📁 [Configuration Files](files.md) - File formats and loading
- 🏠 [Back to Config Guide](index.md)