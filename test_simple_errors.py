#!/usr/bin/env python
"""Simple test of error handling system."""

# Minimal imports at top level
from provide.foundation import (
    FoundationError,
    error_boundary,
    with_error_handling,
    retry_on_error,
)

# Specific errors from the errors module
from provide.foundation.errors import ValidationError

print("Testing minimal error imports:")
print("-" * 40)

# 1. Base error works
try:
    raise FoundationError("Test error", code="TEST_001")
except FoundationError as e:
    print(f"✓ FoundationError: {e.message}, code={e.code}")

# 2. Specific error from errors module
try:
    raise ValidationError("Invalid email", field="email")
except ValidationError as e:
    print(f"✓ ValidationError: {e.message}, field={e.context.get('validation.field')}")

# 3. error_boundary works
with error_boundary(ValueError, reraise=False, log_errors=False):
    int("not a number")
print("✓ error_boundary suppressed ValueError")

# 4. Decorator works
@with_error_handling(fallback="default", suppress=(KeyError,), log_errors=False)
def test_func():
    return {"data": "value"}["missing"]

result = test_func()
print(f"✓ with_error_handling returned: {result}")

print("-" * 40)
print("All basic tests passed!")
print("\nClean import pattern:")
print("  from provide.foundation import FoundationError, error_boundary")
print("  from provide.foundation.errors import ValidationError  # when needed")