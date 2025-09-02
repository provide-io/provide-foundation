# 🏛️ Core Concepts

## The Emoji System: Visual Log Parsing

A key feature of `provide.foundation` is its automatic use of emojis to add visual context to logs. This system is designed to make your console output instantly scannable, allowing you to quickly identify a log's origin and meaning without having to read the entire line.

There are two types of emoji prefixes that can be added to a log message:

1.  **Logger Name Prefix**: Identifies *where* the log is from.
2.  **Semantic Prefix**: Identifies *what* the log is about.

### 1. Logger Name Prefix

Every named logger has a unique, deterministic emoji associated with it. This emoji is generated from a hash of the logger's name.

This means that a logger named `"database.connections"` will *always* have the same emoji prefix, and it will be different from the emoji for a logger named `"api.v1.users"`.

**Example:**

```python
from provide.foundation import logger

# Get two different named loggers
db_logger = logger.get_logger("database.connections")
api_logger = logger.get_logger("api.v1.users")

# Log messages from each
db_logger.info("Connection pool initialized")
api_logger.info("User lookup request received")
```

**Output:**

```
[🗄️] Connection pool initialized
[🙋] User lookup request received
```

As you can see, you can immediately distinguish between logs from the database component and the API component just by looking at the emoji.

This feature is enabled by default but can be disabled via configuration if desired.

### 2. Semantic Prefix

The second set of emojis is determined by the *content* of the log message. This prefix is generated in one of two ways:

*   **From a Semantic Layer**: If the log event contains keys that match an active [Semantic Layer](./semantic-layers.md), the layer defines which emojis to use based on the values of those keys.

    ```python
    # Assuming the 'http' layer is active
    logger.info("Request handled", **{"http.method": "POST", "http.status_code": 201})
    # Output: [📤][✅] Request handled
    ```

*   **From the DAS Fallback**: If no semantic layer matches, the system looks for the `domain`, `action`, and `status` keyword arguments.

    ```python
    logger.info("Task complete", domain="task", action="execute", status="success")
    # Output: [🔄][▶️][✅] Task complete
    ```

### The Combined Prefix

When both systems are active, the prefixes are combined to provide a rich visual summary of the log event:

```
[Logger Emoji][Semantic Emoji 1][Semantic Emoji 2] Log message...
```

**Example:**

```python
from provide.foundation import logger

# Get a named logger
auth_logger = logger.get_logger("auth.service")

# Log a semantic event
auth_logger.info(
    "User successfully logged out",
    domain="auth",
    action="logout",
    status="success",
)
```

**Output:**

```
[🔑][⬅️][✅] User successfully logged out
```

Here, the `[🔑]` is the semantic emoji for `domain="auth"`, and the `[⬅️][✅]` are the semantic emojis for `action="logout"` and `status="success"`. (Note: In this case, the logger name `auth.service` also hashes to `🔑`, demonstrating the deterministic nature of the system).

### Viewing the Emoji Matrix

To help you understand which emojis correspond to which semantic meanings, you can view the complete "emoji matrix" for the currently active configuration.

Set the following environment variable before running your application:

```bash
export FOUNDATION_SHOW_EMOJI_MATRIX=true
```

When your application starts, it will print a detailed reference table of all active emoji mappings for the DAS (Domain-Action-Status) system and any enabled Semantic Layers.

This is an invaluable tool for learning the emoji vocabulary and for designing your own custom semantic layers.

---

Next, learn how to tailor the logger's behavior in [**Configuration**](./configuration.md).
