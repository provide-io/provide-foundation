#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.eventsets.types import EventMapping, EventSet, FieldMapping

"""Task queue and async job processing event set for Foundation."""

EVENT_SET = EventSet(
    name="task_queue",
    description="Asynchronous task queue operation enrichment",
    mappings=[
        EventMapping(
            name="task_system",
            visual_markers={
                "celery": "🥕",
                "rq": "🟥🇶",
                "dramatiq": "🎭",
                "rabbitmq": "🐇",
                "default": "📨",
            },
            metadata_fields={
                "celery": {"task.broker": "celery"},
                "rq": {"task.broker": "redis"},
                "dramatiq": {"task.broker": "dramatiq"},
                "kafka": {"task.broker": "kafka", "task.streaming": True},
                "rabbitmq": {"task.broker": "amqp"},
            },
            default_key="default",
        ),
        EventMapping(
            name="task_status",
            visual_markers={
                "submitted": "➡️📨",
                "received": "📥",
                "started": "▶️",
                "progress": "🔄",
                "retrying": "🔁",
                "failure": "❌🔥",
                "revoked": "🚫",
                "default": "❓",
            },
            metadata_fields={
                "submitted": {"task.state": "pending"},
                "received": {"task.state": "pending"},
                "started": {"task.state": "active"},
                "progress": {"task.state": "active"},
                "retrying": {"task.state": "retry"},
                "success": {"task.state": "completed", "task.success": True},
                "failure": {"task.state": "failed", "task.success": False},
                "revoked": {"task.state": "cancelled"},
            },
            default_key="default",
        ),
    ],
    field_mappings=[
        FieldMapping(
            log_key="task.system",
            event_set_name="task_queue",
            description="Task queue system",
            value_type="string",
        ),
        FieldMapping(
            log_key="task.status",
            event_set_name="task_queue",
            description="Task execution status",
            value_type="string",
        ),
        FieldMapping(
            log_key="task.id",
            event_set_name="task_queue",
            description="Unique task identifier",
            value_type="string",
        ),
        FieldMapping(
            log_key="task.name",
            event_set_name="task_queue",
            description="Task or job name",
            value_type="string",
        ),
        FieldMapping(
            log_key="task.queue_name",
            event_set_name="task_queue",
            description="Queue name",
            value_type="string",
        ),
        FieldMapping(
            log_key="task.retries",
            event_set_name="task_queue",
            description="Retry attempt count",
            value_type="integer",
        ),
        FieldMapping(
            log_key="duration_ms",
            event_set_name="task_queue",
            description="Task execution duration",
            value_type="integer",
        ),
        FieldMapping(
            log_key="trace_id",
            event_set_name="task_queue",
            description="Distributed trace ID",
            value_type="string",
        ),
    ],
    priority=70,
)

# 🧱🏗️🔚
