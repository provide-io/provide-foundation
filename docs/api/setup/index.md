# Setup API Reference

Foundation initialization and teardown functions for managing the complete telemetry system lifecycle.

## Overview

The setup module provides Foundation's core lifecycle management with:
- **System Initialization** - Complete Foundation system setup and configuration
- **Graceful Shutdown** - Proper teardown of all subsystems
- **Configuration Management** - Environment-based and explicit configuration
- **Testing Support** - State reset utilities for test isolation
- **Legacy Compatibility** - Backward-compatible function aliases
- **Future-Ready** - Designed for additional subsystem integration

## Quick Start

```python
from provide.foundation.setup import setup_foundation, shutdown_foundation
from provide.foundation import TelemetryConfig, LoggingConfig

# Basic setup with defaults
setup_foundation()

# Custom configuration setup
config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="json",
        log_file="/var/log/myapp.log"
    )
)
setup_foundation(config)

# Graceful shutdown
import asyncio
await shutdown_foundation()
```

## Initialization Functions

### `setup_foundation(config: TelemetryConfig | None = None) -> None`

Initialize the complete Foundation system with all subsystems.

**Parameters**:
- `config: TelemetryConfig | None` - Configuration to use. If None, loads from environment

**Subsystems Initialized**:
- Logging system setup and configuration
- Stream configuration (file logging, output redirection)
- Future: Tracer initialization
- Future: Metrics collection setup

```python
from provide.foundation.setup import setup_foundation
from provide.foundation import TelemetryConfig, LoggingConfig

# Default setup (reads from environment)
setup_foundation()

# Custom configuration
config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="DEBUG",
        console_formatter="key_value",
        das_emoji_prefix_enabled=True,
        log_file="/var/log/debug.log"
    )
)
setup_foundation(config)

# Production setup
production_config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="json",
        das_emoji_prefix_enabled=False,
        log_file="/var/log/app.log"
    )
)
setup_foundation(production_config)
```

### `setup_telemetry(config: TelemetryConfig | None = None) -> None`

Legacy alias for `setup_foundation()` - maintained for backward compatibility.

**Parameters**: Same as `setup_foundation()`

```python
from provide.foundation.setup import setup_telemetry

# Legacy usage (still supported)
setup_telemetry()

# Equivalent to setup_foundation()
setup_telemetry(config)
```

## Shutdown Functions

### `async shutdown_foundation(timeout_millis: int = 5000) -> None`

Gracefully shutdown all Foundation subsystems.

**Parameters**:
- `timeout_millis: int` - Timeout for shutdown in milliseconds (currently unused, reserved for future)

**Shutdown Operations**:
- Flush all logging streams to ensure data persistence
- Close file handles and reset stream state
- Future: Shutdown tracer subsystem
- Future: Stop metrics collection

```python
import asyncio
from provide.foundation.setup import shutdown_foundation

async def application_shutdown():
    """Proper application shutdown sequence."""
    print("Shutting down application...")
    
    # Shutdown Foundation (flushes logs, closes files)
    await shutdown_foundation()
    
    print("Foundation shutdown complete")

# Use in application lifecycle
if __name__ == "__main__":
    try:
        # Application code
        main()
    finally:
        # Ensure clean shutdown
        asyncio.run(application_shutdown())
```

### `async shutdown_foundation_telemetry(timeout_millis: int = 5000) -> None`

Legacy alias for `shutdown_foundation()` - maintained for backward compatibility.

**Parameters**: Same as `shutdown_foundation()`

```python
from provide.foundation.setup import shutdown_foundation_telemetry

# Legacy usage (still supported)
await shutdown_foundation_telemetry()

# Equivalent to shutdown_foundation()
await shutdown_foundation_telemetry(timeout_millis=10000)
```

## Testing Support

### `reset_foundation_setup_for_testing() -> None`

Reset Foundation's internal state for test isolation.

**Reset Operations**:
- Reset structlog configuration to defaults
- Clear Foundation logger state and configuration
- Reset stream state back to stderr
- Clear lazy setup state tracking
- Clear all cached configurations

```python
from provide.foundation.setup import reset_foundation_setup_for_testing
from provide.foundation import setup_foundation, TelemetryConfig

def test_logging_configuration():
    """Test with clean Foundation state."""
    # Ensure clean state before test
    reset_foundation_setup_for_testing()
    
    # Configure for test
    test_config = TelemetryConfig(
        logging=LoggingConfig(default_level="DEBUG")
    )
    setup_foundation(test_config)
    
    # Test logging behavior
    logger.debug("test_message")
    
    # Clean up after test (optional, but good practice)
    reset_foundation_setup_for_testing()

class TestFoundationSetup:
    """Test class with proper setup/teardown."""
    
    def setup_method(self):
        """Reset state before each test."""
        reset_foundation_setup_for_testing()
    
    def teardown_method(self):
        """Clean up after each test."""
        reset_foundation_setup_for_testing()
    
    def test_custom_setup(self):
        """Test custom configuration."""
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="json"
            )
        )
        setup_foundation(config)
        
        # Test with this configuration
        logger.info("test_info_message")
```

## Configuration Examples

### Environment-Based Setup

Foundation automatically reads configuration from environment variables:

```python
from provide.foundation.setup import setup_foundation

# Set environment variables
import os
os.environ.update({
    'PROVIDE_LOG_LEVEL': 'DEBUG',
    'PROVIDE_LOG_CONSOLE_FORMATTER': 'json',
    'PROVIDE_LOG_DAS_EMOJI_ENABLED': 'true',
    'PROVIDE_LOG_FILE': '/var/log/myapp.log'
})

# Setup reads from environment
setup_foundation()  # Uses environment configuration
```

### Application-Specific Setup

```python
from provide.foundation.setup import setup_foundation
from provide.foundation import TelemetryConfig, LoggingConfig

def setup_for_web_app():
    """Setup optimized for web applications."""
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",          # Machine-readable logs
            das_emoji_prefix_enabled=False,    # No emojis in production
            enabled_emoji_sets=["http"],       # HTTP-specific emojis only
            log_file="/var/log/webapp.log"
        )
    )
    setup_foundation(config)

def setup_for_cli_app():
    """Setup optimized for CLI applications."""
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="key_value",     # Human-readable logs
            das_emoji_prefix_enabled=True,     # Visual parsing aids
            enabled_emoji_sets=["http", "database"],
            # No log file for CLI apps
        )
    )
    setup_foundation(config)

def setup_for_development():
    """Setup optimized for development."""
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="DEBUG",             # Verbose logging
            console_formatter="key_value",     # Human-readable
            das_emoji_prefix_enabled=True,     # Visual aids
            enabled_emoji_sets=["http", "database", "llm"],
            log_file="debug.log"               # Local debug file
        )
    )
    setup_foundation(config)
```

### Conditional Setup

```python
import os
from provide.foundation.setup import setup_foundation
from provide.foundation import TelemetryConfig, LoggingConfig

def smart_setup():
    """Setup based on deployment environment."""
    environment = os.getenv('ENVIRONMENT', 'development')
    
    if environment == 'production':
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="WARNING",       # Minimal noise
                console_formatter="json",      # Structured logs
                das_emoji_prefix_enabled=False,# No emojis
                log_file="/var/log/app.log"
            )
        )
    
    elif environment == 'staging':
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="json",
                das_emoji_prefix_enabled=False,
                log_file="/var/log/staging.log"
            )
        )
    
    elif environment == 'development':
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="DEBUG",
                console_formatter="key_value",
                das_emoji_prefix_enabled=True,
                log_file="dev.log"
            )
        )
    
    else:  # testing, ci, etc.
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="compact",
                das_emoji_prefix_enabled=False,
                # No log file for testing
            )
        )
    
    setup_foundation(config)

# Call during application startup
smart_setup()
```

## Integration Examples

### Web Application Lifecycle

```python
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from provide.foundation.setup import setup_foundation, shutdown_foundation
from provide.foundation import TelemetryConfig, LoggingConfig, logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan management with Foundation."""
    # Startup
    logger.info("🚀 Starting web application")
    
    # Configure Foundation for web app
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
            log_file="/var/log/webapp.log"
        )
    )
    setup_foundation(config)
    
    logger.info("✅ Foundation setup complete")
    
    yield  # Application runs
    
    # Shutdown
    logger.info("🛑 Shutting down web application")
    await shutdown_foundation()
    logger.info("✅ Foundation shutdown complete")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    logger.info("🌐 Root endpoint accessed")
    return {"message": "Hello, World!"}
```

### CLI Application Pattern

```python
import asyncio
import click
from provide.foundation.setup import setup_foundation, shutdown_foundation
from provide.foundation import TelemetryConfig, LoggingConfig, logger

@click.command()
@click.option('--debug', is_flag=True, help='Enable debug logging')
@click.option('--log-file', help='Log to file')
def main(debug, log_file):
    """CLI application with Foundation integration."""
    
    # Setup Foundation based on CLI options
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="DEBUG" if debug else "INFO",
            console_formatter="key_value",
            das_emoji_prefix_enabled=True,
            log_file=log_file
        )
    )
    setup_foundation(config)
    
    logger.info("🎯 CLI application started")
    
    try:
        # Main application logic
        process_data()
        logger.info("✅ Processing complete")
        
    except KeyboardInterrupt:
        logger.warning("⚠️ Operation cancelled by user")
    except Exception as e:
        logger.error("❌ Application error", error=str(e))
        raise
    finally:
        # Ensure clean shutdown
        logger.info("🔄 Shutting down...")
        asyncio.run(shutdown_foundation())

def process_data():
    """Main application logic."""
    logger.info("📊 Processing data")
    # Implementation here
    pass

if __name__ == "__main__":
    main()
```

### Service/Daemon Pattern

```python
import asyncio
import signal
import sys
from provide.foundation.setup import setup_foundation, shutdown_foundation
from provide.foundation import TelemetryConfig, LoggingConfig, logger

class ServiceManager:
    """Service manager with proper Foundation lifecycle."""
    
    def __init__(self):
        self.running = False
        self.shutdown_event = asyncio.Event()
    
    async def setup(self):
        """Initialize the service."""
        logger.info("🔧 Setting up service")
        
        # Configure for long-running service
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="json",
                log_file="/var/log/service.log"
            )
        )
        setup_foundation(config)
        
        # Setup signal handlers
        for sig in [signal.SIGTERM, signal.SIGINT]:
            signal.signal(sig, self._signal_handler)
        
        logger.info("✅ Service setup complete")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"🛑 Received signal {signum}, shutting down...")
        self.shutdown_event.set()
    
    async def run(self):
        """Main service loop."""
        self.running = True
        logger.info("🚀 Service started")
        
        try:
            while self.running and not self.shutdown_event.is_set():
                # Service work
                await self.do_work()
                
                # Wait for next iteration or shutdown signal
                try:
                    await asyncio.wait_for(
                        self.shutdown_event.wait(), 
                        timeout=10.0
                    )
                    break  # Shutdown requested
                except asyncio.TimeoutError:
                    continue  # Continue normal operation
                    
        except Exception as e:
            logger.error("❌ Service error", error=str(e))
            raise
        finally:
            await self.shutdown()
    
    async def do_work(self):
        """Service work implementation."""
        logger.debug("⚙️ Processing work")
        await asyncio.sleep(1)  # Simulate work
    
    async def shutdown(self):
        """Shutdown the service."""
        logger.info("🔄 Service shutting down")
        self.running = False
        
        # Shutdown Foundation
        await shutdown_foundation()
        logger.info("✅ Service shutdown complete")

async def main():
    """Service entry point."""
    service = ServiceManager()
    await service.setup()
    
    try:
        await service.run()
    except KeyboardInterrupt:
        logger.info("⚠️ Service interrupted")
    except Exception as e:
        logger.error("❌ Service failed", error=str(e))
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
```

### Testing Integration

```python
import pytest
import asyncio
from provide.foundation.setup import (
    setup_foundation, 
    shutdown_foundation,
    reset_foundation_setup_for_testing
)
from provide.foundation import TelemetryConfig, LoggingConfig, logger

class TestApplicationWithFoundation:
    """Test class with proper Foundation setup/teardown."""
    
    def setup_method(self):
        """Setup before each test."""
        # Reset Foundation state
        reset_foundation_setup_for_testing()
        
        # Configure for testing
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="DEBUG",
                console_formatter="compact"
                # No log file for tests
            )
        )
        setup_foundation(config)
    
    def teardown_method(self):
        """Cleanup after each test."""
        # Reset state for next test
        reset_foundation_setup_for_testing()
    
    def test_logging_works(self):
        """Test that logging works as expected."""
        logger.info("test_info_message")
        logger.debug("test_debug_message")
        # Add assertions about log output
    
    @pytest.mark.asyncio
    async def test_async_shutdown(self):
        """Test async shutdown functionality."""
        logger.info("test_before_shutdown")
        
        # Test shutdown doesn't raise errors
        await shutdown_foundation()
        
        # Note: After shutdown, new logs may not work as expected
        # Reset needed for subsequent operations

@pytest.fixture(scope="session")
async def foundation_session():
    """Session-level Foundation setup for integration tests."""
    # Setup once for entire test session
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="compact"
        )
    )
    setup_foundation(config)
    
    yield
    
    # Cleanup after all tests
    await shutdown_foundation()

@pytest.mark.asyncio
async def test_integration_with_foundation(foundation_session):
    """Integration test using session-level Foundation setup."""
    logger.info("integration_test_started")
    
    # Test application logic
    result = await some_async_operation()
    assert result is not None
    
    logger.info("integration_test_completed")
```

## Best Practices

### 1. Single Setup Per Process

```python
# ✅ Good - Single setup call
def main():
    setup_foundation(config)  # Once at startup
    # Application logic
    
# ❌ Bad - Multiple setups
def bad_main():
    setup_foundation(config1)  # First setup
    setup_foundation(config2)  # Overwrites first setup
```

### 2. Always Use Graceful Shutdown

```python
# ✅ Good - Proper shutdown
async def main():
    setup_foundation()
    try:
        await run_application()
    finally:
        await shutdown_foundation()  # Always cleanup

# ❌ Bad - No shutdown
def bad_main():
    setup_foundation()
    run_application()
    # Process exits without cleanup
```

### 3. Test Isolation

```python
# ✅ Good - Reset between tests
class TestSuite:
    def setup_method(self):
        reset_foundation_setup_for_testing()
        setup_foundation(test_config)
    
    def teardown_method(self):
        reset_foundation_setup_for_testing()

# ❌ Bad - State leaks between tests
def test_without_reset():
    setup_foundation(config)  # May interfere with other tests
```

### 4. Environment-Aware Configuration

```python
# ✅ Good - Environment-specific setup
def setup_for_environment():
    if os.getenv('ENVIRONMENT') == 'production':
        setup_foundation(production_config)
    elif os.getenv('TESTING'):
        setup_foundation(test_config)
    else:
        setup_foundation()  # Default/development config

# ❌ Bad - One-size-fits-all
def bad_setup():
    setup_foundation(debug_config)  # Same config everywhere
```

## Error Handling

### Setup Errors

```python
from provide.foundation.setup import setup_foundation
from provide.foundation.errors import ConfigurationError

try:
    setup_foundation(config)
except ConfigurationError as e:
    print(f"Configuration error: {e}")
    # Handle configuration issues
    sys.exit(1)
except Exception as e:
    print(f"Setup failed: {e}")
    sys.exit(1)
```

### Shutdown Errors

```python
import asyncio
from provide.foundation.setup import shutdown_foundation

async def safe_shutdown():
    """Shutdown with error handling."""
    try:
        await shutdown_foundation(timeout_millis=10000)
    except asyncio.TimeoutError:
        print("Warning: Shutdown timeout exceeded")
    except Exception as e:
        print(f"Shutdown error: {e}")
        # Continue with application shutdown anyway
```

## Thread Safety

Setup functions are thread-safe but should only be called once:

```python
import threading
from provide.foundation.setup import setup_foundation

# Safe to call from any thread, but only call once
setup_done = threading.Event()

def worker():
    setup_done.wait()  # Wait for setup to complete
    # Use Foundation logging
    logger.info("Worker started")

def main():
    # Setup from main thread
    setup_foundation()
    setup_done.set()  # Signal setup complete
    
    # Start worker threads
    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
```

## See Also

- [Logger API](../logger/) - Foundation logging system
- [Configuration API](../config/) - Configuration management
- [Testing API](../testing/) - Testing utilities and fixtures  
- [Context API](../context/) - Context management system