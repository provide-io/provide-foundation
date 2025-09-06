# Configuration Best Practices

Production-ready configuration strategies for provide.foundation applications.

## Environment-Specific Configuration

### Development Environment

Optimize for developer experience and debugging:

```bash
# .env.development
PROVIDE_LOG_LEVEL=DEBUG
PROVIDE_LOG_FORMAT=pretty
PROVIDE_NO_EMOJI=false
PROVIDE_NO_COLOR=false
PROVIDE_LOG_CALLER_INFO=true
PROVIDE_EMOJI_SETS=true
PROVIDE_LAYER_EMOJI=true
PROVIDE_CONFIG_RELOAD=true
PROVIDE_VERBOSE=2
```

```yaml
# config.development.yaml
logging:
  level: DEBUG
  format: pretty
  no_emoji: false
  caller_info: true
  
emoji_sets:
  enabled: true
  emoji: true
  validation: true
  
debug:
  show_config: true
  trace_processors: true
  profile: false
```

### Staging Environment

Balance between debugging and production-like behavior:

```bash
# .env.staging
PROVIDE_LOG_LEVEL=INFO
PROVIDE_LOG_FORMAT=json
PROVIDE_NO_EMOJI=true
PROVIDE_LOG_FILE=/var/log/app.staging.log
PROVIDE_OTEL_ENDPOINT=http://staging-otel:4317
PROVIDE_OTEL_SAMPLE_RATE=0.5
PROVIDE_APP_ENVIRONMENT=staging
```

```yaml
# config.staging.yaml
logging:
  level: INFO
  format: json
  no_emoji: true
  file: /var/log/app.staging.log
  
otel:
  endpoint: http://staging-otel:4317
  sample_rate: 0.5
  traces: true
  metrics: true
  
app:
  environment: staging
  debug: false
```

### Production Environment

Optimize for performance, reliability, and observability:

```bash
# .env.production
PROVIDE_LOG_LEVEL=WARNING
PROVIDE_LOG_FORMAT=json
PROVIDE_NO_EMOJI=true
PROVIDE_NO_COLOR=true
PROVIDE_LOG_FILE=/var/log/app.log
PROVIDE_ASYNC_LOGGING=true
PROVIDE_BUFFER_SIZE=10000
PROVIDE_OTEL_ENDPOINT=https://prod-otel:4317
PROVIDE_OTEL_SAMPLE_RATE=0.1
PROVIDE_OTEL_COMPRESSION=gzip
PROVIDE_APP_ENVIRONMENT=production
PROVIDE_DROP_ON_OVERFLOW=true
```

```yaml
# config.production.yaml
logging:
  level: WARNING
  format: json
  no_emoji: true
  no_color: true
  file: /var/log/app.log
  
performance:
  async_logging: true
  buffer_size: 10000
  batch_size: 500
  drop_on_overflow: true
  
otel:
  endpoint: https://prod-otel:4317
  sample_rate: 0.1
  compression: gzip
  timeout_ms: 5000
  
app:
  environment: production
  debug: false
```

