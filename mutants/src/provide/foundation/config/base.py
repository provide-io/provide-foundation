# provide/foundation/config/base.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Base configuration classes and utilities."""

from __future__ import annotations

from collections.abc import Callable
import copy
from typing import Any, Self, TypeVar

from attrs import NOTHING, Attribute, define, field as attrs_field, fields

from provide.foundation.config.types import ConfigDict, ConfigSource

T = TypeVar("T", bound="BaseConfig")
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


def x_field__mutmut_orig(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_1(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = True,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_2(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = None

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_3(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata and {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_4(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = None
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_5(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["XXdescriptionXX"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_6(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["DESCRIPTION"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_7(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = None
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_8(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["XXenv_varXX"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_9(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["ENV_VAR"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_10(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = None
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_11(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["XXenv_prefixXX"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_12(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["ENV_PREFIX"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_13(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = None

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_14(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["XXsensitiveXX"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_15(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["SENSITIVE"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_16(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_17(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=None,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_18(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=None,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_19(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=None,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_20(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=None,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_21(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_22(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_23(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_24(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_25(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_26(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=None,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_27(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=None,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_28(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=None,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_29(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=None,
        **kwargs,
    )


def x_field__mutmut_30(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        validator=validator,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_31(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        converter=converter,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_32(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        metadata=config_metadata,
        **kwargs,
    )


def x_field__mutmut_33(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        **kwargs,
    )


def x_field__mutmut_34(
    *,
    default: Any = NOTHING,
    factory: Callable[[], Any] | None = None,
    validator: Callable[[Any, Attribute[Any], Any], None] | None = None,
    converter: Callable[[Any], Any] | None = None,
    metadata: dict[str, Any] | None = None,
    description: str | None = None,
    env_var: str | None = None,
    env_prefix: str | None = None,
    sensitive: bool = False,
    **kwargs: Any,
) -> Any:
    """Enhanced attrs field with configuration-specific metadata.

    Args:
        default: Default value for the field
        factory: Factory function to generate default value
        validator: Validation function
        converter: Conversion function
        metadata: Additional metadata
        description: Human-readable description
        env_var: Environment variable name override
        env_prefix: Prefix for environment variable
        sensitive: Whether this field contains sensitive data
        **kwargs: Additional attrs field arguments

    """
    config_metadata = metadata or {}

    # Add configuration-specific metadata
    if description:
        config_metadata["description"] = description
    if env_var:
        config_metadata["env_var"] = env_var
    if env_prefix:
        config_metadata["env_prefix"] = env_prefix
    if sensitive:
        config_metadata["sensitive"] = sensitive

    # Handle factory vs default
    if factory is not None:
        return attrs_field(
            factory=factory,
            validator=validator,
            converter=converter,
            metadata=config_metadata,
            **kwargs,
        )
    return attrs_field(
        default=default,
        validator=validator,
        converter=converter,
        metadata=config_metadata,
    )


x_field__mutmut_mutants: ClassVar[MutantDict] = {
    "x_field__mutmut_1": x_field__mutmut_1,
    "x_field__mutmut_2": x_field__mutmut_2,
    "x_field__mutmut_3": x_field__mutmut_3,
    "x_field__mutmut_4": x_field__mutmut_4,
    "x_field__mutmut_5": x_field__mutmut_5,
    "x_field__mutmut_6": x_field__mutmut_6,
    "x_field__mutmut_7": x_field__mutmut_7,
    "x_field__mutmut_8": x_field__mutmut_8,
    "x_field__mutmut_9": x_field__mutmut_9,
    "x_field__mutmut_10": x_field__mutmut_10,
    "x_field__mutmut_11": x_field__mutmut_11,
    "x_field__mutmut_12": x_field__mutmut_12,
    "x_field__mutmut_13": x_field__mutmut_13,
    "x_field__mutmut_14": x_field__mutmut_14,
    "x_field__mutmut_15": x_field__mutmut_15,
    "x_field__mutmut_16": x_field__mutmut_16,
    "x_field__mutmut_17": x_field__mutmut_17,
    "x_field__mutmut_18": x_field__mutmut_18,
    "x_field__mutmut_19": x_field__mutmut_19,
    "x_field__mutmut_20": x_field__mutmut_20,
    "x_field__mutmut_21": x_field__mutmut_21,
    "x_field__mutmut_22": x_field__mutmut_22,
    "x_field__mutmut_23": x_field__mutmut_23,
    "x_field__mutmut_24": x_field__mutmut_24,
    "x_field__mutmut_25": x_field__mutmut_25,
    "x_field__mutmut_26": x_field__mutmut_26,
    "x_field__mutmut_27": x_field__mutmut_27,
    "x_field__mutmut_28": x_field__mutmut_28,
    "x_field__mutmut_29": x_field__mutmut_29,
    "x_field__mutmut_30": x_field__mutmut_30,
    "x_field__mutmut_31": x_field__mutmut_31,
    "x_field__mutmut_32": x_field__mutmut_32,
    "x_field__mutmut_33": x_field__mutmut_33,
    "x_field__mutmut_34": x_field__mutmut_34,
}


def field(*args, **kwargs):
    result = _mutmut_trampoline(x_field__mutmut_orig, x_field__mutmut_mutants, args, kwargs)
    return result


field.__signature__ = _mutmut_signature(x_field__mutmut_orig)
x_field__mutmut_orig.__name__ = "x_field"


@define(slots=True, repr=False)
class BaseConfig:
    """Base configuration class with common functionality.

    All configuration classes should inherit from this.

    Note on Validation:
        The validate() method is synchronous. Subclasses can override it to add
        custom validation logic. If async validation is needed, subclasses should
        implement their own async validation methods.
    """

    # These are instance attributes that need to be defined outside of slots
    _source_map: dict[str, ConfigSource] = attrs_field(init=False, factory=dict)
    _original_values: dict[str, Any] = attrs_field(init=False, factory=dict)

    def __attrs_post_init__(self) -> None:
        """Post-initialization hook for subclasses.

        Note: validate() is not called automatically to allow subclasses
        to perform validation at the appropriate time (e.g., after all
        fields are populated from multiple sources).
        """
        # The _source_map and _original_values are now handled by attrs with factory

    def validate(self) -> None:
        """Validate the configuration.

        This is a synchronous validation method. Override this in subclasses
        to add custom validation logic. Call this explicitly after creating
        and populating a configuration instance.

        Raises:
            ValidationError: If validation fails

        """

    def to_dict(self, include_sensitive: bool = False) -> ConfigDict:
        """Convert configuration to dictionary.

        Args:
            include_sensitive: Whether to include sensitive fields

        Returns:
            Dictionary representation of the configuration

        """
        result = {}

        for attr in fields(self.__class__):
            value = getattr(self, attr.name)

            # Skip sensitive fields if requested
            if not include_sensitive and attr.metadata.get("sensitive", False):
                continue

            # Convert nested configs recursively
            if isinstance(value, BaseConfig):
                value = value.to_dict(include_sensitive)
            elif isinstance(value, dict):
                value = self._convert_dict_values(value, include_sensitive)
            elif isinstance(value, list):
                value = self._convert_list_values(value, include_sensitive)

            result[attr.name] = value

        return result

    def _convert_dict_values(self, d: dict[str, Any], include_sensitive: bool) -> dict[str, Any]:
        """Convert dictionary values recursively."""
        result = {}
        for key, value in d.items():
            if isinstance(value, BaseConfig):
                value = value.to_dict(include_sensitive)
            elif isinstance(value, dict):
                value = self._convert_dict_values(value, include_sensitive)
            elif isinstance(value, list):
                value = self._convert_list_values(value, include_sensitive)
            result[key] = value
        return result

    def _convert_list_values(self, lst: list[Any], include_sensitive: bool) -> list[Any]:
        """Convert list values recursively."""
        result = []
        for value in lst:
            if isinstance(value, BaseConfig):
                value = value.to_dict(include_sensitive)
            elif isinstance(value, dict):
                value = self._convert_dict_values(value, include_sensitive)
            elif isinstance(value, list):
                value = self._convert_list_values(value, include_sensitive)
            result.append(value)
        return result

    @classmethod
    def from_dict(cls, data: ConfigDict, source: ConfigSource = ConfigSource.RUNTIME) -> Self:
        """Create configuration from dictionary.

        Args:
            data: Configuration data
            source: Source of the configuration

        Returns:
            Configuration instance

        Raises:
            ValidationError: If validation fails

        """
        # Filter data to only include fields defined in the class, excluding private fields
        field_names = {f.name for f in fields(cls) if not f.name.startswith("_")}
        filtered_data = {k: v for k, v in data.items() if k in field_names}

        # Create instance
        instance = cls(**filtered_data)

        # Track sources
        for key in filtered_data:
            instance._source_map[key] = source
            instance._original_values[key] = filtered_data[key]

        # Validate configuration
        instance.validate()

        return instance

    def update(self, updates: ConfigDict, source: ConfigSource = ConfigSource.RUNTIME) -> None:
        """Update configuration with new values.

        Args:
            updates: Dictionary of updates
            source: Source of the updates

        Raises:
            ValidationError: If validation fails after update

        """
        for key, value in updates.items():
            if hasattr(self, key):
                # Only update if new source has higher precedence
                current_source = self._source_map.get(key, ConfigSource.DEFAULT)
                if source >= current_source:
                    setattr(self, key, value)
                    self._source_map[key] = source
                    self._original_values[key] = value

        # Validate configuration after updates
        self.validate()

    def get_source(self, field_name: str) -> ConfigSource | None:
        """Get the source of a configuration field.

        Args:
            field_name: Name of the field

        Returns:
            Source of the field value or None

        """
        return self._source_map.get(field_name)

    def reset_to_defaults(self) -> None:
        """Reset all fields to their default values."""
        for attr in fields(self.__class__):
            # Skip internal fields
            if attr.name.startswith("_"):
                continue

            if attr.default != NOTHING:
                setattr(self, attr.name, attr.default)
            elif attr.factory != NOTHING:
                # attrs factory is always callable
                setattr(self, attr.name, attr.factory())

        self._source_map.clear()
        self._original_values.clear()

        # Note: validate() should be called separately if validation is needed after reset

    def clone(self) -> Self:
        """Create a deep copy of the configuration."""
        cloned = copy.deepcopy(self)
        # Cloned configuration inherits validation state from original
        return cloned

    def diff(self, other: BaseConfig) -> dict[str, tuple[Any, Any]]:
        """Compare with another configuration.

        Args:
            other: Configuration to compare with

        Returns:
            Dictionary of differences (field_name: (self_value, other_value))

        """
        if not isinstance(other, self.__class__):
            raise TypeError(f"Cannot compare {self.__class__.__name__} with {other.__class__.__name__}")

        differences = {}

        for attr in fields(self.__class__):
            self_value = getattr(self, attr.name)
            other_value = getattr(other, attr.name)

            if self_value != other_value:
                differences[attr.name] = (self_value, other_value)

        return differences

    def __repr__(self) -> str:
        """String representation hiding sensitive fields."""
        # Get the actual attrs fields
        import attrs

        attr_fields = attrs.fields(self.__class__)

        parts = []
        for attr in attr_fields:
            # Skip internal fields
            if attr.name.startswith("_"):
                continue

            value = getattr(self, attr.name)

            # Hide sensitive values
            if attr.metadata.get("sensitive", False):
                value = "***SENSITIVE***"

            parts.append(f"{attr.name}={value!r}")

        return f"{self.__class__.__name__}({', '.join(parts)})"


# <3 🧱🤝⚙️🪄
