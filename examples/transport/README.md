# Transport Examples

HTTP client and networking capabilities using provide-foundation's transport system.

## Examples

### 01_http_client.py
Comprehensive HTTP client usage with middleware, error handling, and streaming.

**Features:**
- Basic HTTP methods (GET, POST, PUT, DELETE)
- UniversalClient session management
- Middleware pipeline configuration
- Error handling with specific exception types
- Response processing (JSON, text, headers)
- Timeout and retry configuration
- Global vs client-specific usage patterns

## Key Concepts

### UniversalClient
Foundation's primary HTTP client with automatic transport discovery, connection pooling, and middleware support.

### Middleware Pipeline
Extensible request/response processing including:
- Automatic logging of all HTTP operations
- Metrics collection for performance monitoring  
- Retry logic with configurable backoff strategies
- Custom middleware for authentication, caching, etc.

### Error Handling
Comprehensive error types for different failure scenarios:
- `TransportTimeoutError` - Request timeouts
- `TransportConnectionError` - Network connectivity issues
- `HTTPResponseError` - HTTP 4xx/5xx status codes
- `TransportNotFoundError` - Unknown protocols

### Transport Registry
Automatic protocol discovery based on URI schemes with support for custom transport implementations.

## Usage Patterns

The example demonstrates several usage patterns:
1. **Simple requests** - Direct function calls for quick operations
2. **Session management** - UniversalClient for multiple related requests
3. **Middleware configuration** - Custom processing pipelines
4. **Error scenarios** - Handling various failure modes
5. **Response processing** - Working with different content types

## Related Documentation

- [HTTP Requests Guide](../../docs/how-to-guides/http/requests.md) - HTTP client usage patterns
- [HTTP Middleware Guide](../../docs/how-to-guides/http/middleware.md) - Middleware configuration and examples
