# Testing & Common Patterns

Configuration testing strategies and common implementation patterns.

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