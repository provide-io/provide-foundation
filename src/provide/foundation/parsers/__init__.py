#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.parsers.attrs_integration import (
    _extract_field_type,
    _resolve_string_type,
    _try_converter,
    auto_parse,
)
from provide.foundation.parsers.collections import (
    parse_comma_list,
    parse_dict,
    parse_list,
    parse_set,
    parse_tuple,
)
from provide.foundation.parsers.errors import (
    _VALID_FORMATTER_TUPLE,
    _VALID_FOUNDATION_LOG_OUTPUT_TUPLE,
    _VALID_LOG_LEVEL_TUPLE,
    _VALID_OVERFLOW_POLICY_TUPLE,
    _format_invalid_value_error,
    _format_validation_error,
)
from provide.foundation.parsers.primitives import (
    parse_bool,
    parse_bool_extended,
    parse_bool_strict,
    parse_float_with_validation,
    parse_json_dict,
    parse_json_list,
    parse_sample_rate,
)
from provide.foundation.parsers.structured import (
    parse_headers,
    parse_module_levels,
    parse_rate_limits,
)
from provide.foundation.parsers.telemetry import (
    parse_console_formatter,
    parse_foundation_log_output,
    parse_log_level,
)
from provide.foundation.parsers.typed import (
    _parse_basic_type,
    _parse_generic_type,
    _parse_list_type,
    _parse_set_type,
    _parse_tuple_type,
    extract_concrete_type,
    parse_typed_value,
)

"""Unified parsing package for provide.foundation.

Consolidates all parsing logic into a single top-level package:
- Primitive type parsing (bool, int, float, str, JSON)
- Collection parsing (list, dict, tuple, set)
- Type-aware parsing with generics support
- Attrs field integration
- Domain-specific parsers (telemetry, structured config)

All parsers are accessible via a unified import:
    from provide.foundation.parsers import parse_bool, parse_typed_value, auto_parse
"""

__all__ = [
    # Error utilities
    "_VALID_FORMATTER_TUPLE",
    "_VALID_FOUNDATION_LOG_OUTPUT_TUPLE",
    "_VALID_LOG_LEVEL_TUPLE",
    "_VALID_OVERFLOW_POLICY_TUPLE",
    "_extract_field_type",
    "_format_invalid_value_error",
    "_format_validation_error",
    "_parse_basic_type",
    "_parse_generic_type",
    "_parse_list_type",
    "_parse_set_type",
    "_parse_tuple_type",
    "_resolve_string_type",
    "_try_converter",
    # Attrs integration
    "auto_parse",
    # Type-aware parsing
    "extract_concrete_type",
    # Primitives
    "parse_bool",
    "parse_bool_extended",
    "parse_bool_strict",
    # Collections
    "parse_comma_list",
    "parse_console_formatter",
    "parse_dict",
    "parse_float_with_validation",
    # Domain-specific parsers
    "parse_foundation_log_output",
    "parse_headers",
    "parse_json_dict",
    "parse_json_list",
    "parse_list",
    "parse_log_level",
    "parse_module_levels",
    "parse_rate_limits",
    "parse_sample_rate",
    "parse_set",
    "parse_tuple",
    "parse_typed_value",
]

# 🧱🏗️🔚
