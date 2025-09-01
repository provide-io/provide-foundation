#!/usr/bin/env python
"""Test script showing clean import patterns for error handling."""

from provide.foundation import (
    logger,
    setup_telemetry,
    # Only essentials at top level
    FoundationError,
    error_boundary,
    with_error_handling,
    retry_on_error,
)

# Specific error types from errors module
from provide.foundation.errors import (
    ValidationError,
    NetworkError,
    ConfigurationError,
)

# Context and types when needed
from provide.foundation.errors.context import (
    ErrorContext,
    ErrorSeverity,
    ErrorCategory,
)

# Additional decorators when needed
from provide.foundation.errors.decorators import suppress_and_log

# Setup telemetry
setup_telemetry()

print("=" * 60)
print("Testing Clean Error Import Patterns")
print("=" * 60)

# Example 1: Most code just needs FoundationError
print("\n1. Basic usage with FoundationError:")
try:
    raise FoundationError(
        "Something went wrong",
        code="APP_001",
        request_id="req_123"
    )
except FoundationError as e:
    logger.error("Application error", **e.to_dict())
    print("   ✓ Basic FoundationError usage")

# Example 2: Using error_boundary (top-level import)
print("\n2. Using error_boundary (commonly used):")
with error_boundary(ValueError, reraise=False):
    int("not a number")
print("   ✓ error_boundary available at top level")

# Example 3: Common decorators at top level
print("\n3. Using common decorators:")

@with_error_handling(fallback=None, suppress=(KeyError,))
def may_fail():
    raise KeyError("oops")

@retry_on_error(NetworkError, max_attempts=2, delay=0.1)
def network_call():
    print("   Making network call...")
    return "success"

result = may_fail()
print(f"   with_error_handling result: {result}")
result = network_call()
print(f"   retry_on_error result: {result}")

# Example 4: Specific errors from errors module
print("\n4. Using specific error types:")
try:
    raise ValidationError(
        "Invalid input",
        field="email",
        value="not-an-email"
    )
except ValidationError as e:
    print(f"   Caught {type(e).__name__}: {e}")

# Example 5: Advanced - using context (imported when needed)
print("\n5. Advanced usage with ErrorContext:")
ctx = ErrorContext(
    severity=ErrorSeverity.HIGH,
    category=ErrorCategory.EXTERNAL
)
ctx.add_namespace("terraform", {"provider": "aws"})
print(f"   Created context: {ctx.to_dict()}")

# Example 6: Additional decorators (imported when needed)
print("\n6. Using additional decorators:")

@suppress_and_log(AttributeError, fallback="default")
def access_attr(obj):
    return obj.missing

result = access_attr(None)
print(f"   suppress_and_log result: {result}")

print("\n" + "=" * 60)
print("Import Pattern Summary:")
print("- Top level: FoundationError, error_boundary, with_error_handling, retry_on_error")
print("- From errors module: Specific exception types as needed")
print("- From errors.context: Context classes when needed")
print("- From errors.decorators: Additional decorators when needed")
print("=" * 60)