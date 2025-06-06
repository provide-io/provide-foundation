#
# emoji_matrix.py
#
"""
Pyvider Telemetry Emoji Matrix and Display Utilities.

This module is central to the visual and semantic aspect of Domain-Action-Status
(DAS) logging within the `pyvider-telemetry` library. It defines the core
dictionaries that map keywords for "domain", "action", and "status" log event
fields to their corresponding emoji representations. These emojis significantly
improve the scannability and contextual understanding of logs.

Key Components:
- `PRIMARY_EMOJI`: Defines emojis for the 'domain' part of DAS logging,
  representing the primary context or system component of a log event
  (e.g., "system": "⚙️", "database": "🗄️").
- `SECONDARY_EMOJI`: Defines emojis for the 'action' part of DAS logging,
  representing the operation being performed (e.g., "init": "🌱", "read": "📖").
- `TERTIARY_EMOJI`: Defines emojis for the 'status' part of DAS logging,
  representing the outcome or state of the operation (e.g., "success": "✅",
  "failure": "❌").

These emoji mappings are utilized by the `add_das_emoji_prefix` processor in
`custom_processors.py` to prepend a `[D][A][S]` emoji sequence to log messages.

Utility Functions:
- `show_emoji_matrix()`: A helper function that prints the current "emoji contract"
  (all defined DAS emoji mappings) to the console using the telemetry logger.
  This is intended for developer reference and can be activated by setting the
  `PYVIDER_SHOW_EMOJI_MATRIX` environment variable to a truthy value (e.g.,
  "true", "1", "yes").

By centralizing these definitions, this module ensures consistency in emoji usage
across the logging system and provides a clear reference for developers.
"""
import os

from pyvider.telemetry.logger import (
    base as pyvider_logger_base,
)

PRIMARY_EMOJI: dict[str, str] = {
    "system": "⚙️", "server": "🛎️", "client": "🙋", "network": "🌐",
    "security": "🔐", "config": "🔩", "database": "🗄️", "cache": "💾",
    "task": "🔄", "plugin": "🔌", "telemetry": "🛰️", "di": "💉",
    "protocol": "📡", "file": "📄", "user": "👤", "test": "🧪",
    "utils": "🧰", "core": "🌟", "auth": "🔑", "entity": "🦎",
    "report": "📈", "payment": "💳",
    "default": "❓",
}
"""
Emojis for the 'domain' key in Domain-Action-Status (DAS) logging.
Represents the primary context or system component of a log event.
"""

SECONDARY_EMOJI: dict[str, str] = {
    "init": "🌱", "start": "🚀", "stop": "🛑", "connect": "🔗",
    "disconnect": "💔", "listen": "👂", "send": "📤", "receive": "📥",
    "read": "📖", "write": "📝", "process": "⚙️", "validate": "🛡️",
    "execute": "▶️", "query": "🔍", "update": "🔄", "delete": "🗑️",
    "login": "➡️", "logout": "⬅️", "auth": "🔑", "error": "🔥",
    "encrypt": "🛡️", "decrypt": "🔓", "parse": "🧩", "transmit": "📡",
    "build": "🏗️", "schedule": "📅", "emit": "📢", "load": "💡",
    "observe": "🧐", "request": "🗣️", "interrupt": "🚦",
    "register": "⚙️",  # FIXED: Added missing register action
    "default": "❓",  # Default action emoji (unknown or missing action)
}
"""
Emojis for the 'action' key in Domain-Action-Status (DAS) logging.
Represents the operation or activity being performed.
"""

TERTIARY_EMOJI: dict[str, str] = {
    "success": "✅", "failure": "❌", "error": "🔥", "warning": "⚠️",
    "info": "ℹ️",  # noqa: RUF001  -- Intentional use of INFORMATION SOURCE emoji
    "debug": "🐞", "trace": "👣", "attempt": "⏳",
    "retry": "🔁", "skip": "⏭️", "complete": "🏁", "timeout": "⏱️",
    "notfound": "❓", "unauthorized": "🚫", "invalid": "💢", "cached": "🎯",
    "ongoing": "🏃", "idle": "💤", "ready": "👍",
    "default": "➡️",
}
"""
Emojis for the 'status' key in Domain-Action-Status (DAS) logging.
Represents the outcome, result, or state of the operation.
"""

def show_emoji_matrix() -> None: # pragma: no cover
    """
    Prints the Pyvider emoji logging contract (DAS emoji mappings) to the console.

    This utility function is designed for developer reference. It displays the
    current mappings for primary (domain), secondary (action), and tertiary (status)
    emojis used in Domain-Action-Status (DAS) logging.

    The display is activated if the `PYVIDER_SHOW_EMOJI_MATRIX` environment
    variable is set to a truthy value (e.g., "true", "1", "yes").
    The output is logged using a dedicated logger instance
    (`pyvider.telemetry.emoji_matrix_display`) at the INFO level.
    """
    if os.getenv("PYVIDER_SHOW_EMOJI_MATRIX", "false").strip().lower() not in ("true", "1", "yes"):
        return

    matrix_logger = pyvider_logger_base.logger.get_logger("pyvider.telemetry.emoji_matrix_display")
    lines = ["Pyvider Emoji Logging Contract:",
             "  1. Single Prefix (logger name): `EMOJI Your log...`",
             "  2. DAS Prefix (keys): `[D][A][S] Your log...`",
             "="*70, "\nPrimary Emojis (DAS 'domain' key):"]
    lines.extend(f"  {e}  -> {k.capitalize()}" for k, e in PRIMARY_EMOJI.items())
    lines.append("\nSecondary Emojis (DAS 'action' key):")
    lines.extend(f"  {e}  -> {k.capitalize()}" for k, e in SECONDARY_EMOJI.items())
    lines.append("\nTertiary Emojis (DAS 'status' key):")
    lines.extend(f"  {e}  -> {k.capitalize()}" for k, e in TERTIARY_EMOJI.items())
    matrix_logger.info("\n".join(lines))

# 💡🧱
