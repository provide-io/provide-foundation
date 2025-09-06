# Testing

Comprehensive testing strategies for applications using provide.foundation.

## Overview

Testing applications with provide.foundation requires special consideration for logging, configuration, and component management. This section covers:

- **Basic Testing** - Logger testing and log assertion patterns
- **Advanced Testing** - Configuration, context, CLI, and async testing
- **Performance Testing** - Testing performance and error handling

## Testing Topics

### [Basic Testing](testing-basics.md)

Fundamental testing patterns:
- Logger testing and mocking
- Log output verification
- Test isolation and cleanup
- Basic assertion patterns

### [Advanced Testing](testing-advanced.md)

Comprehensive testing strategies:
- Configuration testing patterns
- Context testing and isolation
- CLI command testing
- Async testing patterns
- Integration testing

### [Performance Testing](testing-performance.md)

Performance and reliability testing:
- Performance testing strategies
- Error handling testing
- Load testing with logging
- Test optimization techniques

## Quick Reference

| Testing Area | Key Concerns | Tools |
|-------------|-------------|--------|
| [Basic](testing-basics.md) | Logger mocking, output verification | pytest, unittest |
| [Advanced](testing-advanced.md) | Integration, configuration, CLI | pytest-asyncio, fixtures |
| [Performance](testing-performance.md) | Load testing, error handling | pytest-benchmark, stress tools |

## Related Documentation

- [Logger API](../api/logger/api-index.md) - Logger testing utilities
- [CLI Framework](cli/index.md) - CLI testing patterns  
- [Configuration](config/index.md) - Configuration testing
- [Context Management](logging/context.md) - Context testing patterns