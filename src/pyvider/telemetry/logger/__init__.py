#
# __init__.py
#
"""
Pyvider Telemetry Logger Sub-package.

This `__init__.py` serves as the public entry point for the `pyvider.telemetry.logger`
sub-package. It re-exports key components related to the actual logging
functionality, making them easily accessible for users who need to interact
directly with the logger or its associated utilities.

Key Exports:
- `logger`: The primary, pre-configured `PyviderLogger` instance for application-wide
  logging. This is the most common import from this sub-package.
- `PyviderLogger`: The class definition for the logger, useful for type hinting
  or if users need to understand the logger's structure (though direct
  instantiation by client code is generally not required).
- Emoji Utilities:
    - `PRIMARY_EMOJI`, `SECONDARY_EMOJI`, `TERTIARY_EMOJI`: Dictionaries
      mapping keywords to emojis for Domain-Action-Status (DAS) structured logging.
    - `show_emoji_matrix`: A utility function to display the current emoji
      contract to the console, aiding developers in using DAS emojis correctly.

This sub-package encapsulates the logger's implementation details (like the base
logger and custom processors) while exposing a clean interface here. Users typically
import `logger` from `pyvider.telemetry` (which re-exports it from here), but direct
imports from `pyvider.telemetry.logger` are available for more specific needs or
for accessing logger-specific utilities not promoted to the top-level package.
"""
from pyvider.telemetry.logger.base import (
    PyviderLogger,
    logger,
)
from pyvider.telemetry.logger.emoji_matrix import (
    PRIMARY_EMOJI,
    SECONDARY_EMOJI,
    TERTIARY_EMOJI,
    show_emoji_matrix,
)

__all__ = [
    "PRIMARY_EMOJI",
    "SECONDARY_EMOJI",
    "TERTIARY_EMOJI",
    "PyviderLogger",
    "logger",
    "show_emoji_matrix",
]

# 🐍📝
