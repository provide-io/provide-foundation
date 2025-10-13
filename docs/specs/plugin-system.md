# Plugin Architecture Design for provide.foundation

## Executive Summary

The provide.foundation library contains a fully functional plugin discovery system that is currently not automatically invoked. This document outlines the architecture, provides justification for design decisions, and presents a comprehensive plan to enable auto-discovery with dependency injection while maintaining backward compatibility.

### Current State
- **Discovery Implementation**: ✅ Complete and functional
- **Auto-invocation**: ❌ Not enabled
- **Developer Experience**: 4/10 (requires manual registration)
- **Multi-dimensional Registry**: ✅ Unique and powerful

### Proposed State
- **Auto-discovery**: Enabled by default with opt-out
- **Dependency Injection**: Automatic resolution and wiring
- **Developer Experience**: 9/10 (zero-config for common cases)
- **Backward Compatibility**: 100% maintained

## Architecture Analysis

### Current Discovery Implementation

The discovery system in `hub/discovery.py` is fully implemented:

```python
def discover_components(
    group: str,
    dimension: str = "component",
    registry: Registry | None = None,
) -> dict[str, type[Any]]:
    """Discover and register components from entry points."""
```

Key features:
- Uses Python's `importlib.metadata` for entry point discovery
- Supports any dimension in the multi-dimensional registry
- Returns discovered components for further processing
- **Issue**: Never automatically called during Hub initialization

### Multi-dimensional Registry Design

Foundation's registry uses a `(dimension, name)` tuple system:

```python
# Current usage patterns
registry.register("my_logger", logger_class, dimension="component")
registry.register("init", init_command, dimension="command")
registry.register("db", database_resource, dimension="resource")
```

This is **unique** among Python plugin systems and provides:
- Namespace isolation without naming conflicts
- Logical grouping of similar components
- Flexible categorization without rigid hierarchies

### Comparison with Other Plugin Systems

| System | Discovery | Auto-wiring | Multi-dimensional | DX Rating |
|--------|-----------|-------------|-------------------|-----------|
| **pytest** | ✅ Automatic | ✅ Fixtures | ❌ Single namespace | 9/10 |
| **Flask** | ❌ Manual | ❌ Manual | ❌ Single namespace | 7/10 |
| **Django** | ✅ INSTALLED_APPS | ✅ Signals | ❌ Apps only | 8/10 |
| **Sphinx** | ✅ Automatic | ❌ Manual | ✅ Domains | 8/10 |
| **Stevedore** | ✅ Automatic | ❌ Manual | ❌ Single namespace | 6/10 |
| **Poetry** | ✅ Automatic | ❌ Manual | ❌ Groups only | 7/10 |
| **Click** | ❌ Manual | ❌ Manual | ❌ Commands only | 6/10 |
| **Foundation** (current) | ❌ Manual | ❌ Manual | ✅ Full multi-dim | 4/10 |
| **Foundation** (proposed) | ✅ Automatic | ✅ Automatic | ✅ Full multi-dim | 9/10 |

**Key Insight**: Only Sphinx's domain system comes close to Foundation's multi-dimensional approach, but Foundation's is cleaner and more unified.

## Design Decisions

### 1. Dimension Naming Convention

**Decision**: Use short, semantic dimension names without namespacing.

```python
# Recommended ✅
dimension="resource"
dimension="middleware"
dimension="command"

# Not recommended ❌
dimension="pyvider.resource"
dimension="com.example.middleware"
```

**Rationale**:
- Dimensions are categories, not ownership markers
- Provider information belongs in metadata
- Keeps the API clean and intuitive
- Matches current usage patterns

### 2. Auto-discovery vs Manual Registration

**Decision**: Support both with auto-discovery as default.

```python
# Auto-discovery (default)
# Automatically discovered via entry points

# Manual registration (still supported)
hub.registry.register("my_component", MyClass, dimension="component")
```

**Rationale**:
- Progressive enhancement - start manual, go automatic when ready
- No breaking changes for existing code
- Flexibility for dynamic registration
- Testing remains simple

### 3. Entry Point Group Naming

**Decision**: Use `provide.foundation.*` prefix for foundation-specific groups, allow custom groups.

```python
# Standard groups
[tool.poetry.plugins."provide.foundation.components"]
logger = "myapp.logging:CustomLogger"

[tool.poetry.plugins."provide.foundation.commands"]
deploy = "myapp.cli:DeployCommand"

# Custom groups (for specific apps)
[tool.poetry.plugins."pyvider.resources"]
database = "myapp.resources:DatabaseResource"
cache = "myapp.resources.cache:CacheResource"
```

## Implementation Plan

### Phase 1: Enable Auto-discovery in Hub Initialization

Modify `Hub.initialize_foundation()` to automatically discover plugins:

```python
def initialize_foundation(self, config: Any = None, force: bool = False) -> None:
    """Initialize Foundation system through Hub."""
    # Existing initialization
    self._foundation.initialize_foundation(config, force)

    # NEW: Auto-discovery
    if config.get("auto_discover", True):
        self._discover_all_plugins()

def _discover_all_plugins(self) -> None:
    """Discover all registered plugins."""
    standard_groups = [
        ("provide.foundation.components", "component"),
        ("provide.foundation.commands", "command"),
        ("provide.foundation.middleware", "middleware"),
        ("provide.foundation.processors", "processor"),
    ]

    for group, dimension in standard_groups:
        discover_components(group, dimension, self.registry)
```

### Phase 2: Add Dependency Injection System

Create `hub/injection.py`:

```python
from typing import Any, get_type_hints
from provide.foundation.hub.registry import Registry

class InjectionMarker:
    """Marks a field for injection."""
    def __init__(self, name: str | None = None):
        self.name = name

def inject(name: str | None = None) -> Any:
    """Mark a field for dependency injection."""
    return InjectionMarker(name)

class Injector:
    """Handles dependency injection."""

    def __init__(self, registry: Registry):
        self.registry = registry

    def inject_dependencies(self, obj: Any) -> None:
        """Inject dependencies into an object."""
        hints = get_type_hints(obj.__class__)

        for field_name, field_type in hints.items():
            field_value = getattr(obj.__class__, field_name, None)

            if isinstance(field_value, InjectionMarker):
                # Resolve and inject the dependency
                dep_name = field_value.name or field_name
                dependency = self.resolve(dep_name, field_type)
                setattr(obj, field_name, dependency)

    def resolve(self, name: str, expected_type: type) -> Any:
        """Resolve a dependency by name and type."""
        # Try each dimension until we find a match
        for dimension in ["component", "service", "resource"]:
            try:
                value = self.registry.get(name, dimension)
                if value and isinstance(value, expected_type):
                    return value
            except KeyError:
                continue

        raise ValueError(f"Cannot resolve dependency: {name} of type {expected_type}")
```

### Phase 3: Create Plugin Protocols and Lifecycle Hooks

Create `hub/protocols.py`:

```python
from typing import Protocol, Any

class Plugin(Protocol):
    """Base protocol for all plugins."""

    def on_register(self, hub: Any) -> None:
        """Called when plugin is registered."""
        ...

    def on_initialize(self) -> None:
        """Called when plugin is initialized."""
        ...

    def on_shutdown(self) -> None:
        """Called when plugin is shutting down."""
        ...

class ComponentPlugin(Plugin):
    """Protocol for component plugins."""
    pass

class CommandPlugin(Plugin):
    """Protocol for CLI command plugins."""

    def get_command(self) -> Any:
        """Return the Click command."""
        ...

class ResourcePlugin(Plugin):
    """Protocol for resource plugins."""

    def acquire(self) -> Any:
        """Acquire the resource."""
        ...

    def release(self) -> None:
        """Release the resource."""
        ...
```

### Phase 4: Implement Decorator Enhancements

Create `hub/decorators.py`:

```python
from typing import Any, Callable
from provide.foundation.hub import get_hub

def component(
    name: str | None = None,
    dimension: str = "component",
    auto_wire: bool = True,
) -> Callable:
    """Decorator for components."""
    def decorator(cls: type) -> type:
        # Store metadata
        cls._foundation_metadata = {
            "name": name or cls.__name__.lower(),
            "dimension": dimension,
            "auto_wire": auto_wire,
        }

        # Register with hub if available
        try:
            hub = get_hub()
            hub.registry.register(
                cls._foundation_metadata["name"],
                cls,
                dimension=dimension,
            )
        except Exception:
            pass  # Hub not initialized yet, will be discovered later

        return cls
    return decorator

def resource(name: str | None = None) -> Callable:
    """Decorator for resources."""
    return component(name, dimension="resource")

def command(name: str | None = None) -> Callable:
    """Decorator for CLI commands."""
    return component(name, dimension="command")

def middleware(name: str | None = None) -> Callable:
    """Decorator for middleware."""
    return component(name, dimension="middleware")
```

### Phase 5: Add Entry Point Groups

Update `pyproject.toml` to define standard entry point groups:

```toml
# For provide.foundation itself
[tool.poetry.plugins."provide.foundation.components"]
# Components provided by foundation

[tool.poetry.plugins."provide.foundation.commands"]
# Commands provided by foundation

# For consuming projects
[project.entry-points."provide.foundation.components"]
my_logger = "myapp.logging:CustomLogger"

[project.entry-points."provide.foundation.commands"]
deploy = "myapp.cli:deploy"
```

## Integration Examples

### Example 1: pyvider Integration

```python
# pyvider/resources/database.py
from provide.foundation.hub.decorators import resource
from provide.foundation.hub.injection import inject
from provide.foundation.config import Config

@resource("database")
class DatabaseResource:
    """Database connection resource."""

    # Auto-injected dependencies
    config: Config = inject()
    logger: Any = inject("logger")

    def __init__(self):
        # Dependencies already injected
        self.connection = None

    def acquire(self):
        """Acquire database connection."""
        self.logger.info("Connecting to database",
                         host=self.config.db_host)
        # ... connection logic ...
```

```toml
# pyvider's pyproject.toml
[tool.poetry.plugins."provide.foundation.resources"]
database = "pyvider.resources.database:DatabaseResource"
cache = "pyvider.resources.cache:CacheResource"

[tool.poetry.plugins."pyvider.middleware"]
auth = "pyvider.middleware.auth:AuthMiddleware"
```

### Example 2: supsrc Integration

```python
# supsrc/components/supervisor.py
from provide.foundation.hub.decorators import component
from provide.foundation.hub.protocols import ComponentPlugin

@component("supervisor")
class ProcessSupervisor(ComponentPlugin):
    """Process supervision component."""

    def on_initialize(self):
        """Initialize supervisor."""
        self.processes = {}

    def start_process(self, name: str, command: str):
        """Start a supervised process."""
        # ... implementation ...
```

### Example 3: plating Integration

```python
# plating/commands/serve.py
from provide.foundation.hub.decorators import command
import click

@command("serve")
@click.command()
@click.option("--port", default=8000)
def serve(port: int):
    """Serve the plated application."""
    # ... implementation ...
```

## Migration Guide

### Stage 1: Existing Code (No Changes Required)

```python
# Current code continues to work
from provide.foundation.hub import get_hub

hub = get_hub()
hub.registry.register("my_component", MyComponent, dimension="component")
```

### Stage 2: Add Decorators (Optional Enhancement)

```python
# Add decorators for better DX
from provide.foundation.hub.decorators import component

@component("my_component")
class MyComponent:
    pass
```

### Stage 3: Enable Auto-wiring (Progressive Enhancement)

```python
# Use dependency injection
from provide.foundation.hub.injection import inject

@component("my_component")
class MyComponent:
    logger: Logger = inject()
    config: Config = inject()
```

### Stage 4: Entry Points (Full Auto-discovery)

```toml
# Add to pyproject.toml
[tool.poetry.plugins."provide.foundation.components"]
my_component = "myapp.components:MyComponent"
```

## Backward Compatibility Matrix

| Feature | Current Code | With Enhancements |
|---------|--------------|-------------------|
| Manual registration | ✅ Works | ✅ Still works |
| Direct instantiation | ✅ Works | ✅ Still works |
| Custom dimensions | ✅ Works | ✅ Still works |
| Registry access | ✅ Works | ✅ Still works |
| Existing decorators | ✅ Works | ✅ Enhanced |

## Benefits

1. **Zero Configuration**: Plugins work immediately upon installation
2. **Progressive Enhancement**: Start simple, add features as needed
3. **Type Safety**: Full typing support with dependency injection
4. **Testing**: Easy to mock and test with explicit dependencies
5. **Discoverability**: Clear entry points show what's available
6. **Performance**: Lazy loading and efficient resolution
7. **Maintainability**: Less boilerplate, clearer intent

## Trade-offs

1. **Complexity**: More moving parts in the framework
2. **Magic**: Some developers prefer explicit over implicit
3. **Debugging**: Auto-wiring can make flow harder to trace
4. **Learning Curve**: New concepts for developers to learn

## Conclusion

The proposed plugin architecture enhances provide.foundation from a solid but manual framework (4/10 DX) to a best-in-class plugin system (9/10 DX) while maintaining 100% backward compatibility. The multi-dimensional registry remains the unique differentiator, and auto-discovery with dependency injection brings the developer experience up to match the power of the underlying architecture.

The implementation can be done incrementally:
1. **Week 1**: Enable auto-discovery in Hub
2. **Week 2**: Add dependency injection
3. **Week 3**: Create plugin protocols
4. **Week 4**: Implement decorators
5. **Week 5**: Documentation and examples

This positions provide.foundation as the premier choice for Python applications requiring sophisticated plugin architecture with minimal configuration overhead.
