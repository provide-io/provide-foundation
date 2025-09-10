# Configuration Examples

Configuration management patterns for provide-foundation applications.

## Examples

### 01_custom_config.py
Programmatic configuration using TelemetryConfig and LoggingConfig objects.

**Features:**
- Custom service names
- Log level configuration
- Output format selection (JSON, key-value)
- Configuration validation

### 02_env_variables.py
Environment variable-based configuration for runtime adjustments.

**Features:**
- Environment variable parsing
- Runtime configuration changes
- Deployment-specific settings
- No hardcoded defaults

### 03_config_management.py
Complete configuration system with file loading and environment overrides.

**Features:**
- YAML/JSON configuration files
- Environment variable overrides
- Configuration inheritance
- Async configuration loading
- Hub-based configuration management

## Configuration Patterns

### Development
Use `01_custom_config.py` patterns for development with programmatic control.

### Production
Use `02_env_variables.py` patterns for production deployments with environment-based configuration.

### Enterprise
Use `03_config_management.py` patterns for complex applications with file-based configuration and runtime updates.

## Environment Variables

Foundation supports these key environment variables:

- `PROVIDE_LOG_LEVEL` - Log level (DEBUG, INFO, WARNING, ERROR)
- `PROVIDE_SERVICE_NAME` - Service identifier
- `PROVIDE_LOG_FORMAT` - Output format (key_value, json, compact)
- `PROVIDE_ENABLE_METRICS` - Enable metrics collection
- `PROVIDE_ENABLE_TRACING` - Enable distributed tracing