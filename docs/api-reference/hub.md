# 📚 API Reference

## Hub

This section provides a detailed reference for the Foundation Hub, a system for managing components and CLI commands.

### The `Hub` Class

The `Hub` class is the main manager that coordinates all components and commands.

::: provide.foundation.hub.manager.Hub
    options:
      members:
        - add_component
        - get_component
        - list_components
        - discover_components
        - add_command
        - get_command
        - list_commands
        - create_cli

---

### Decorators

The most common way to register components and commands is via decorators.

#### `@register_component`

::: provide.foundation.hub.components.register_component

#### `@register_command`

::: provide.foundation.hub.commands.register_command

---

### Global Instance

A global `Hub` instance can be easily accessed.

::: provide.foundation.hub.manager.get_hub
