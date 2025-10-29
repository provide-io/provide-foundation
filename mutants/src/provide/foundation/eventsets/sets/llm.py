# provide/foundation/eventsets/sets/llm.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.eventsets.types import EventMapping, EventSet, FieldMapping

"""Large Language Model (LLM) interaction event set for Foundation."""

EVENT_SET = EventSet(
    name="llm",
    description="LLM provider and interaction enrichment",
    mappings=[
        EventMapping(
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
            default_key="default",
        ),
        EventMapping(
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
            default_key="default",
        ),
        EventMapping(
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
            default_key="default",
        ),
    ],
    field_mappings=[
        FieldMapping(
            log_key="llm.provider",
            event_set_name="llm",
            description="LLM provider name",
            value_type="string",
        ),
        FieldMapping(
            log_key="llm.task",
            event_set_name="llm",
            description="LLM task type",
            value_type="string",
        ),
        FieldMapping(
            log_key="llm.model",
            event_set_name="llm",
            description="Model identifier",
            value_type="string",
        ),
        FieldMapping(
            log_key="llm.outcome",
            event_set_name="llm",
            description="Operation outcome",
            value_type="string",
        ),
        FieldMapping(
            log_key="llm.input.tokens",
            event_set_name="llm",
            description="Input token count",
            value_type="integer",
        ),
        FieldMapping(
            log_key="llm.output.tokens",
            event_set_name="llm",
            description="Output token count",
            value_type="integer",
        ),
        FieldMapping(
            log_key="llm.tool.name",
            event_set_name="llm",
            description="Tool/function name",
            value_type="string",
        ),
        FieldMapping(
            log_key="llm.tool.call_id",
            event_set_name="llm",
            description="Tool call identifier",
            value_type="string",
        ),
        FieldMapping(
            log_key="duration_ms",
            event_set_name="llm",
            description="LLM operation duration",
            value_type="integer",
        ),
        FieldMapping(
            log_key="trace_id",
            event_set_name="llm",
            description="Distributed trace ID",
            value_type="string",
        ),
    ],
    priority=100,  # High priority for LLM operations
)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


# <3 🧱🤝📊🪄
