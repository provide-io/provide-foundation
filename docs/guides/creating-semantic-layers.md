# 🧑‍💻 Guides

## Creating Custom Semantic Layers

One of the most powerful features of `provide.foundation` is its extensible Semantic Layer system. While the built-in layers are useful, the true power comes from creating layers tailored to your application's specific domain. This guide will walk you through the process of creating a custom semantic layer from scratch.

For this tutorial, we will create a semantic layer for a **CI/CD pipeline**. Our goal is to create a logging standard for build and deployment jobs.

### Step 1: Plan Your Layer

First, we need to define the "schema" for our logging events. What information is important for a CI/CD job?

*   **Domain**: `cicd`
*   **Key Fields**:
    *   `cicd.pipeline.name`: The name of the pipeline (e.g., `"production-api"`).
    *   `cicd.job.name`: The name of the job within the pipeline (e.g., `"build"`, `"test"`, `"deploy"`). This will be one of our emoji-generating fields.
    *   `cicd.job.outcome`: The result of the job (e.g., `"success"`, `"failure"`, `"cancelled"`). This will also generate an emoji.
    *   `cicd.commit.hash`: The git commit hash being processed.
*   **Emoji Mappings**:
    *   **Job Name**: `build` -> `🏗️`, `test` -> `🧪`, `deploy` -> `🚀`
    *   **Job Outcome**: `success` -> `✅`, `failure` -> `❌`, `cancelled` -> `🛑`

### Step 2: Define Your Emoji Sets

An emoji set is a named dictionary that maps specific values to emojis. We need to create one for `cicd.job.name` and one for `cicd.job.outcome`.

```python
from provide.foundation import CustomDasEmojiSet

# Emoji set for the job name
cicd_job_emojis = CustomDasEmojiSet(
    name="cicd_job_name_emojis",
    emojis={
        "build": "🏗️",
        "test": "🧪",
        "deploy": "🚀",
        "default": "⚙️", # A fallback for any other job name
    }
)

# Emoji set for the job outcome
cicd_outcome_emojis = CustomDasEmojiSet(
    name="cicd_job_outcome_emojis",
    emojis={
        "success": "✅",
        "failure": "❌",
        "cancelled": "🛑",
        "default": "➡️", # A fallback for any other outcome
    }
)
```

### Step 3: Define Your Semantic Fields

A semantic field defines a single key in your layer's schema. Here, we link our log keys (e.g., `cicd.job.name`) to the emoji sets we just created.

```python
from provide.foundation import SemanticFieldDefinition

cicd_fields = [
    # This field will use our job name emoji set
    SemanticFieldDefinition(
        log_key="cicd.job.name",
        description="The name of the CI/CD job.",
        emoji_set_name="cicd_job_name_emojis",
    ),
    # This field will use our job outcome emoji set
    SemanticFieldDefinition(
        log_key="cicd.job.outcome",
        description="The outcome of the CI/CD job.",
        emoji_set_name="cicd_job_outcome_emojis",
    ),
    # These fields provide context but do not generate emojis
    SemanticFieldDefinition(
        log_key="cicd.pipeline.name",
        description="The name of the parent pipeline.",
    ),
    SemanticFieldDefinition(
        log_key="cicd.commit.hash",
        description="The git commit hash.",
    ),
]
```

### Step 4: Create the Semantic Layer

Now, we assemble the pieces into a single `SemanticLayer` object.

```python
from provide.foundation import SemanticLayer

cicd_layer = SemanticLayer(
    name="cicd",
    description="Semantic conventions for CI/CD pipeline events.",
    # Include the emoji sets we defined
    emoji_sets=[cicd_job_emojis, cicd_outcome_emojis],
    # Include the field definitions
    field_definitions=cicd_fields,
)
```

### Step 5: Enable the Custom Layer

To activate our new layer, we pass it to the `LoggingConfig` during setup.

```python
from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig

config = TelemetryConfig(
    logging=LoggingConfig(
        # Add our custom layer to this list
        custom_semantic_layers=[cicd_layer]
    )
)

setup_telemetry(config)
```

### Step 6: Use Your New Layer!

Your custom semantic layer is now active. You can log events using the keys you defined, and `provide.foundation` will automatically add the correct emoji prefixes.

```python
from provide.foundation import logger

# Example 1: A successful build job
logger.info(
    "Build job completed successfully",
    **{
        "cicd.pipeline.name": "production-api",
        "cicd.job.name": "build",
        "cicd.job.outcome": "success",
        "cicd.commit.hash": "a1b2c3d",
    }
)

# Example 2: A failed deployment job
logger.error(
    "Deployment to production failed",
    **{
        "cicd.pipeline.name": "production-api",
        "cicd.job.name": "deploy",
        "cicd.job.outcome": "failure",
        "cicd.commit.hash": "a1b2c3d",
        "error_message": "Connection to server timed out",
    }
)
```

**Output:**

```
[🏗️][✅] Build job completed successfully cicd.pipeline.name=production-api cicd.commit.hash=a1b2c3d
[🚀][❌] Deployment to production failed cicd.pipeline.name=production-api cicd.commit.hash=a1b2c3d error_message='Connection to server timed out'
```

Congratulations! You have successfully created and used a custom semantic layer, extending `provide.foundation` to perfectly fit your application's domain.

---

With the guides complete, it's time to dive into the details in the [**API Reference**](../api-reference/logger.md).
