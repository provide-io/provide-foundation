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

