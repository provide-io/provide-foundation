# Secret Management

Learn how to securely handle secrets and sensitive configuration data.

## Overview

Foundation provides secure patterns for handling secrets, including file-based secrets for container platforms and environment variable protection.

## File-Based Secrets

Read secrets from files (Kubernetes-style secrets):

```python
from provide.foundation.config import BaseConfig, env_field
from attrs import define

@define
class DatabaseConfig(BaseConfig):
    host: str = env_field(env_var="DB_HOST", default="localhost")
    port: int = env_field(env_var="DB_PORT", default=5432)

    # Will read from file if value starts with "file://"
    password: str = env_field(env_var="DB_PASSWORD")

# Set environment variable to point to secret file
# export DB_PASSWORD="file:///run/secrets/db_password"

config = DatabaseConfig.from_env()
# config.password contains the contents of /run/secrets/db_password
```

## Kubernetes Secrets Example

```yaml
# kubernetes-deployment.yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: my-app
      env:
        - name: DB_PASSWORD
          value: "file:///run/secrets/db_password"
      volumeMounts:
        - name: db-secret
          mountPath: "/run/secrets"
          readOnly: true
  volumes:
    - name: db-secret
      secret:
        secretName: database-credentials
```

## Environment Variable Best Practices

**❌ Don't:**
```python
# Never hardcode secrets
API_KEY = "sk_live_abc123..."

# Never log secrets
logger.info("api_call", api_key=api_key)  # BAD!
```

**✅ Do:**
```python
# Load from environment
from provide.foundation.utils.environment import get_str

api_key = get_str("API_KEY", required=True)

# Sanitize in logs
logger.info("api_call", api_key_prefix=api_key[:7] + "...")
```

## Automatic Secret Sanitization

Foundation's log processors can automatically sanitize sensitive data:

```python
from provide.foundation import logger

# These will be automatically sanitized
logger.info(
    "user_update",
    password="secret123",      # Will be redacted
    api_token="sk_abc...",     # Will be redacted
    safe_field="public_data"   # Will be logged
)
# Output: password='***REDACTED***' api_token='***REDACTED***'
```

## Separate Secrets from Config

Keep secrets in a separate file:

```yaml
# config.yaml (version controlled)
service:
  name: my-app
  port: 8000
  database:
    host: localhost
    # Password loaded separately
```

```yaml
# secrets.yaml (NOT in version control)
database:
  password: super_secret_password
api_keys:
  stripe: sk_live_...
  sendgrid: SG....
```

```python
# Load both
config = await manager.load_yaml("config.yaml")
secrets = await manager.load_yaml("secrets.yaml")

# Merge
config["database"]["password"] = secrets["database"]["password"]
```

## AWS Secrets Manager Integration

```python
import boto3
import json

def load_aws_secret(secret_name: str) -> dict:
    """Load secret from AWS Secrets Manager."""
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Use in configuration
secrets = load_aws_secret("prod/database")

@define
class Config(BaseConfig):
    db_password: str = secrets["password"]
```

## Vault Integration

```python
import hvac

def load_vault_secret(path: str, key: str) -> str:
    """Load secret from HashiCorp Vault."""
    client = hvac.Client(url='https://vault.example.com')
    client.token = os.getenv('VAULT_TOKEN')

    secret = client.secrets.kv.v2.read_secret_version(path=path)
    return secret['data']['data'][key]
```

## Next Steps

- **[Environment Variables](env-variables.md)** - Basic configuration
- **[File-Based Config](file-config.md)** - Loading from files
- **[Production Deployment](../production/deployment.md)** - Production patterns

---

**Security Tip:** Never commit secrets to version control. Use `.gitignore` to exclude secret files.
