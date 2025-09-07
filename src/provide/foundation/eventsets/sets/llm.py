"""
Large Language Model (LLM) interaction event set for Foundation.
"""

from provide.foundation.eventsets.types import EventSet, EventSetConfig, FieldMapping

EVENT_SET = EventSetConfig(
    name="llm",
    description="LLM provider and interaction enrichment",
    event_sets=[
        EventSet(
            name="llm_provider",
            visual_markers={
                "openai": "🤖",
                "anthropic": "📚",
                "google": "🇬",
                "meta": "🦙",
                "mistral": "🌬️",
                "perplexity": "❓",
                "cohere": "🔊",
                "default": "💡",
            },
            metadata_fields={
                "openai": {"llm.vendor": "openai", "llm.api": "openai"},
                "anthropic": {"llm.vendor": "anthropic", "llm.api": "claude"},
                "google": {"llm.vendor": "google", "llm.api": "gemini"},
                "meta": {"llm.vendor": "meta", "llm.api": "llama"},
                "mistral": {"llm.vendor": "mistral", "llm.api": "mistral"},
            },
            default_key="default"
        ),
        EventSet(
            name="llm_task",
            visual_markers={
                "generation": "✍️",
                "completion": "✅",
                "embedding": "🔗",
                "chat": "💬",
                "tool_use": "🛠️",
                "summarization": "📜",
                "translation": "🌐",
                "classification": "🏷️",
                "default": "⚡",
            },
            metadata_fields={
                "generation": {"llm.type": "generative"},
                "completion": {"llm.type": "completion"},
                "embedding": {"llm.type": "embedding"},
                "chat": {"llm.type": "conversational"},
                "tool_use": {"llm.type": "function_calling"},
            },
            default_key="default"
        ),
        EventSet(
            name="llm_outcome",
            visual_markers={
                "success": "👍",
                "error": "🔥",
                "filtered_input": "🛡️👁️",
                "filtered_output": "🛡️🗣️",
                "rate_limit": "⏳",
                "partial_success": "🤏",
                "tool_call": "📞",
                "default": "➡️",
            },
            metadata_fields={
                "success": {"llm.success": True},
                "error": {"llm.error": True},
                "rate_limit": {"llm.rate_limited": True},
                "filtered_input": {"llm.filtered": True, "llm.filter_type": "input"},
                "filtered_output": {"llm.filtered": True, "llm.filter_type": "output"},
            },
            default_key="default"
        ),
    ],
    field_mappings=[
        FieldMapping(
            log_key="llm.provider",
            description="LLM provider name",
            value_type="string",
            event_set_name="llm_provider"
        ),
        FieldMapping(
            log_key="llm.task",
            description="LLM task type",
            value_type="string",
            event_set_name="llm_task"
        ),
        FieldMapping(
            log_key="llm.model",
            description="Model identifier",
            value_type="string",
            event_set_name="llm_provider"
        ),
        FieldMapping(
            log_key="llm.outcome",
            description="Operation outcome",
            value_type="string",
            event_set_name="llm_outcome"
        ),
        FieldMapping(
            log_key="llm.input.tokens",
            description="Input token count",
            value_type="integer"
        ),
        FieldMapping(
            log_key="llm.output.tokens",
            description="Output token count",
            value_type="integer"
        ),
        FieldMapping(
            log_key="llm.tool.name",
            description="Tool/function name",
            value_type="string"
        ),
        FieldMapping(
            log_key="llm.tool.call_id",
            description="Tool call identifier",
            value_type="string"
        ),
        FieldMapping(
            log_key="duration_ms",
            description="LLM operation duration",
            value_type="integer"
        ),
        FieldMapping(
            log_key="trace_id",
            description="Distributed trace ID",
            value_type="string"
        ),
    ],
    priority=100  # High priority for LLM operations
)