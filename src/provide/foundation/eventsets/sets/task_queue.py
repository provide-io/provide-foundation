"""
Task queue and async job processing event set for Foundation.
"""

from provide.foundation.eventsets.types import EventSet, EventSetConfig, FieldMapping

EVENT_SET = EventSetConfig(
    name="task_queue",
    description="Asynchronous task queue operation enrichment",
    event_sets=[
        EventSet(
            name="task_system",
            visual_markers={
                "celery": "🥕",
                "rq": "🟥🇶",
                "dramatiq": "🎭",
                "kafka": "🌊",
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
            default_key="default"
        ),
        EventSet(
            name="task_status",
            visual_markers={
                "submitted": "➡️📨",
                "received": "📥",
                "started": "▶️",
                "progress": "🔄",
                "retrying": "🔁",
                "success": "✅🏁",
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
            default_key="default"
        ),
    ],
    field_mappings=[
        FieldMapping(
            log_key="task.system",
            description="Task queue system",
            value_type="string",
            event_set_name="task_system"
        ),
        FieldMapping(
            log_key="task.status",
            description="Task execution status",
            value_type="string",
            event_set_name="task_status"
        ),
        FieldMapping(
            log_key="task.id",
            description="Unique task identifier",
            value_type="string"
        ),
        FieldMapping(
            log_key="task.name",
            description="Task or job name",
            value_type="string"
        ),
        FieldMapping(
            log_key="task.queue_name",
            description="Queue name",
            value_type="string"
        ),
        FieldMapping(
            log_key="task.retries",
            description="Retry attempt count",
            value_type="integer"
        ),
        FieldMapping(
            log_key="duration_ms",
            description="Task execution duration",
            value_type="integer"
        ),
        FieldMapping(
            log_key="trace_id",
            description="Distributed trace ID",
            value_type="string"
        ),
    ],
    priority=70
)