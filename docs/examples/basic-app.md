# Basic Application

Simple application setup with structured logging using provide-foundation.

## Overview

This example demonstrates the minimal setup needed to get started with provide-foundation in a basic Python application. It shows structured logging, configuration management, and telemetry setup.

## Code Example

```python
#!/usr/bin/env python3
"""
Basic Application Example

Demonstrates minimal setup for provide-foundation with structured logging.
"""

from provide.foundation import Context, logger, setup_telemetry
from provide.foundation.console import pout


def main():
    """Main application entry point."""
    # Create context from environment
    ctx = Context.from_env()
    
    # Setup telemetry with context
    setup_telemetry(ctx.to_telemetry_config())
    
    # Application startup
    logger.info("application_startup", version="1.0.0", profile=ctx.profile)
    
    # Example business logic with structured logging
    process_data()
    
    # Application shutdown
    logger.info("application_shutdown", status="success")
    pout("Application completed successfully")


def process_data():
    """Example business logic with structured logging."""
    logger.info("data_processing_start", operation="user_registration")
    
    try:
        # Simulate some work
        user_id = "usr_12345"
        email = "user@example.com"
        
        logger.info("user_created", user_id=user_id, email=email, status="success")
        
    except Exception as e:
        logger.exception("user_creation_failed", error=str(e))
        raise


if __name__ == "__main__":
    main()
```

## Key Features Demonstrated

### Structured Logging
- Event-based logging with semantic field names
- Automatic context enrichment with visual markers
- Exception handling with full traceback capture

### Configuration Management
- Environment-based configuration loading
- Context integration with telemetry system
- Profile-based settings management

### Output Handling
- Separation of user-facing output (`pout`) from logging
- Structured log events for monitoring and debugging
- Clean console output for end users

## Running the Example

1. Set up your environment:
```bash
export FOUNDATION_LOG_LEVEL=INFO
export FOUNDATION_PROFILE=development
export FOUNDATION_DEBUG=false
```

2. Run the application:
```bash
python basic_app.py
```

## Expected Output

```
INFO application_startup version=1.0.0 profile=development
INFO data_processing_start operation=user_registration  
✅ INFO user_created user_id=usr_12345 email=user@example.com status=success
INFO application_shutdown status=success
Application completed successfully
```

## Configuration Options

You can customize the behavior through environment variables:

```bash
# Set log level
export FOUNDATION_LOG_LEVEL=DEBUG

# Enable JSON output
export FOUNDATION_JSON_OUTPUT=true

# Set service identification
export FOUNDATION_SERVICE_NAME=my-basic-app
export FOUNDATION_SERVICE_VERSION=1.0.0
```

## Next Steps

- Explore [CLI Tool](cli-tool.md) for command-line interfaces
- Learn about [Web Service](web-service.md) patterns for HTTP services
- Review [Data Pipeline](data-pipeline.md) for data processing workflows