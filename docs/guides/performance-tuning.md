# 🧑‍💻 Guides

## Performance Tuning Guide

`provide.foundation` is engineered for high performance and is suitable for production use out of the box. Our benchmarks show that it can process tens of thousands of log messages per second. However, in ultra-high-throughput or resource-constrained environments, you can apply several strategies to optimize its performance even further.

### 1. Set the Right Log Level in Production

This is the single most important performance optimization you can make.

By default, the log level is `DEBUG`. While this is great for development, it can create significant overhead in production if many `DEBUG` messages are being written.

Logging at a higher level (like `INFO` or `WARNING`) means that lower-level log calls (like `logger.debug()`) return almost instantly, without performing any expensive formatting or I/O operations.

**Recommendation:** In production, set your default log level to `INFO` or `WARNING`.

```bash
# In your production environment
export FOUNDATION_LOG_LEVEL="INFO"
```

Or programmatically:

```python
from provide.foundation import LoggingConfig

config = LoggingConfig(default_level="INFO")
```

### 2. Use Module-Level Filtering

Sometimes, a specific library or component in your application is overly "chatty," producing a large volume of logs that you don't need. Instead of raising the global log level, you can selectively silence noisy modules.

**Recommendation:** Use module-level filtering to set a higher log level for specific, noisy components.

```bash
# Silence a noisy library while keeping your app's logs at DEBUG
export FOUNDATION_LOG_MODULE_LEVELS="noisy_library:WARNING,another_lib.utils:ERROR"
```

Or programmatically:

```python
config = LoggingConfig(
    default_level="DEBUG",
    module_levels={
        "noisy_library": "WARNING",
        "another_lib.utils": "ERROR",
    }
)
```

### 3. Use the JSON Formatter

If your logs are primarily intended for consumption by a log aggregation service (like Datadog, Splunk, or an ELK stack), using the JSON formatter can be more efficient.

*   It avoids the string formatting overhead of the `key_value` formatter.
*   It produces output that can be ingested much more efficiently by downstream systems.

**Recommendation:** For production services that log to a central collector, use the `json` formatter.

```bash
export FOUNDATION_LOG_CONSOLE_FORMATTER="json"
```

### 4. Disabling Emojis

The emoji generation system is highly optimized, but it does introduce a small amount of overhead. In extreme performance-critical scenarios, you can disable one or both emoji prefix systems.

*   **Logger Name Emoji**: This involves a hashing operation and a dictionary lookup, which is then cached. The overhead is minimal after the first call for a given logger name.
*   **Semantic Emoji**: This involves dictionary lookups based on the log's context.

**Recommendation:** Only consider this if you have benchmarked your application and identified logging as a bottleneck. The visual benefits of emojis often outweigh the microsecond-level performance cost.

```bash
# Disable the logger-name-based emoji
export FOUNDATION_LOG_LOGGER_NAME_EMOJI_ENABLED="false"

# Disable the semantic (DAS or Layer-based) emoji
export FOUNDATION_LOG_DAS_EMOJI_ENABLED="false"
```

### Internal Optimizations to Be Aware Of

`provide.foundation` already includes several internal optimizations, so you don't have to worry about them:

*   **Lazy Initialization**: The logger only performs its full setup the first time it is used, minimizing import-time side effects.
*   **Logger Name Emoji Caching**: The emoji for each named logger is cached after the first lookup, making subsequent calls extremely fast.
*   **Early Filtering**: Log level filtering happens early in the processing chain, ensuring that suppressed messages have a near-zero performance cost.

By applying these strategies, you can ensure that your logging is not only beautiful and informative but also highly performant, even under the most demanding production loads.

---

Next, learn how to extend the library's core functionality in the [**Creating Custom Semantic Layers**](./creating-semantic-layers.md) guide.
