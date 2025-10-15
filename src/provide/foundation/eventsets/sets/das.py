# provide/foundation/eventsets/sets/das.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.eventsets.types import EventMapping, EventSet, FieldMapping

"""Domain-Action-Status (DAS) event set."""

EVENT_SET = EventSet(
    name="default",
    description="Core Domain-Action-Status event enrichment",
    mappings=[
        EventMapping(
            name="domain",
            visual_markers={
                "system": "⚙️",
                "server": "🛎️",
                "client": "🙋",
                "network": "🌐",
                "security": "🔐",
                "config": "🔩",
                "database": "🗄️",
                "cache": "💾",
                "task": "🔄",
                "plugin": "🔌",
                "telemetry": "🛰️",
                "di": "💉",
                "protocol": "📡",
                "file": "📄",
                "user": "👤",
                "test": "🧪",
                "utils": "🧰",
                "core": "🌟",
                "auth": "🔑",
                "entity": "🦎",
                "report": "📈",
                "payment": "💳",
                "default": "❓",
            },
            default_key="default",
        ),
        EventMapping(
            name="action",
            visual_markers={
                "init": "🌱",
                "start": "🚀",
                "stop": "🛑",
                "connect": "🔗",
                "disconnect": "💔",
                "listen": "👂",
                "send": "📤",
                "receive": "📥",
                "read": "📖",
                "write": "📝",
                "process": "⚙️",
                "validate": "🛡️",
                "execute": "▶️",
                "query": "🔍",
                "update": "🔄",
                "delete": "🗑️",
                "login": "➡️",
                "logout": "⬅️",
                "auth": "🔑",
                "error": "🔥",
                "encrypt": "🛡️",
                "decrypt": "🔓",
                "parse": "🧩",
                "transmit": "📡",
                "build": "🏗️",
                "schedule": "📅",
                "emit": "📢",
                "load": "💡",
                "observe": "🧐",
                "request": "🗣️",
                "interrupt": "🚦",
                "register": "⚙️",
                "default": "❓",
            },
            default_key="default",
        ),
        EventMapping(
            name="status",
            visual_markers={
                "success": "✅",
                "failure": "❌",
                "error": "🔥",
                "warning": "⚠️",
                "info": "i",
                "debug": "🐞",
                "trace": "👣",
                "attempt": "⏳",
                "retry": "🔁",
                "skip": "⏭️",
                "complete": "🏁",
                "timeout": "⏱️",
                "notfound": "❓",
                "unauthorized": "🚫",
                "invalid": "💢",
                "cached": "🎯",
                "ongoing": "🏃",
                "idle": "💤",
                "ready": "👍",
                "default": "➡️",
            },
            default_key="default",
        ),
    ],
    field_mappings=[
        FieldMapping(
            log_key="domain",
            event_set_name="default",
            description="System domain or component",
        ),
        FieldMapping(
            log_key="action",
            event_set_name="default",
            description="Action being performed",
        ),
        FieldMapping(
            log_key="status",
            event_set_name="default",
            description="Status or outcome of the action",
        ),
    ],
    priority=0,
)


# <3 🧱🤝📊🪄
