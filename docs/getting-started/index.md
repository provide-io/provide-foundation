# Getting Started

Welcome to provide.foundation! This guide will help you get up and running quickly.

## Quick Navigation

<div class="feature-grid">
  <div class="feature-card">
    <h3>📦 Installation</h3>
    <p>Install provide.foundation and its dependencies</p>
    <a href="installation">Get Started →</a>
  </div>
  
  <div class="feature-card">
    <h3>🚀 Quick Start</h3>
    <p>Your first provide.foundation application in 5 minutes</p>
    <a href="quick-start">Learn More →</a>
  </div>
  
  <div class="feature-card">
    <h3>💻 First Application</h3>
    <p>Build a complete application with logging, CLI, and configuration</p>
    <a href="first-app">Build Now →</a>
  </div>
  
  <div class="feature-card">
    <h3>📚 Examples</h3>
    <p>Explore real-world examples and use cases</p>
    <a href="examples">Browse →</a>
  </div>
</div>

## What is provide.foundation?

provide.foundation is a comprehensive Python library that provides:

- **🎯 Structured Logging**: Beautiful, performant logging with emoji-enhanced visual parsing
- **🖥️ CLI Framework**: Decorator-based command registration with automatic help generation  
- **⚙️ Configuration Management**: Environment-based configuration with type safety
- **🔧 System Utilities**: Cross-platform utilities for process execution, platform detection, and more

## Why provide.foundation?

### For Developers
- **Zero Configuration**: Works beautifully out of the box
- **Type Safe**: Full type hints and runtime validation
- **Fast**: Optimized for production workloads (>14,000 msg/sec)
- **Testable**: Built-in testing utilities

### For Teams
- **Consistent**: Standardized logging across all services
- **Observable**: Structured logs ready for analysis
- **Maintainable**: Clean, well-documented APIs
- **Extensible**: Plugin system for customization

## Core Features at a Glance

### Structured Logging
```python
from provide.foundation import logger

logger.info("user_login", 
            user_id="user-123",
            ip_address="192.168.1.1",
            success=True)
```

### CLI Framework
```python
from provide.foundation.cli import register_command

@register_command("deploy")
def deploy(environment: str = "staging"):
    """Deploy the application."""
    logger.info("deployment_started", env=environment)
```

### Configuration Management
```python
from provide.foundation.config import TelemetryConfig

config = TelemetryConfig.from_env()
logger.info("config_loaded", level=config.level)
```

### Platform Utilities
```python
from provide.foundation.platform import get_system_info

info = get_system_info()
logger.info("system_info", 
            platform=info.platform,
            python=info.python_version)
```

## Learning Path

1. **Start Here**: [Installation](installation.md) - Set up your environment
2. **Learn Basics**: [Quick Start](quick-start.md) - Core concepts in 5 minutes
3. **Build Something**: [First Application](first-app.md) - Complete working example
4. **Explore More**: [Examples](examples.md) - Real-world use cases
5. **Deep Dive**: [User Guide](../guide/index.md) - Comprehensive documentation

## System Requirements

- Python 3.11 or higher
- No compiled dependencies
- Works on Linux, macOS, and Windows
- Optional: psutil for enhanced system info

## Need Help?

- 📖 Check the [User Guide](../guide/index.md)
- 🔍 Browse the [API Reference](../api/api-index.md)  
- 🏗️ Review the [Architecture](../architecture/index.md)
- 💡 See [Examples](examples.md) for practical patterns

Ready to start? Head to the [Installation Guide](installation.md) →