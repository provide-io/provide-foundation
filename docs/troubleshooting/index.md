# Troubleshooting Guide

This guide helps you diagnose and resolve common issues when using provide.foundation.

## Quick Diagnostics

Run this diagnostic script to check your installation:

```python
from provide.foundation import logger
from provide.foundation.platform import get_system_info
from provide.foundation.config import TelemetryConfig

# Check installation
try:
    config = TelemetryConfig.from_env()
    print(f"✅ Configuration loaded: {config.level}")
except Exception as e:
    print(f"❌ Configuration error: {e}")

# Check platform
info = get_system_info()
print(f"Platform: {info.platform} {info.arch}")
print(f"Python: {info.python_version}")

# Test logging
logger.info("test_message", diagnostic=True)
print("✅ Logging functional")
```

## Common Issues

### 🔴 Import Errors

**Problem**: `ModuleNotFoundError: No module named 'provide.foundation'`

**Solution**:
```bash
# Ensure installation
pip install provide-foundation

# Or with development dependencies
pip install provide-foundation[dev]
```

### 🔴 Logger Not Outputting

**Problem**: Logger calls don't produce any output

**Solutions**:

1. **Check log level**:
```python
import os
os.environ["PROVIDE_LOG_LEVEL"] = "DEBUG"

from provide.foundation import logger
logger.debug("This should appear")
```

2. **Verify initialization**:
```python
from provide.foundation.logger import setup_logging
setup_logging(level="DEBUG", format="pretty")
```

### 🔴 Configuration Not Loading

**Problem**: Environment variables not being picked up

**Solutions**:

1. **Check environment variable names**:
```bash
# Correct format
export PROVIDE_LOG_LEVEL=DEBUG
export PROVIDE_LOG_FORMAT=json

# Not FOUNDATION_LOG_LEVEL (wrong prefix)
```

2. **Verify configuration loading**:
```python
from provide.foundation.config import TelemetryConfig
config = TelemetryConfig.from_env()
print(config)
```

### 🔴 Performance Issues

**Problem**: Logging is slow or blocking

**Solutions**:

1. **Use async logging for high-throughput**:
```python
import asyncio
from provide.foundation import logger

async def main():
    # Async context for better performance
    async with logger.bind(request_id="123"):
        await logger.ainfo("async_log")
```

2. **Adjust processor chain**:
```python
from provide.foundation.logger import setup_logging

# Minimize processors for performance
setup_logging(
    processors=["timestamp", "level"],  # Minimal processing
    format="json"  # Faster than pretty format
)
```

### 🔴 CLI Commands Not Registering

**Problem**: Decorated commands not appearing in CLI

**Solution**:
```python
# Ensure commands are imported before running
from provide.foundation.cli import run_cli

# Import your command modules
import myapp.commands  # This triggers registration

if __name__ == "__main__":
    run_cli()
```

## Platform-Specific Issues

### macOS

- **Emoji display issues**: Ensure terminal supports UTF-8
- **Permission errors**: Check file permissions for log outputs

### Linux

- **systemd integration**: Use JSON format for journald compatibility
- **Container logging**: Set `PROVIDE_LOG_FORMAT=json` for container environments

### Windows

- **Color output**: Enable ANSI colors in terminal
- **Path issues**: Use forward slashes in configuration files

## Debug Techniques

### Enable Verbose Logging

```python
import logging
import structlog

# Enable debug for all loggers
logging.basicConfig(level=logging.DEBUG)
structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG)
)
```

### Trace Processor Chain

```python
from provide.foundation.logger import get_logger_config

config = get_logger_config()
for processor in config.processors:
    print(f"Processor: {processor}")
```

### Check Thread Safety

```python
import threading
from provide.foundation import logger

def worker(n):
    logger.info("worker_message", thread=n)

threads = [threading.Thread(target=worker, args=(i,)) 
           for i in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

## Error Messages Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `ConfigurationError: Invalid log level` | Unknown log level string | Use: DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `ProcessorError: Failed to serialize` | Non-JSON serializable object | Convert objects to primitives |
| `ImportError: No module named 'emoji'` | Missing optional dependency | `pip install provide-foundation[emoji]` |
| `RuntimeError: Event loop is closed` | Async context issue | Ensure proper async context management |

## Getting Help

1. **Check the FAQ**: [Frequently Asked Questions](faq.md)
2. **Search Issues**: [GitHub Issues](https://github.com/provide-io/provide-foundation/issues)
3. **Community Support**: [Discussions](../community/support.md)
4. **File a Bug**: [Bug Report Template](https://github.com/provide-io/provide-foundation/issues/new)

## Diagnostic Checklist

- [ ] Latest version installed: `pip show provide-foundation`
- [ ] Python version ≥ 3.11: `python --version`
- [ ] Environment variables set correctly
- [ ] No conflicting logger configurations
- [ ] Terminal supports UTF-8 for emoji display
- [ ] Write permissions for log output locations
- [ ] No circular imports in custom processors