# Structured Logging

Understanding why structured logging transforms observability and debugging.

## The Traditional Logging Problem

Most applications use string-based logging that embeds data within messages:

```python
# Traditional approach - data trapped in strings
log.info(f"User {user_id} logged in from {ip_address} at {timestamp}")
# Output: "User 12345 logged in from 192.168.1.1 at 2024-01-20 10:30:00"
```

This approach creates several problems:

1. **Unsearchable**: Finding all logs for user "12345" requires complex regex patterns
2. **Unparseable**: Extracting the IP address needs custom parsing logic
3. **Inconsistent**: Different developers format the same event differently
4. **Lossy**: Converting objects to strings loses type information
5. **Noisy**: Repetitive text clutters the actual data

## The Structured Solution

Structured logging treats logs as data, not text. provide.foundation separates the event description from its context:

```python
# Structured approach - data as first-class fields
logger.info("user_login", 
            user_id=12345, 
            ip_address="192.168.1.1",
            timestamp=datetime.now())
```

This produces queryable output:
```json
{
  "event": "user_login",
  "level": "info",
  "user_id": 12345,
  "ip_address": "192.168.1.1",
  "timestamp": "2024-01-20T10:30:00Z"
}
```

## Why This Matters

### 1. Powerful Queries
Search becomes trivial with structured data:
```sql
-- Find all failed logins for a user
SELECT * FROM logs 
WHERE event = 'user_login' 
  AND user_id = 12345 
  AND status = 'failed'

-- Analyze login patterns
SELECT ip_address, COUNT(*) as login_count
FROM logs
WHERE event = 'user_login'
GROUP BY ip_address
ORDER BY login_count DESC
```

### 2. Automatic Aggregation
Monitoring tools can automatically create metrics:
- Count events by type
- Calculate percentiles for durations
- Track error rates by endpoint
- Build dashboards without configuration

### 3. Context Preservation
Structured logging maintains relationships between data:
```python
# Context flows through your application
with logger.bind(request_id="req-123"):
    logger.info("request_received", method="POST", path="/api/users")
    
    user = create_user(data)
    logger.info("user_created", user_id=user.id)
    
    send_email(user)
    logger.info("welcome_email_sent", email=user.email)

# All three logs automatically include request_id="req-123"
```

### 4. Type Safety
Data types are preserved, not stringified:
```python
logger.info("metrics",
           count=42,          # Integer
           ratio=0.95,        # Float  
           active=True,       # Boolean
           tags=["web", "api"], # List
           metadata={...})     # Dict
```

## Event Naming Conventions

Structured logging requires consistent event naming. provide.foundation uses the Domain-Action-Status pattern:

```python
# Domain_Action_Status
logger.info("database_connection_established")
logger.error("payment_processing_failed")
logger.debug("cache_invalidation_completed")
```

This creates a taxonomy of events that's both human-readable and machine-parseable.

## Structured vs. Unstructured Comparison

### Finding Specific Errors

**Unstructured**:
```python
# Logging
log.error(f"Failed to process order {order_id}: {error}")

# Searching (complex regex needed)
grep "Failed to process order [0-9]+" logs.txt
```

**Structured**:
```python
# Logging
logger.error("order_processing_failed",
            order_id=order_id,
            error=str(error))

# Searching (simple field match)
jq 'select(.event == "order_processing_failed")' logs.json
```

### Tracking Performance

**Unstructured**:
```python
# Logging
log.info(f"API call took {duration}ms")

# Analysis (needs parsing)
# Extract duration with regex, convert to number, calculate stats
```

**Structured**:
```python
# Logging
logger.info("api_call_completed", duration_ms=duration)

# Analysis (direct aggregation)
jq '.duration_ms | stats' logs.json
```

## Best Practices

### 1. Use Events, Not Messages
Think of logs as events that occurred, not messages to display:

```python
# ✅ Good: Event with context
logger.info("order_placed",
           order_id=order.id,
           customer_id=customer.id,
           total=order.total)

# ❌ Bad: Message string
logger.info(f"Order {order.id} placed by customer {customer.id}")
```

### 2. Standardize Field Names
Use consistent field names across your application:

```python
# ✅ Consistent fields
logger.info("user_action", user_id=user.id, action="login")
logger.info("order_created", user_id=user.id, order_id=order.id)

# ❌ Inconsistent fields
logger.info("login", uid=user.id)
logger.info("order", customer=user.id)
```

### 3. Avoid String Interpolation
Let the logging system handle formatting:

```python
# ✅ Good: Structured fields
logger.error("database_error",
            query=sql,
            error=str(e),
            retry_count=retries)

# ❌ Bad: Pre-formatted string
logger.error(f"Database error on query '{sql}' after {retries} retries: {e}")
```

### 4. Include Relevant Context
Add fields that help diagnose issues:

```python
logger.error("api_request_failed",
            endpoint=url,
            method=method,
            status_code=response.status_code,
            response_time_ms=duration,
            retry_attempt=attempt,
            error_message=str(error))
```

## Implementation Benefits

### For Development
- **Faster Debugging**: Filter logs by any field instantly
- **Clear Intent**: Event names describe what happened
- **Less Guesswork**: Consistent structure across the codebase

### For Operations
- **Better Monitoring**: Automatic metric extraction
- **Easier Alerting**: Alert on specific field values
- **Simplified Analysis**: Query logs like a database

### For Business
- **Audit Trails**: Complete, searchable history
- **Compliance**: Structured data for regulatory requirements  
- **Analytics**: Direct business insights from logs

## Integration with Tools

Structured logs integrate seamlessly with modern observability tools:

- **Elasticsearch**: Index and search by fields
- **Datadog**: Automatic faceted search
- **Splunk**: Field extraction without configuration
- **CloudWatch**: Insights and metrics from log data
- **Grafana Loki**: Label-based log aggregation

## Performance Considerations

Structured logging with provide.foundation is optimized for performance:

1. **Lazy Evaluation**: Fields are only computed when needed
2. **Efficient Serialization**: Fast JSON encoding
3. **Smart Batching**: Group operations for throughput
4. **Memory Management**: Reuse of common strings

Benchmarks show >14,000 messages/second on modern hardware.

## Migration Strategy

Moving from string to structured logging:

1. **Start with New Code**: Use structured logging for new features
2. **High-Value First**: Convert critical paths and error handling
3. **Gradual Migration**: Update existing logs during refactoring
4. **Standardize Fields**: Create a field naming convention
5. **Tool Integration**: Configure log aggregation for structured data

## Common Patterns

### Request Tracking
```python
with logger.bind(request_id=generate_id()):
    logger.info("request_started", method=method, path=path)
    result = handle_request()
    logger.info("request_completed", status=result.status)
```

### Error Context
```python
try:
    process_data(data)
except Exception as e:
    logger.error("processing_failed",
                error=str(e),
                error_type=type(e).__name__,
                input_size=len(data))
```

### Performance Metrics
```python
start = time.time()
result = expensive_operation()
logger.info("operation_completed",
           duration_ms=(time.time() - start) * 1000,
           result_size=len(result))
```

## Summary

Structured logging transforms logs from text artifacts into queryable, analyzable data. By treating log entries as events with associated context, provide.foundation enables:

- Powerful searching and filtering
- Automatic metric generation  
- Consistent debugging workflows
- Seamless tool integration

The small change from string interpolation to structured fields yields massive improvements in observability, debugging speed, and operational intelligence.

## Next Steps

- 🎭 [Semantic Layers](emoji-sets.md) - Domain-specific logging interfaces
- 🎯 [DAS Pattern](das-pattern.md) - Domain-Action-Status naming
- 🎨 [Emoji System](emoji-system.md) - Visual log parsing
- ⚡ [Performance](performance.md) - Optimization strategies
- 🏠 [Back to Concepts](index.md)
