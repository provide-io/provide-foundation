#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.eventsets.types import EventMapping, EventSet, FieldMapping

"""HTTP request/response event set for Foundation."""

EVENT_SET = EventSet(
    name="http",
    description="HTTP client and server interaction enrichment",
    mappings=[
        EventMapping(
            name="http_method",
            visual_markers={
                "get": "📥",
                "post": "📤",
                "put": "📝⬆️",
                "delete": "🗑️",
                "patch": "🩹",
                "head": "👤❔",
                "default": "🌐",
            },
            default_key="default",
        ),
        EventMapping(
            name="http_status_class",
            visual_markers={
                "1xx": "i",
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
            default_key="default",
        ),
        EventMapping(
            name="http_target_type",
            visual_markers={
                "path": "🛣️",
                "query": "❓",
                "fragment": "#️⃣",
                "default": "🎯",
            },
            default_key="default",
        ),
    ],
    field_mappings=[
        FieldMapping(
            log_key="http.method",
            event_set_name="http",
            description="HTTP request method",
            value_type="string",
        ),
        FieldMapping(
            log_key="http.status_class",
            event_set_name="http",
            description="HTTP status code class",
            value_type="string",
        ),
        FieldMapping(
            log_key="http.target",
            event_set_name="http",
            description="Request target path and query",
            value_type="string",
            default_override_key="path",
        ),
        FieldMapping(
            log_key="http.url",
            event_set_name="http",
            description="Full HTTP URL",
            value_type="string",
        ),
        FieldMapping(
            log_key="http.scheme",
            event_set_name="http",
            description="URL scheme",
            value_type="string",
        ),
        FieldMapping(
            log_key="http.host",
            event_set_name="http",
            description="Request hostname",
            value_type="string",
        ),
        FieldMapping(
            log_key="http.status_code",
            event_set_name="http",
            description="HTTP response status code",
            value_type="integer",
        ),
        FieldMapping(
            log_key="http.request.body.size",
            event_set_name="http",
            description="Request body size in bytes",
            value_type="integer",
        ),
        FieldMapping(
            log_key="http.response.body.size",
            event_set_name="http",
            description="Response body size in bytes",
            value_type="integer",
        ),
        FieldMapping(
            log_key="client.address",
            event_set_name="http",
            description="Client IP address",
            value_type="string",
        ),
        FieldMapping(
            log_key="server.address",
            event_set_name="http",
            description="Server address or hostname",
            value_type="string",
        ),
        FieldMapping(
            log_key="duration_ms",
            event_set_name="http",
            description="Request duration in milliseconds",
            value_type="integer",
        ),
        FieldMapping(
            log_key="trace_id",
            event_set_name="http",
            description="Distributed trace ID",
            value_type="string",
        ),
        FieldMapping(
            log_key="span_id",
            event_set_name="http",
            description="Span ID",
            value_type="string",
        ),
        FieldMapping(
            log_key="error.message",
            event_set_name="http",
            description="Error message if request failed",
            value_type="string",
        ),
        FieldMapping(
            log_key="error.type",
            event_set_name="http",
            description="Error type if request failed",
            value_type="string",
        ),
    ],
    priority=80,
)

# 🧱🏗️🔚
