"""
Domain-Action-Status (DAS) event set.
"""

from provide.foundation.eventsets.types import EventMapping, EventSet, FieldMapping

EVENT_SET = EventSet(
    name="das",
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
            default_key="default"
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
            default_key="default"
        ),
        EventMapping(
            name="status",
            visual_markers={
                "success": "✅",
                "failure": "❌",
                "error": "🔥",
                "warning": "⚠️",
                "info": "ℹ️",
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
            default_key="default"
        ),
    ],
    field_mappings=[
        FieldMapping(
            log_key="domain",
            description="System domain or component",
            event_set_name="domain"
        ),
        FieldMapping(
            log_key="action",
            description="Action being performed",
            event_set_name="action"
        ),
        FieldMapping(
            log_key="status",
            description="Status or outcome of the action",
            event_set_name="status"
        ),
    ],
    priority=0
)