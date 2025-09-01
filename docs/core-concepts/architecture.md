# 🏛️ Core Concepts

## System Architecture

To best understand how `provide.foundation` works, it's helpful to visualize the journey of a log message from the moment it's created to when it's written to the console. The library uses a pipeline of "processors," where each processor is a function that adds, removes, or modifies data in the log event dictionary.

### The Logging Processor Chain

The diagram below illustrates the standard processor chain. When you call a function like `logger.info()`, an event dictionary is created and passed through this pipeline sequentially.

```mermaid
graph TD
    subgraph "Your Code"
        A[logger.info("User logged in", user_id=123)]
    end

    subgraph "Core Processors"
        B(add_log_level)
        C(add_logger_name)
        D(add_das_emoji_prefix)
        E(add_logger_name_emoji_prefix)
    end

    subgraph "Standard structlog Processors"
        F(TimeStamper)
        G(format_exc_info)
    end

    subgraph "Formatter / Renderer"
        H{Console or JSON?}
        I[KeyValueRenderer]
        J[JSONRenderer]
    end

    subgraph "Final Output"
        K([Formatted Log Message])
    end

    A --> B --> C --> D --> E --> F --> G --> H
    H -- key_value --> I --> K
    H -- json --> J --> K
```

### Breakdown of the Stages

1.  **Your Code**: You call a logging method with a message and structured key-value pairs.
2.  **Core Processors**: This is where `provide.foundation` adds its unique value:
    *   `add_log_level`: Adds the log level (e.g., `info`, `warning`) to the event.
    *   `add_logger_name`: Adds the logger's name (e.g., `database.connections`).
    *   `add_das_emoji_prefix`: This is the semantic processor. It inspects the event for keys matching active **Semantic Layers** or the **DAS** (`domain`, `action`, `status`) pattern and prepends the corresponding emojis.
    *   `add_logger_name_emoji_prefix`: Prepends the unique emoji associated with the logger's name.
3.  **Standard `structlog` Processors**: Common processors for adding standard information like timestamps and formatting exception tracebacks.
4.  **Formatter / Renderer**: This is the final step that serializes the event dictionary into a string. Based on your configuration, it will use either the human-readable `KeyValueRenderer` or the machine-readable `JSONRenderer`.
5.  **Final Output**: The formatted string is written to the console.

Understanding this flow is key to creating custom processors or debugging logging behavior in complex scenarios.
