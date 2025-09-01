# 📚 API Reference

## Error Handling

This section provides a detailed reference for the `provide.foundation` error handling system, including the exception hierarchy and resilience decorators.

### Base Exception

All exceptions in the system inherit from `FoundationError`.

::: provide.foundation.errors.exceptions.FoundationError

### Built-in Exceptions

Below are the most common built-in exception types. All inherit from `FoundationError` and can have rich context attached.

::: provide.foundation.errors.exceptions.ConfigurationError

::: provide.foundation.errors.exceptions.ValidationError

::: provide.foundation.errors.exceptions.NetworkError

::: provide.foundation.errors.exceptions.TimeoutError

::: provide.foundation.errors.exceptions.AuthenticationError

::: provide.foundation.errors.exceptions.AuthorizationError

::: provide.foundation.errors.exceptions.NotFoundError

::: provide.foundation.errors.exceptions.AlreadyExistsError

### Resilience Decorators

These decorators can be used to make your functions more resilient to errors.

::: provide.foundation.errors.decorators.retry_on_error

::: provide.foundation.errors.decorators.with_error_handling

::: provide.foundation.errors.decorators.suppress_and_log

::: provide.foundation.errors.decorators.fallback_on_error

::: provide.foundation.errors.decorators.circuit_breaker
