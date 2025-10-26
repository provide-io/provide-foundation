# How to Use Security Utilities

Foundation provides security utilities for protecting sensitive data in logs, command output, and API requests.

## Overview

The security module provides two main categories:

- **Secret Masking**: Automatically hide secrets in logs and command output
- **Data Sanitization**: Remove sensitive data from HTTP headers, URIs, and dictionaries

## Secret Masking

### Automatic Secret Detection

Foundation automatically masks common secret patterns:

```python
from provide.foundation.security import mask_secrets

# Masks API keys, tokens, passwords
text = "API_KEY=sk-1234567890abcdef DATABASE_PASSWORD=secret123"
masked = mask_secrets(text)
print(masked)
# "API_KEY=***MASKED*** DATABASE_PASSWORD=***MASKED***"
```

**Default patterns masked:**
- API keys (api_key, apikey)
- Tokens (token, auth_token, access_token)
- Passwords (password, passwd, pwd)
- Secrets (secret, client_secret)
- Credentials (credentials)
- Private keys (private_key, priv_key)

### Custom Secret Patterns

Add your own secret patterns:

```python
from provide.foundation.security import mask_secrets, DEFAULT_SECRET_PATTERNS

# Add custom pattern
custom_patterns = DEFAULT_SECRET_PATTERNS + [
    r"CUSTOM_SECRET=[^\s]+",
    r"SESSION_ID=[^\s]+"
]

text = "CUSTOM_SECRET=abc123 SESSION_ID=xyz789"
masked = mask_secrets(text, patterns=custom_patterns)
```

### Mask Command Output

Protect secrets in shell command output:

```python
from provide.foundation.security import mask_command

# Mask secrets in command strings
command = "curl -H 'Authorization: Bearer secret-token' https://api.example.com"
masked = mask_command(command)
print(masked)
# "curl -H 'Authorization: Bearer ***MASKED***' https://api.example.com"
```

### Check If Should Mask

Test if a string contains secrets:

```python
from provide.foundation.security import should_mask

if should_mask("password=secret123"):
    print("Contains secrets - mask before logging")
```

## Data Sanitization

### Sanitize HTTP Headers

Remove sensitive headers from HTTP requests/responses:

```python
from provide.foundation.security import sanitize_headers

headers = {
    "Authorization": "Bearer secret-token",
    "X-API-Key": "api-key-123",
    "Content-Type": "application/json",
    "User-Agent": "MyApp/1.0"
}

safe_headers = sanitize_headers(headers)
print(safe_headers)
# {
#     "Authorization": "***REDACTED***",
#     "X-API-Key": "***REDACTED***",
#     "Content-Type": "application/json",
#     "User-Agent": "MyApp/1.0"
# }
```

**Default sensitive headers:**
- Authorization
- X-API-Key, API-Key
- Cookie, Set-Cookie
- X-Auth-Token, X-Access-Token
- Proxy-Authorization

### Sanitize URIs

Remove sensitive query parameters:

```python
from provide.foundation.security import sanitize_uri

uri = "https://api.example.com/users?api_key=secret123&user_id=456"
safe_uri = sanitize_uri(uri)
print(safe_uri)
# "https://api.example.com/users?api_key=***REDACTED***&user_id=456"
```

**Default sensitive parameters:**
- api_key, apikey
- token, access_token, auth_token
- password, passwd
- secret, client_secret
- key

### Sanitize Dictionaries

Recursively sanitize dictionary data:

```python
from provide.foundation.security import sanitize_dict

data = {
    "user_id": "user_123",
    "api_key": "secret-key",
    "settings": {
        "password": "secret-password",
        "theme": "dark"
    }
}

safe_data = sanitize_dict(data)
print(safe_data)
# {
#     "user_id": "user_123",
#     "api_key": "***REDACTED***",
#     "settings": {
#         "password": "***REDACTED***",
#         "theme": "dark"
#     }
# }
```

## Integration with Logging

Combine with Foundation logger for secure logging:

```python
from provide.foundation import logger
from provide.foundation.security import sanitize_dict, mask_secrets

def log_api_request(url: str, headers: dict, body: dict):
    """Log API request with sanitized data."""
    from provide.foundation.security import sanitize_headers

    logger.info(
        "api_request_sent",
        url=url,
        headers=sanitize_headers(headers),
        body=sanitize_dict(body)
    )

# Usage
log_api_request(
    url="https://api.example.com/users",
    headers={"Authorization": "Bearer secret-token"},
    body={"password": "secret123", "email": "user@example.com"}
)
# Logs with sensitive data masked
```

## Configuration

### Automatic Sanitization

Foundation can automatically sanitize logs:

```python
from provide.foundation import get_hub, LoggingConfig, TelemetryConfig

config = TelemetryConfig(
    logging=LoggingConfig(
        sanitization_enabled=True,  # Enable auto-sanitization
        sanitization_sanitize_dicts=True,  # Sanitize dict values
        sanitization_mask_patterns=[  # Custom patterns
            r"CUSTOM_KEY=[^\s]+",
        ]
    )
)

hub = get_hub()
hub.initialize_foundation(config)
```

### Environment Variables

```bash
# Enable sanitization
export PROVIDE_LOG_SANITIZATION_ENABLED=true

# Sanitize dictionaries
export PROVIDE_LOG_SANITIZATION_SANITIZE_DICTS=true

# Add custom patterns (comma-separated)
export PROVIDE_LOG_SANITIZATION_MASK_PATTERNS="CUSTOM_KEY=[^\\s]+,SESSION=[^\\s]+"
```

## Best Practices

### ✅ DO: Sanitize Before Logging

```python
# ✅ Good: Sanitize sensitive data
from provide.foundation import logger
from provide.foundation.security import sanitize_dict

logger.info("user_data", data=sanitize_dict(user_dict))

# ❌ Bad: Log raw sensitive data
logger.info("user_data", data=user_dict)  # May contain passwords!
```

### ✅ DO: Mask Command Output

```python
# ✅ Good: Mask commands before logging
from provide.foundation import logger
from provide.foundation.security import mask_command

cmd = "curl -H 'X-API-Key: secret' https://api.example.com"
logger.debug("executing_command", command=mask_command(cmd))

# ❌ Bad: Log commands directly
logger.debug("executing_command", command=cmd)  # Exposes API key!
```

### ✅ DO: Use Custom Patterns for Domain-Specific Secrets

```python
# ✅ Good: Add domain-specific patterns
from provide.foundation.security import mask_secrets, DEFAULT_SECRET_PATTERNS

COMPANY_PATTERNS = DEFAULT_SECRET_PATTERNS + [
    r"INTERNAL_TOKEN=[^\s]+",
    r"VENDOR_KEY=[^\s]+"
]

text = "INTERNAL_TOKEN=abc123 VENDOR_KEY=xyz789"
safe = mask_secrets(text, patterns=COMPANY_PATTERNS)

# ❌ Bad: Rely only on default patterns
safe = mask_secrets(text)  # May miss company-specific secrets
```

### ✅ DO: Sanitize User Input

```python
# ✅ Good: Sanitize user-provided data
from provide.foundation.security import sanitize_dict

def process_user_input(data: dict):
    safe_data = sanitize_dict(data)
    store_in_database(safe_data)

# ❌ Bad: Store raw user input
def process_user_input_bad(data: dict):
    store_in_database(data)  # May contain passwords/tokens!
```

## Common Patterns

### Secure HTTP Client

```python
from provide.foundation import logger
from provide.foundation.security import sanitize_headers, sanitize_uri
import httpx

def secure_http_request(method: str, url: str, **kwargs):
    """Make HTTP request with secure logging."""
    headers = kwargs.get("headers", {})

    logger.info(
        "http_request_started",
        method=method,
        url=sanitize_uri(url),
        headers=sanitize_headers(headers)
    )

    response = httpx.request(method, url, **kwargs)

    logger.info(
        "http_request_completed",
        status_code=response.status_code,
        headers=sanitize_headers(dict(response.headers))
    )

    return response
```

### Secure Configuration Logging

```python
from provide.foundation import logger
from provide.foundation.security import sanitize_dict

def log_application_config(config: dict):
    """Log application configuration securely."""
    # Sanitize before logging
    safe_config = sanitize_dict(config)

    logger.info(
        "application_configured",
        config=safe_config
    )
```

## Next Steps

- **[Logging](../logging/basic-logging.md)**: Structured logging with security
- **[Configuration](../configuration/env-variables.md)**: Secure configuration management
- **[Process Execution](../process/subprocess.md)**: Secure command execution

---

**Tip**: Always sanitize data before logging to prevent accidental secret exposure.
