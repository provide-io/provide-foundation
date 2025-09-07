"""
Database operations event set for Foundation.
"""

from provide.foundation.eventsets.types import EventSet, EventSetConfig, FieldMapping

EVENT_SET = EventSetConfig(
    name="database",
    description="Database interaction and query enrichment",
    event_sets=[
        EventSet(
            name="db_system",
            visual_markers={
                "postgres": "🐘",
                "mysql": "🐬",
                "sqlite": "💾",
                "mongodb": "🍃",
                "redis": "🟥",
                "elasticsearch": "🔍",
                "default": "🗄️",
            },
            metadata_fields={
                "postgres": {"db.type": "sql", "db.vendor": "postgresql"},
                "mysql": {"db.type": "sql", "db.vendor": "mysql"},
                "sqlite": {"db.type": "sql", "db.vendor": "sqlite"},
                "mongodb": {"db.type": "nosql", "db.vendor": "mongodb"},
                "redis": {"db.type": "cache", "db.vendor": "redis"},
                "elasticsearch": {"db.type": "search", "db.vendor": "elastic"},
            },
            default_key="default"
        ),
        EventSet(
            name="db_operation",
            visual_markers={
                "query": "🔍",
                "select": "🔍",
                "insert": "➕",
                "update": "🔄",
                "delete": "🗑️",
                "connect": "🔗",
                "disconnect": "💔",
                "transaction_begin": "💳🟢",
                "transaction_commit": "💳✅",
                "transaction_rollback": "💳❌",
                "default": "⚙️",
            },
            metadata_fields={
                "select": {"db.read": True},
                "query": {"db.read": True},
                "insert": {"db.write": True},
                "update": {"db.write": True},
                "delete": {"db.write": True},
            },
            default_key="default"
        ),
        EventSet(
            name="db_outcome",
            visual_markers={
                "success": "👍",
                "error": "🔥",
                "not_found": "❓🤷",
                "timeout": "⏱️",
                "default": "➡️",
            },
            metadata_fields={
                "success": {"db.success": True},
                "error": {"db.error": True},
                "timeout": {"db.timeout": True},
            },
            default_key="default"
        ),
    ],
    field_mappings=[
        FieldMapping(
            log_key="db.system",
            description="Database system type",
            value_type="string",
            event_set_name="db_system"
        ),
        FieldMapping(
            log_key="db.operation",
            description="Database operation performed",
            value_type="string",
            event_set_name="db_operation"
        ),
        FieldMapping(
            log_key="db.outcome",
            description="Operation outcome",
            value_type="string",
            event_set_name="db_outcome"
        ),
        FieldMapping(
            log_key="db.statement",
            description="SQL or query statement",
            value_type="string"
        ),
        FieldMapping(
            log_key="db.table",
            description="Table name",
            value_type="string",
            event_set_name="db_system",
            default_override_key="default"
        ),
        FieldMapping(
            log_key="db.rows_affected",
            description="Number of rows affected",
            value_type="integer"
        ),
        FieldMapping(
            log_key="duration_ms",
            description="Query duration in milliseconds",
            value_type="integer"
        ),
        FieldMapping(
            log_key="trace_id",
            description="Distributed trace ID",
            value_type="string"
        ),
    ],
    priority=90
)