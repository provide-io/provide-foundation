#!/usr/bin/env python
"""Test script for the new error handling system."""

import time
from provide.foundation import (
    # Logger
    logger,
    setup_telemetry,
    # Errors
    FoundationError,
    ValidationError,
    NetworkError,
    ConfigurationError,
    ErrorContext,
    ErrorSeverity,
    ErrorCategory,
    # Handlers
    error_boundary,
    # Decorators
    with_error_handling,
    retry_on_error,
    suppress_and_log,
)

# Setup telemetry
setup_telemetry()

print("=" * 60)
print("Testing Foundation Error Handling System")
print("=" * 60)

# Test 1: Basic exception with context
print("\n1. Testing basic FoundationError with context:")
try:
    error = FoundationError(
        "Basic operation failed",
        code="TEST_001",
        user_id=123,
        operation="test_operation"
    )
    print(f"   Created error: {error}")
    print(f"   Error code: {error.code}")
    print(f"   Error context: {error.context}")
    raise error
except FoundationError as e:
    logger.error("Caught FoundationError", **e.to_dict())
    print("   ✓ Successfully caught and logged FoundationError")

# Test 2: ValidationError with field information
print("\n2. Testing ValidationError with field info:")
try:
    raise ValidationError(
        "Email format invalid",
        field="email",
        value="not-an-email",
        rule="email_format"
    )
except ValidationError as e:
    print(f"   Validation error: {e}")
    print(f"   Field: {e.context.get('validation.field')}")
    print(f"   Value: {e.context.get('validation.value')}")
    print("   ✓ ValidationError working correctly")

# Test 3: Error context with namespaces
print("\n3. Testing ErrorContext with namespaces:")
ctx = ErrorContext(severity=ErrorSeverity.HIGH, category=ErrorCategory.EXTERNAL)
ctx.add_namespace("terraform", {
    "provider": "aws",
    "resource": "aws_instance.example",
    "version": "5.0.0"
})
ctx.add_namespace("aws", {
    "region": "us-east-1",
    "account": "123456789",
    "error_code": "InvalidInstanceType"
})
ctx.add_tags("production", "critical")

print(f"   Context dict: {ctx.to_dict()}")
print("   ✓ ErrorContext namespace system working")

# Test 4: Error boundary context manager
print("\n4. Testing error_boundary context manager:")
with error_boundary(
    ValueError,
    log_errors=True,
    reraise=False,
    context={"test": "boundary"}
):
    print("   Attempting to trigger ValueError...")
    int("not a number")
print("   ✓ Error boundary suppressed the error")

# Test 5: Decorator - with_error_handling
print("\n5. Testing @with_error_handling decorator:")

@with_error_handling(
    fallback="default_value",
    suppress=(KeyError,),
    context_provider=lambda: {"decorator": "with_error_handling"}
)
def get_value(data, key):
    return data[key]

result = get_value({}, "missing_key")
print(f"   Result with missing key: {result}")
print("   ✓ Error handling decorator working")

# Test 6: Decorator - retry_on_error
print("\n6. Testing @retry_on_error decorator:")

attempt_count = 0

@retry_on_error(
    NetworkError,
    max_attempts=3,
    delay=0.1
)
def flaky_network_call():
    global attempt_count
    attempt_count += 1
    print(f"   Attempt {attempt_count}")
    if attempt_count < 3:
        raise NetworkError("Connection failed", host="api.example.com")
    return "Success!"

try:
    result = flaky_network_call()
    print(f"   Final result: {result}")
    print("   ✓ Retry decorator succeeded after retries")
except NetworkError:
    print("   ✗ All retry attempts failed")

# Test 7: Decorator - suppress_and_log
print("\n7. Testing @suppress_and_log decorator:")

@suppress_and_log(AttributeError, KeyError, fallback={})
def access_nested(obj):
    return obj.data["key"]

result = access_nested(None)
print(f"   Result when accessing None: {result}")
print("   ✓ Suppress and log decorator working")

# Test 8: Chaining errors with cause
print("\n8. Testing error chaining with cause:")
try:
    try:
        raise ValueError("Original error")
    except ValueError as original:
        raise ConfigurationError(
            "Config failed due to invalid value",
            config_key="timeout",
            cause=original
        )
except ConfigurationError as e:
    print(f"   Config error: {e}")
    print(f"   Caused by: {e.cause}")
    print("   ✓ Error chaining working")

# Test 9: Complex error with terraform context
print("\n9. Testing complex error for Terraform/pyvider:")
error = NetworkError(
    "Failed to create EC2 instance",
    service="terraform",
    endpoint="ec2.amazonaws.com",
    status_code=403,
    host="ec2.us-east-1.amazonaws.com",
    port=443
)
error.add_context("terraform.provider", "registry.terraform.io/hashicorp/aws")
error.add_context("terraform.resource_address", "module.compute.aws_instance.web[0]")
error.add_context("terraform.workspace", "production")
error.add_context("aws.region", "us-east-1")
error.add_context("aws.error_code", "UnauthorizedOperation")

print(f"   Error message: {error.message}")
print(f"   Error code: {error.code}")
print(f"   Full context: {error.to_dict()}")
print("   ✓ Complex Terraform/pyvider error structure working")

print("\n" + "=" * 60)
print("All tests completed successfully!")
print("=" * 60)