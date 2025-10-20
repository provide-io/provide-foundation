# Spec: Plugin Architecture Design

This document outlines the architecture for enabling auto-discovery and dependency injection for plugins within `provide.foundation`.

## Overview

The goal is to evolve the existing `Registry` into a fully-featured plugin system with zero-configuration for common cases, while maintaining 100% backward compatibility.

## Proposed State
- **Auto-discovery**: Enabled by default via entry points.
- **Dependency Injection**: Automatic resolution of registered components.
- **Developer Experience**: Move from manual registration to a declarative, "it-just-works" model.

## Implementation Plan

1.  **Enable Auto-discovery in Hub:** The `Hub` will be modified to automatically scan for `provide.foundation.components` and other standard entry point groups during initialization.
2.  **Add Dependency Injection System:** A lightweight `Injector` will be created to resolve dependencies for registered components based on type hints.
3.  **Implement Decorator Enhancements:** Decorators like `@component`, `@resource`, and `@command` will be introduced to simplify registration and metadata attachment.

## Example: Plugin Definition

```python
# my_plugin/components.py
from provide.foundation.hub.decorators import component
from provide.foundation.hub.injection import inject

@component("my_custom_component")
class MyCustomComponent:
    logger: Logger = inject()
    config: AppConfig = inject()

    def run(self):
        self.logger.info("Custom component running!")
```

```toml
# my_plugin/pyproject.toml
[project.entry-points."provide.foundation.components"]
my_component = "my_plugin.components:MyCustomComponent"
```
