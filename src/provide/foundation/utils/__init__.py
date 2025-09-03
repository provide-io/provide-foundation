"""
Utility modules for provide.foundation.

Common utilities that can be used across the foundation and by other packages.
"""

from provide.foundation.utils.parsing import (
    auto_parse,
    parse_bool,
    parse_dict,
    parse_list,
    parse_typed_value,
)
from provide.foundation.utils.timing import timed_block
from provide.foundation.utils.env import (
    get_bool,
    get_int,
    get_float,
    get_str,
    get_path,
    get_list,
    get_dict,
    require,
    EnvPrefix,
    parse_duration,
    parse_size,
)
from provide.foundation.utils.formatting import (
    format_size,
    format_duration,
    format_number,
    format_percentage,
    truncate,
    pluralize,
    indent,
    wrap_text,
    strip_ansi,
    to_snake_case,
    to_kebab_case,
    to_camel_case,
    format_table,
)

__all__ = [
    # Parsing utilities
    "auto_parse",
    "parse_bool",
    "parse_dict",
    "parse_list",
    "parse_typed_value",
    # Timing utilities
    "timed_block",
    # Environment utilities
    'get_bool',
    'get_int',
    'get_float',
    'get_str',
    'get_path',
    'get_list',
    'get_dict',
    'require',
    'EnvPrefix',
    'parse_duration',
    'parse_size',
    # Formatting utilities
    'format_size',
    'format_duration',
    'format_number',
    'format_percentage',
    'truncate',
    'pluralize',
    'indent',
    'wrap_text',
    'strip_ansi',
    'to_snake_case',
    'to_kebab_case',
    'to_camel_case',
    'format_table',
]
