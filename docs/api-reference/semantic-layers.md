# 📚 API Reference

## Semantic Layers

This section provides a detailed reference for the data classes used to create custom semantic layers.

For a practical tutorial on how to use these, see the [**Creating Custom Semantic Layers**](../guides/creating-semantic-layers.md) guide.

---

### `SemanticLayer`

This is the main data class that defines a complete semantic logging convention for a specific domain.

::: provide.foundation.semantic_layers.SemanticLayer
    options:
      show_root_heading: false

---

### `SemanticFieldDefinition`

This data class defines a single structured log key within a `SemanticLayer`.

::: provide.foundation.semantic_layers.SemanticFieldDefinition
    options:
      show_root_heading: false

---

### `CustomDasEmojiSet`

This data class defines a named collection of emojis mapped to specific string values.

::: provide.foundation.semantic_layers.CustomDasEmojiSet
    options:
      show_root_heading: false

---

### Built-in Layers

The following semantic layers are built-in and can be enabled by name in the `LoggingConfig`.

*   `llm`: For Large Language Model interactions.
*   `database`: For database interactions.
*   `http`: For HTTP client and server interactions.
*   `task_queue`: For asynchronous task queue operations.

```python
from provide.foundation import LoggingConfig

# Example of enabling built-in layers
config = LoggingConfig(enabled_semantic_layers=["http", "database"])
```