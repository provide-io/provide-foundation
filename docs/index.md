# Welcome to the Provide Foundation

**The Provide Foundation** is a comprehensive Python 3.11+ library for building robust, operationally excellent applications. It provides a cohesive, "batteries-included" toolkit that addresses common challenges in modern application development.

Built on industry-standard libraries like `structlog`, `click`, and `attrs`, `provide.foundation` offers a superior developer experience with beautiful console output, powerful error handling, and cross-platform system utilities.

## Why provide.foundation?

| For Developers | For Teams |
| :--- | :--- |
| ✅ **Zero Configuration**: Works beautifully out of the box. | 🤝 **Consistent**: Standardized patterns across all services. |
| ✅ **Type Safe**: Full type hints and runtime validation. | 🔭 **Observable**: Structured logs ready for analysis. |
| ✅ **Fast**: Optimized for production (>14,000 msg/sec). | 🛠️ **Maintainable**: Clean, well-documented APIs. |
| ✅ **Testable**: Built-in testing utilities and patterns. | 🧩 **Extensible**: Plugin system for customization. |

## Learning Path

This documentation is structured to help you learn effectively, whether you're a beginner or an expert.

<div class="feature-grid">
  <div class="feature-card">
    <h3>🎓 Tutorials</h3>
    <p>Step-by-step lessons to get you started. Perfect for new users.</p>
    <a href="tutorials/01-quick-start.md">Start Learning →</a>
  </div>
  <div class="feature-card">
    <h3>📖 How-To Guides</h3>
    <p>Practical, goal-oriented recipes to solve specific problems.</p>
    <a href="how-to-guides/logging/basic-logging.md">Solve a Problem →</a>
  </div>
  <div class="feature-card">
    <h3>🧠 Explanation</h3>
    <p>Deep dives into the concepts and architecture behind the framework.</p>
    <a href="explanation/architecture.md">Understand the "Why" →</a>
  </div>
  <div class="feature-card">
    <h3>📚 API Reference</h3>
    <p>Detailed technical descriptions of every class, method, and function.</p>
    <a href="reference/index.md">Look It Up →</a>
  </div>
</div>

## Quick Example

```python
from provide.foundation import logger, pout, get_hub
from provide.foundation.hub import register_command
from provide.foundation.resilience import retry
from provide.foundation.errors import NetworkError

# Initialize the framework (optional - logger auto-initializes on first use)
# For advanced configuration:
# get_hub().initialize_foundation()

# Structured logging with event enrichment
logger.info("application_startup", version="1.0.0", emoji="🚀")

# User-facing console output
pout("✅ Configuration loaded successfully.", color="green")

# Resilient functions
@retry(max_attempts=3, exceptions=(NetworkError,))
def fetch_data_from_api():
    logger.info("api_call_start", endpoint="/data", emoji="📡")
    # ... API call logic that might fail ...
    # if failed:
    #     raise NetworkError("API is unavailable")
    logger.info("api_call_complete", status=200, emoji="✅")

# Declarative CLI commands
@register_command("process")
def process_data(file: str, force: bool = False):
    """Process the given data file."""
    pout(f"Processing {file} with force={force}...")
    fetch_data_from_api()
```

## System Requirements

-   Python 3.11 or higher
-   Works on Linux, macOS, and Windows
-   Minimal core dependencies (`structlog`, `attrs`, `click`)

---

Ready to get started? Head to the **[Quick Start Tutorial](tutorials/01-quick-start.md)**.
