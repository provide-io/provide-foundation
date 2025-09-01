# 📚 API Reference

## Semantic Layers API

This document provides a detailed reference for the data classes used to create custom semantic layers. For a practical tutorial on how to use these, see the [**Creating Custom Semantic Layers**](../guides/creating-semantic-layers.md) guide.

### `SemanticLayer`

This is the main data class that defines a complete semantic logging convention for a specific domain.

```python
@define(frozen=True, slots=True)
class SemanticLayer:
    name: str
    description: str | None = None
    emoji_sets: list[CustomDasEmojiSet] = field(factory=list)
    field_definitions: list[SemanticFieldDefinition] = field(factory=list)
    priority: int = 0
```

*   **`name`** (`str`)
    *   **Description**: A unique name for the layer (e.g., `"http"`, `"database"`, `"cicd"`). This name is used to enable the layer in the configuration.

*   **`description`** (`str` | `None`)
    *   **Description**: A human-readable description of the layer's purpose.

*   **`emoji_sets`** (`list[CustomDasEmojiSet]`)
    *   **Description**: A list of `CustomDasEmojiSet` objects that this layer uses. These sets define the mappings from log values to emojis.

*   **`field_definitions`** (`list[SemanticFieldDefinition]`)
    *   **Description**: A list of `SemanticFieldDefinition` objects that define the schema of the layer. The order of this list is important, as it determines the order of the emojis in the semantic prefix.

*   **`priority`** (`int`)
    *   **Description**: A number used to resolve conflicts if multiple active layers define a field for the same `log_key`. The layer with the higher priority will take precedence. Not typically needed for most use cases.

### `SemanticFieldDefinition`

This data class defines a single structured log key within a `SemanticLayer`.

```python
@define(frozen=True, slots=True)
class SemanticFieldDefinition:
    log_key: str
    description: str | None = None
    value_type: str | None = None
    emoji_set_name: str | None = None
```

*   **`log_key`** (`str`)
    *   **Description**: The key to look for in the log event's `kwargs` (e.g., `"http.method"`, `"cicd.job.outcome"`). Using a dot-separated namespace is a recommended convention.

*   **`description`** (`str` | `None`)
    *   **Description**: A human-readable description of what this field represents.

*   **`value_type`** (`str` | `None`)
    *   **Description**: The expected type of the field's value (e.g., `"string"`, `"int"`). This is currently for documentation purposes but may be used for validation in the future.

*   **`emoji_set_name`** (`str` | `None`)
    *   **Description**: The `name` of the `CustomDasEmojiSet` to use for finding an emoji for this key's value. If this is `None`, this field will be included as context in the log, but it will not contribute to the semantic emoji prefix.

### `CustomDasEmojiSet`

This data class defines a named collection of emojis mapped to specific string values. It is the fundamental building block for generating semantic emoji prefixes.

```python
@define(frozen=True, slots=True)
class CustomDasEmojiSet:
    name: str
    emojis: dict[str, str]
    default_emoji_key: str = "default"
```

*   **`name`** (`str`)
    *   **Description**: A unique name for the set (e.g., `"http_method_emojis"`, `"job_outcome_emojis"`). This name is referenced by `SemanticFieldDefinition.emoji_set_name`.

*   **`emojis`** (`dict[str, str]`)
    *   **Description**: A dictionary mapping a specific log value (e.g., `"GET"`, `"success"`) to an emoji (e.g., `"➡️"`, `"✅"`).

*   **`default_emoji_key`** (`str`)
    *   **Description**: The key within the `emojis` dictionary to use as a fallback if the logged value is not found in the dictionary. It is highly recommended to always include a `"default"` key in your `emojis` dictionary and leave this as `"default"`.

---

Next, learn about the utility functions available in the [**Utilities API**](./utils.md).
