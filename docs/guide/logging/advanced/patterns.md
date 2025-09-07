# Integration Patterns

Common patterns for integrating provide.foundation logging with various frameworks and systems.

## Overview

This section covers integration patterns for different types of applications and frameworks. Each pattern provides:

- **Setup examples** - Complete configuration for the framework
- **Middleware integration** - Request/response logging patterns
- **Context management** - Maintaining context across async operations
- **Performance considerations** - Optimizations for high-throughput scenarios
- **Best practices** - Production-ready configurations

## Pattern Categories

### [Web Framework Integration](patterns-web.md)

Integration patterns for web frameworks including:
- FastAPI with async middleware
- Django with request context
- Flask with application context
- Starlette middleware patterns
- Request/response logging
- Error handling integration

### [Database Integration](patterns-database.md)

Database integration patterns covering:
- SQLAlchemy with connection pooling
- AsyncPG with transaction context
- MongoDB with operation logging
- Redis with command logging
- Connection lifecycle management
- Query performance monitoring

### [Message Queue Integration](patterns-messaging.md)

Message queue and event-driven patterns:
- Celery task logging
- RabbitMQ with pika integration
- Apache Kafka consumers/producers
- Redis pub/sub patterns
- Event sourcing integration
- Distributed tracing across services

### [Async Application Patterns](patterns-async.md)

Patterns for async/concurrent applications:
- asyncio task context
- Concurrent futures logging
- Background task management
- Context propagation patterns
- Error handling in async code
- Performance monitoring

## Quick Navigation

| Pattern Type | Best For | Key Features |
|-------------|----------|--------------|
| [Web](patterns-web.md) | REST APIs, web applications | Request tracing, middleware integration |
| [Database](patterns-database.md) | Data-heavy applications | Query logging, transaction context |
| [Messaging](patterns-messaging.md) | Event-driven systems | Message correlation, async processing |
| [Async](patterns-async.md) | High-concurrency apps | Task context, concurrent execution |

## Related Documentation

- [Advanced Logging](../advanced.md) - Advanced logging techniques
- [Performance Tuning](../performance.md) - Optimizing log performance
- [Context Management](../context.md) - Managing log context
- [Filtering](filtering.md) - Log filtering strategies