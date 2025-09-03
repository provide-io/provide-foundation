# Structured Logging

Why structured logging is fundamental to provide.foundation.

## The Problem with String Logging

Traditional logging uses formatted strings:
```python
log.info(f"User {user_id} logged in from {ip_address}")
```

## The Structured Approach

provide.foundation uses structured data:
```python
logger.info("user_login", user_id=user_id, ip_address=ip_address)
```

## Benefits

- **Searchable**: Query logs by field
- **Parseable**: Machine-readable format
- **Consistent**: Standardized field names
- **Contextual**: Automatic context propagation
