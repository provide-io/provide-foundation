"""
Utility modules for provide.foundation.

Common utilities that can be used across the foundation and by other packages.
"""

from provide.foundation.utils.deps import (
    DependencyStatus,
    check_optional_deps,
    get_available_features,
    get_optional_dependencies,
    has_dependency,
    require_dependency,
)
from provide.foundation.utils.env import (
    EnvPrefix,
    get_bool,
    get_dict,
    get_float,
    get_int,
    get_list,
    get_path,
    get_str,
    parse_duration,
    parse_size,
    require,
)
from provide.foundation.utils.formatting import (
    format_duration,
    format_number,
    format_percentage,
    format_size,
    format_table,
    indent,
    pluralize,
    strip_ansi,
    to_camel_case,
    to_kebab_case,
    to_snake_case,
    truncate,
    wrap_text,
)
from provide.foundation.utils.parsing import (
    auto_parse,
    parse_bool,
    parse_dict,
    parse_list,
    parse_typed_value,
)
from provide.foundation.utils.rate_limiting import TokenBucketRateLimiter
from provide.foundation.utils.timing import timed_block

__all__ = [
    "EnvPrefix",
    # Parsing utilities
    "auto_parse",
    # Dependency checking utilities
    "check_optional_deps",
    "DependencyStatus",
    "format_duration",
    "format_number",
    "format_percentage",
    # Formatting utilities
    "format_size",
    "format_table",
    "get_available_features",
    # Environment utilities
    "get_bool",
    "get_dict",
    "get_float",
    "get_int",
    "get_list",
    "get_optional_dependencies",
    "get_path",
    "get_str",
    "has_dependency",
    "indent",
    "parse_bool",
    "parse_dict",
    "parse_duration",
    "parse_list",
    "parse_size",
    "parse_typed_value",
    "pluralize",
    "require",
    "require_dependency",
    "strip_ansi",
    # Timing utilities
    "timed_block",
    "to_camel_case",
    # Rate limiting utilities
    "TokenBucketRateLimiter",
    "to_kebab_case",
    "to_snake_case",
    "truncate",
    "wrap_text",
]
