# OpenObserve Integration Examples

This directory contains examples demonstrating Foundation's OpenObserve integration for log aggregation, querying, and streaming.

## Prerequisites

### 1. Install Foundation with OpenObserve support

```bash
uv add 'provide-foundation[openobserve]'
```

### 2. Run OpenObserve

The easiest way to run OpenObserve is via Docker:

```bash
# Run OpenObserve with default credentials
docker run -d \
  -p 5080:5080 \
  -e ZO_ROOT_USER_EMAIL="root@example.com" \
  -e ZO_ROOT_USER_PASSWORD="password" \
  --name openobserve \
  public.ecr.aws/zinclabs/openobserve:latest
```

### 3. Configure Environment Variables

```bash
export OPENOBSERVE_URL="http://localhost:5080/api/default"
export OPENOBSERVE_USER="root@example.com"
export OPENOBSERVE_PASSWORD="password"
export OPENOBSERVE_ORG="default"  # Optional
export OPENOBSERVE_STREAM="default"  # Optional
```

## Examples

### 01_openobserve_integration.py

Complete end-to-end example demonstrating:
- Sending logs to OpenObserve (via OTLP or bulk API)
- Querying logs with SQL
- Searching by level, trace ID, service
- Aggregating log counts
- Multiple output formats (JSON, table, log, summary)

```bash
python examples/openobserve/01_openobserve_integration.py
```

## CLI Commands

Foundation provides CLI commands for working with OpenObserve:

### Test Connection

```bash
foundation openobserve test
```

### Query Logs

```bash
# Basic query
foundation openobserve query --sql "SELECT * FROM default" --start "-1h"

# With formatting
foundation openobserve query \
  --sql "SELECT * FROM default WHERE level='ERROR'" \
  --format table \
  --start "-24h"
```

### Tail Logs (Follow Mode)

```bash
# Tail all logs
foundation openobserve tail

# Tail with filter
foundation openobserve tail --filter "level=ERROR"

# Tail specific stream
foundation openobserve tail --stream my_app_logs --filter "service=api"
```

### Search Errors

```bash
foundation openobserve errors --stream default --start "-6h"
```

### Search by Trace ID

```bash
foundation openobserve trace <trace_id> --stream default
```

### List Streams

```bash
foundation openobserve streams
```

### View Search History

```bash
foundation openobserve history --size 10
```

## OTLP Auto-Configuration

When OpenObserve is configured and reachable, Foundation automatically configures OTLP (OpenTelemetry Protocol) settings:

- **OTLP Endpoint**: Derived from `OPENOBSERVE_URL`
- **OTLP Headers**: Automatically includes organization and stream headers
- **Seamless Integration**: No additional OTLP configuration needed

This allows you to use OpenTelemetry SDKs with OpenObserve automatically.

## Features

### Log Querying
- Full SQL query support
- Time range filtering (relative and absolute)
- Multiple output formats (JSON, table, CSV, log format)
- Pagination support

### Log Streaming
- Real-time log tailing (like `tail -f`)
- Filter-based streaming
- HTTP/2 streaming support
- Polling-based streaming fallback

### Search Operations
- Search by log level
- Search by trace ID
- Search by service name
- Error log filtering
- Custom SQL queries

### Formatters
- **JSON**: Machine-readable output
- **Table**: Columnar display
- **Log**: Human-readable log format
- **CSV**: Spreadsheet-compatible
- **Summary**: Condensed overview

## Integration Patterns

### 1. Direct Log Sending

```python
from provide.foundation.integrations.openobserve import send_log

send_log(
    message="Operation completed",
    level="INFO",
    service="my_service",
    attributes={"user_id": "123", "action": "login"}
)
```

### 2. Querying Logs

```python
from provide.foundation.integrations.openobserve import search_logs

response = search_logs(
    sql="SELECT * FROM default WHERE level='ERROR'",
    start_time="-1h",
    size=100
)

for hit in response.hits:
    print(f"{hit['level']}: {hit['message']}")
```

### 3. Streaming Logs

```python
from provide.foundation.integrations.openobserve import tail_logs

for log_entry in tail_logs(stream="default", filters={"level": "ERROR"}):
    print(f"New error: {log_entry['message']}")
```

## Troubleshooting

### Connection Issues

```bash
# Test OpenObserve connection
foundation openobserve test

# Check if OpenObserve is running
curl http://localhost:5080/healthz
```

### Authentication Errors

- Verify `OPENOBSERVE_USER` and `OPENOBSERVE_PASSWORD` are correct
- Check organization name matches (default is "default")

### No Logs Found

- Ensure logs are being sent to the correct stream
- Check time range (use wider range like `-24h`)
- Verify stream exists: `foundation openobserve streams`

## Learn More

- [OpenObserve Documentation](https://openobserve.ai/docs/)
- [Foundation Documentation](https://github.com/provide-io/provide-foundation)
- [OpenTelemetry Protocol](https://opentelemetry.io/docs/specs/otlp/)
