"""
Provide Namespace Package.

Provides easy access to common foundation components:
- logger: Foundation logging system
- config: Foundation configuration system
"""

# Core imports for convenience
from provide.foundation import config, logger

__all__ = [
    "config",
    "logger",
]
