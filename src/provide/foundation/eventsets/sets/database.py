#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.eventsets.types import EventMapping, EventSet, FieldMapping

"""Database operations event set for Foundation."""

EVENT_SET = EventSet(
    name="database",
    description="Database interaction and query enrichment",
    mappings=[
        EventMapping(
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
            default_key="default",
        ),
        EventMapping(
            name="db_operation",
            visual_markers={
                "query": "🔍",
                "select": "🔍",
                "insert": "+",
                "update": "🔄",
                "delete": "🗑️",
                "connect": "🔗",
                "disconnect": "💔",
                "transaction_begin": "💳🟢",
                "transaction_rollback": "💳❌",
            },
            metadata_fields={
                "select": {"db.read": True},
                "query": {"db.read": True},
                "insert": {"db.write": True},
                "update": {"db.write": True},
                "delete": {"db.write": True},
            },
            default_key="default",
        ),
        EventMapping(
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
            default_key="default",
        ),
    ],
    field_mappings=[
        FieldMapping(
            log_key="db.system",
            event_set_name="database",
            description="Database system type",
            value_type="string",
        ),
        FieldMapping(
            log_key="db.operation",
            event_set_name="database",
            description="Database operation performed",
            value_type="string",
        ),
        FieldMapping(
            log_key="db.outcome",
            event_set_name="database",
            description="Operation outcome",
            value_type="string",
        ),
        FieldMapping(
            log_key="db.statement",
            event_set_name="database",
            description="SQL or query statement",
            value_type="string",
        ),
        FieldMapping(
            log_key="db.table",
            event_set_name="database",
            description="Table name",
            value_type="string",
            default_override_key="default",
        ),
        FieldMapping(
            log_key="db.rows_affected",
            event_set_name="database",
            description="Number of rows affected",
            value_type="integer",
        ),
        FieldMapping(
            log_key="duration_ms",
            event_set_name="database",
            description="Query duration in milliseconds",
            value_type="integer",
        ),
        FieldMapping(
            log_key="trace_id",
            event_set_name="database",
            description="Distributed trace ID",
            value_type="string",
        ),
    ],
    priority=90,
)

# 🧱🏗️🔚
