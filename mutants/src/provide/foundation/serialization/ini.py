# provide/foundation/serialization/ini.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from configparser import ConfigParser
from io import StringIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass
from provide.foundation.serialization.cache import get_cache_enabled, get_cache_key, get_serialization_cache

"""INI format serialization with caching support."""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_ini_dumps__mutmut_orig(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_1(obj: dict[str, dict[str, str]], *, include_default: bool = True) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_2(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_3(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError(None)

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_4(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("XXINI serialization requires a dictionaryXX")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_5(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ini serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_6(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI SERIALIZATION REQUIRES A DICTIONARY")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_7(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = None

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_8(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" or not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_9(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name != "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_10(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "XXDEFAULTXX" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_11(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "default" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_12(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_13(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                break

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_14(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_15(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(None)

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_16(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name == "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_17(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "XXDEFAULTXX":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_18(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "default":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_19(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(None)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_20(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(None, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_21(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, None, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_22(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, None)

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_23(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_24(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_25(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, )

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_26(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(None))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_27(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = None
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_28(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(None)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to INI: {e}") from e


def x_ini_dumps__mutmut_29(obj: dict[str, dict[str, str]], *, include_default: bool = False) -> str:
    """Serialize nested dictionary to INI format string.

    Args:
        obj: Nested dictionary (sections -> key-value pairs)
        include_default: Whether to include DEFAULT section

    Returns:
        INI format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> ini_dumps({"section": {"key": "value"}})
        '[section]\\nkey = value\\n\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("INI serialization requires a dictionary")

    parser = ConfigParser()

    try:
        for section_name, section_data in obj.items():
            if section_name == "DEFAULT" and not include_default:
                continue

            if not isinstance(section_data, dict):
                raise ValidationError(f"Section '{section_name}' must be a dictionary")

            if section_name != "DEFAULT":
                parser.add_section(section_name)

            for key, value in section_data.items():
                parser.set(section_name, key, str(value))

        # Write to string
        output = StringIO()
        parser.write(output)
        return output.getvalue()
    except Exception as e:
        raise ValidationError(None) from e

x_ini_dumps__mutmut_mutants : ClassVar[MutantDict] = {
'x_ini_dumps__mutmut_1': x_ini_dumps__mutmut_1, 
    'x_ini_dumps__mutmut_2': x_ini_dumps__mutmut_2, 
    'x_ini_dumps__mutmut_3': x_ini_dumps__mutmut_3, 
    'x_ini_dumps__mutmut_4': x_ini_dumps__mutmut_4, 
    'x_ini_dumps__mutmut_5': x_ini_dumps__mutmut_5, 
    'x_ini_dumps__mutmut_6': x_ini_dumps__mutmut_6, 
    'x_ini_dumps__mutmut_7': x_ini_dumps__mutmut_7, 
    'x_ini_dumps__mutmut_8': x_ini_dumps__mutmut_8, 
    'x_ini_dumps__mutmut_9': x_ini_dumps__mutmut_9, 
    'x_ini_dumps__mutmut_10': x_ini_dumps__mutmut_10, 
    'x_ini_dumps__mutmut_11': x_ini_dumps__mutmut_11, 
    'x_ini_dumps__mutmut_12': x_ini_dumps__mutmut_12, 
    'x_ini_dumps__mutmut_13': x_ini_dumps__mutmut_13, 
    'x_ini_dumps__mutmut_14': x_ini_dumps__mutmut_14, 
    'x_ini_dumps__mutmut_15': x_ini_dumps__mutmut_15, 
    'x_ini_dumps__mutmut_16': x_ini_dumps__mutmut_16, 
    'x_ini_dumps__mutmut_17': x_ini_dumps__mutmut_17, 
    'x_ini_dumps__mutmut_18': x_ini_dumps__mutmut_18, 
    'x_ini_dumps__mutmut_19': x_ini_dumps__mutmut_19, 
    'x_ini_dumps__mutmut_20': x_ini_dumps__mutmut_20, 
    'x_ini_dumps__mutmut_21': x_ini_dumps__mutmut_21, 
    'x_ini_dumps__mutmut_22': x_ini_dumps__mutmut_22, 
    'x_ini_dumps__mutmut_23': x_ini_dumps__mutmut_23, 
    'x_ini_dumps__mutmut_24': x_ini_dumps__mutmut_24, 
    'x_ini_dumps__mutmut_25': x_ini_dumps__mutmut_25, 
    'x_ini_dumps__mutmut_26': x_ini_dumps__mutmut_26, 
    'x_ini_dumps__mutmut_27': x_ini_dumps__mutmut_27, 
    'x_ini_dumps__mutmut_28': x_ini_dumps__mutmut_28, 
    'x_ini_dumps__mutmut_29': x_ini_dumps__mutmut_29
}

def ini_dumps(*args, **kwargs):
    result = _mutmut_trampoline(x_ini_dumps__mutmut_orig, x_ini_dumps__mutmut_mutants, args, kwargs)
    return result 

ini_dumps.__signature__ = _mutmut_signature(x_ini_dumps__mutmut_orig)
x_ini_dumps__mutmut_orig.__name__ = 'x_ini_dumps'


def x_ini_loads__mutmut_orig(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_1(s: str, *, use_cache: bool = False) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_2(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_3(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError(None)

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_4(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("XXInput must be a stringXX")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_5(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_6(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("INPUT MUST BE A STRING")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_7(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache or get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_8(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = None
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_9(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(None, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_10(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, None)
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_11(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key("ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_12(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, )
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_13(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "XXiniXX")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_14(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "INI")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_15(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = None
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_16(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(None)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_17(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_18(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = None

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_19(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(None)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_20(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(None) from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_21(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = None

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_22(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = None

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_23(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(None)

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_24(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(None))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_25(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = None

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_26(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["XXDEFAULTXX"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_27(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["default"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_28(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(None)

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_29(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache or get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_30(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = None
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_31(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(None, "ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_32(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, None)
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_33(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key("ini")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_34(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, )
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_35(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "XXiniXX")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_36(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "INI")
        get_serialization_cache().set(cache_key, result)

    return result


def x_ini_loads__mutmut_37(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(None, result)

    return result


def x_ini_loads__mutmut_38(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, None)

    return result


def x_ini_loads__mutmut_39(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(result)

    return result


def x_ini_loads__mutmut_40(s: str, *, use_cache: bool = True) -> dict[str, dict[str, str]]:
    """Deserialize INI format string to nested dictionary.

    Args:
        s: INI format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Nested dictionary (sections -> key-value pairs)

    Raises:
        ValidationError: If string is not valid INI format

    Example:
        >>> ini_loads('[section]\\nkey = value')
        {'section': {'key': 'value'}}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    parser = ConfigParser()

    try:
        parser.read_string(s)
    except Exception as e:
        raise ValidationError(f"Invalid INI string: {e}") from e

    # Convert to dictionary
    result: dict[str, dict[str, str]] = {}

    for section in parser.sections():
        result[section] = dict(parser.items(section))

    # Include DEFAULT section if present
    if parser.defaults():
        result["DEFAULT"] = dict(parser.defaults())

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ini")
        get_serialization_cache().set(cache_key, )

    return result

x_ini_loads__mutmut_mutants : ClassVar[MutantDict] = {
'x_ini_loads__mutmut_1': x_ini_loads__mutmut_1, 
    'x_ini_loads__mutmut_2': x_ini_loads__mutmut_2, 
    'x_ini_loads__mutmut_3': x_ini_loads__mutmut_3, 
    'x_ini_loads__mutmut_4': x_ini_loads__mutmut_4, 
    'x_ini_loads__mutmut_5': x_ini_loads__mutmut_5, 
    'x_ini_loads__mutmut_6': x_ini_loads__mutmut_6, 
    'x_ini_loads__mutmut_7': x_ini_loads__mutmut_7, 
    'x_ini_loads__mutmut_8': x_ini_loads__mutmut_8, 
    'x_ini_loads__mutmut_9': x_ini_loads__mutmut_9, 
    'x_ini_loads__mutmut_10': x_ini_loads__mutmut_10, 
    'x_ini_loads__mutmut_11': x_ini_loads__mutmut_11, 
    'x_ini_loads__mutmut_12': x_ini_loads__mutmut_12, 
    'x_ini_loads__mutmut_13': x_ini_loads__mutmut_13, 
    'x_ini_loads__mutmut_14': x_ini_loads__mutmut_14, 
    'x_ini_loads__mutmut_15': x_ini_loads__mutmut_15, 
    'x_ini_loads__mutmut_16': x_ini_loads__mutmut_16, 
    'x_ini_loads__mutmut_17': x_ini_loads__mutmut_17, 
    'x_ini_loads__mutmut_18': x_ini_loads__mutmut_18, 
    'x_ini_loads__mutmut_19': x_ini_loads__mutmut_19, 
    'x_ini_loads__mutmut_20': x_ini_loads__mutmut_20, 
    'x_ini_loads__mutmut_21': x_ini_loads__mutmut_21, 
    'x_ini_loads__mutmut_22': x_ini_loads__mutmut_22, 
    'x_ini_loads__mutmut_23': x_ini_loads__mutmut_23, 
    'x_ini_loads__mutmut_24': x_ini_loads__mutmut_24, 
    'x_ini_loads__mutmut_25': x_ini_loads__mutmut_25, 
    'x_ini_loads__mutmut_26': x_ini_loads__mutmut_26, 
    'x_ini_loads__mutmut_27': x_ini_loads__mutmut_27, 
    'x_ini_loads__mutmut_28': x_ini_loads__mutmut_28, 
    'x_ini_loads__mutmut_29': x_ini_loads__mutmut_29, 
    'x_ini_loads__mutmut_30': x_ini_loads__mutmut_30, 
    'x_ini_loads__mutmut_31': x_ini_loads__mutmut_31, 
    'x_ini_loads__mutmut_32': x_ini_loads__mutmut_32, 
    'x_ini_loads__mutmut_33': x_ini_loads__mutmut_33, 
    'x_ini_loads__mutmut_34': x_ini_loads__mutmut_34, 
    'x_ini_loads__mutmut_35': x_ini_loads__mutmut_35, 
    'x_ini_loads__mutmut_36': x_ini_loads__mutmut_36, 
    'x_ini_loads__mutmut_37': x_ini_loads__mutmut_37, 
    'x_ini_loads__mutmut_38': x_ini_loads__mutmut_38, 
    'x_ini_loads__mutmut_39': x_ini_loads__mutmut_39, 
    'x_ini_loads__mutmut_40': x_ini_loads__mutmut_40
}

def ini_loads(*args, **kwargs):
    result = _mutmut_trampoline(x_ini_loads__mutmut_orig, x_ini_loads__mutmut_mutants, args, kwargs)
    return result 

ini_loads.__signature__ = _mutmut_signature(x_ini_loads__mutmut_orig)
x_ini_loads__mutmut_orig.__name__ = 'x_ini_loads'


__all__ = [
    "ini_dumps",
    "ini_loads",
]


# <3 🧱🤝📜🪄
