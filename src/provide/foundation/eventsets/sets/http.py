"""
HTTP request/response event set for Foundation.
"""

from provide.foundation.eventsets.types import EventSet, EventSetConfig, FieldMapping

EVENT_SET = EventSetConfig(
    name="http",
    description="HTTP client and server interaction enrichment",
    event_sets=[
        EventSet(
            name="http_method",
            visual_markers={
                "get": "📥",
                "post": "📤",
                "put": "📝⬆️",
                "delete": "🗑️",
                "patch": "🩹",
                "head": "👤❔",
                "options": "⚙️❔",
                "default": "🌐",
            },
            default_key="default"
        ),
        EventSet(
            name="http_status_class",
            visual_markers={
                "1xx": "ℹ️",
                "2xx": "✅",
                "3xx": "↪️",
                "4xx": "⚠️CLIENT",
                "5xx": "🔥SERVER",
                "default": "❓",
            },
            metadata_fields={
                "2xx": {"http.success": True},
                "4xx": {"http.client_error": True},
                "5xx": {"http.server_error": True},
            },
            default_key="default"
        ),
        EventSet(
            name="http_target_type",
            visual_markers={
                "path": "🛣️",
                "query": "❓",
                "fragment": "#️⃣",
                "default": "🎯",
            },
            default_key="default"
        ),
    ],
    field_mappings=[
        FieldMapping(
            log_key="http.method",
            description="HTTP request method",
            value_type="string",
            event_set_name="http_method"
        ),
        FieldMapping(
            log_key="http.status_class",
            description="HTTP status code class",
            value_type="string",
            event_set_name="http_status_class"
        ),
        FieldMapping(
            log_key="http.target",
            description="Request target path and query",
            value_type="string",
            event_set_name="http_target_type",
            default_override_key="path"
        ),
        FieldMapping(
            log_key="http.url",
            description="Full HTTP URL",
            value_type="string"
        ),
        FieldMapping(
            log_key="http.scheme",
            description="URL scheme",
            value_type="string"
        ),
        FieldMapping(
            log_key="http.host",
            description="Request hostname",
            value_type="string"
        ),
        FieldMapping(
            log_key="http.status_code",
            description="HTTP response status code",
            value_type="integer"
        ),
        FieldMapping(
            log_key="http.request.body.size",
            description="Request body size in bytes",
            value_type="integer"
        ),
        FieldMapping(
            log_key="http.response.body.size",
            description="Response body size in bytes",
            value_type="integer"
        ),
        FieldMapping(
            log_key="client.address",
            description="Client IP address",
            value_type="string"
        ),
        FieldMapping(
            log_key="server.address",
            description="Server address or hostname",
            value_type="string"
        ),
        FieldMapping(
            log_key="duration_ms",
            description="Request duration in milliseconds",
            value_type="integer"
        ),
        FieldMapping(
            log_key="trace_id",
            description="Distributed trace ID",
            value_type="string"
        ),
        FieldMapping(
            log_key="span_id",
            description="Span ID",
            value_type="string"
        ),
        FieldMapping(
            log_key="error.message",
            description="Error message if request failed",
            value_type="string"
        ),
        FieldMapping(
            log_key="error.type",
            description="Error type if request failed",
            value_type="string"
        ),
    ],
    priority=80
)