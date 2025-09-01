"""
Provide Foundation Hub - Unified Registry System
=================================================

A multi-dimensional registry system for components and CLI commands.
Allows tools to register and discover components dynamically.
"""

from .registry import Registry, RegistryDimension
from .decorators import register_component, register_command, register
from .hub import Hub, get_hub

__all__ = [
    "Registry",
    "RegistryDimension", 
    "register_component",
    "register_command",
    "register",
    "Hub",
    "get_hub",
]