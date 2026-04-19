# Getting Started with provide.foundation

Welcome to provide.foundation! This section will guide you through installation and your first application in just a few minutes.

## What is provide.foundation?

provide.foundation is a comprehensive Python library for building robust, production-focused applications with:

- **Structured Logging**: Beautiful, performant logging with zero configuration
- **CLI Framework**: Build command-line tools with declarative commands
- **Configuration**: Environment-based configuration without hardcoded defaults
- **Resilience**: Retry patterns, error handling, and failure recovery
- **Utilities**: File operations, cryptography, serialization, and more

## Quick Navigation

<div class="getting-started-grid">
  <div class="getting-started-card">
    <h3>📦 Installation</h3>
    <p>Install Foundation and configure your environment</p>
    <p><a href="installation/">Start Here →</a></p>
  </div>
  <div class="getting-started-card">
    <h3>⚡ Quick Start</h3>
    <p>Write your first Foundation application in 5 minutes</p>
    <p><a href="quick-start/">Get Coding →</a></p>
  </div>
  <div class="getting-started-card">
    <h3>🏗️ First Application</h3>
    <p>Build a complete CLI task manager</p>
    <p><a href="first-app/">Build Something →</a></p>
  </div>
  <div class="getting-started-card">
    <h3>💡 Examples</h3>
    <p>Explore code examples for all features</p>
    <p><a href="examples/">See Examples →</a></p>
  </div>
</div>

## Learning Path

We recommend following this path:

1. **[Installation](installation.md)** - Set up your environment (2 minutes)
1. **[Quick Start](quick-start.md)** - Write your first logs (5 minutes)
1. **[First Application](first-app.md)** - Build a CLI tool (15 minutes)
1. **[Examples](examples.md)** - Explore specific features (ongoing)

After completing these, dive into the [How-To Guides](../how-to-guides/logging/basic-logging.md) for specific use cases.

## System Requirements

- Python 3.11 or higher
- Works on Linux, macOS, and Windows
- Minimal core dependencies (`structlog`, `attrs`)

## Optional Features

Foundation has modular installation options:

| Feature            | Install Command                            | When You Need It               |
| ------------------ | ------------------------------------------ | ------------------------------ |
| **Basic logging**  | `uv add provide-foundation`                | Core functionality             |
| **CLI framework**  | `uv add provide-foundation[cli]`           | Building command-line tools    |
| **Cryptography**   | `uv add provide-foundation[crypto]`        | Hashing, signing, certificates |
| **HTTP Transport** | `uv add provide-foundation[transport]`     | HTTP client utilities          |
| **OpenTelemetry**  | `uv add provide-foundation[opentelemetry]` | Distributed tracing            |
| **All features**   | `uv add provide-foundation[all]`           | Everything above               |

## Need Help?

- **Documentation:** Browse the [How-To Guides](../how-to-guides/logging/basic-logging.md) and [Explanation](../explanation/architecture.md) sections
- **Examples:** Check the [Examples](examples.md) for working code
- **Issues:** Report bugs on [GitHub Issues](https://github.com/provide-io/provide-foundation/issues)

______________________________________________________________________

Ready to begin? Start with [Installation](installation.md) →
