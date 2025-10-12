# Security Guide

Security best practices and cryptographic utilities.

## Secret Management

`provide.foundation` promotes the use of environment variables for managing secrets. This approach avoids hardcoding sensitive information in your codebase and makes it easy to manage secrets in different environments.

### Environment Variables

You can use the `provide.foundation.config` module to load secrets from environment variables:

```python
from provide.foundation.config import BaseConfig, field

class AppConfig(BaseConfig):
    api_key: str = field(default=None, metadata={"sensitive": True})
    db_password: str = field(default=None, metadata={"sensitive": True})

config = AppConfig.from_env()

# The values of api_key and db_password will be loaded from the
# PROVIDE_API_KEY and PROVIDE_DB_PASSWORD environment variables.
```

### File-Based Secrets

For production environments, it is recommended to use file-based secrets. You can use a configuration file to specify the path to your secrets file:

```yaml
# config.yaml
secrets_file: /path/to/secrets.yaml
```

Then, in your application, you can load the secrets file and merge it with your configuration:

```python
from provide.foundation.config import ConfigManager, FileConfigLoader

manager = ConfigManager()
loader = FileConfigLoader("config.yaml")

manager.register("app", loader=loader)
config = manager.get("app")

if config.secrets_file:
    secrets_loader = FileConfigLoader(config.secrets_file)
    manager.register("secrets", loader=secrets_loader)
    secrets = manager.get("secrets")
    config.merge(secrets)
```

## Cryptographic Operations

`provide.foundation` provides a set of utilities for common cryptographic operations.

### Hashing

You can use the `provide.foundation.crypto.hashing` module to hash data using various algorithms:

```python
from provide.foundation.crypto.hashing import hash_data

data = b"Hello, World!"
hashed_data = hash_data(data, algorithm="sha256")
```

### Signatures

You can use the `provide.foundation.crypto.signatures` module to sign and verify data:

```python
from provide.foundation.crypto.signatures import generate_signing_keypair, sign_data, verify_signature

keypair = generate_signing_keypair()
data = b"Hello, World!"

signature = sign_data(data, keypair.private_key)
is_valid = verify_signature(data, signature, keypair.public_key)
```

## Access Control

`provide.foundation` does not provide a built-in access control system, but it provides the building blocks for implementing one. You can use the `provide.foundation.errors.auth` module to raise authentication and authorization errors:

```python
from provide.foundation.errors.auth import AuthenticationError, AuthorizationError

def get_user(request):
    # ...
    if not user:
        raise AuthenticationError("User not authenticated")
    return user

def check_permissions(user, resource):
    # ...
    if not has_permission:
        raise AuthorizationError("User not authorized to access this resource")
```

## Audit Logging

You can use the structured logging system to create an audit trail of security-related events:

```python
from provide.foundation import logger

logger.info("user_login", user_id=user.id, ip_address=request.ip)
logger.info("resource_accessed", user_id=user.id, resource_id=resource.id)
```