# provide/foundation/formatting/text.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re

"""Text manipulation and formatting utilities.

Provides utilities for text truncation, indentation, and other common
text operations.
"""

# Compiled regex patterns for performance
ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*m")
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


def x_truncate__mutmut_orig(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 0, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_1(text: str, max_length: int, suffix: str = "XX...XX", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 0, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_2(text: str, max_length: int, suffix: str = "...", whole_words: bool = False) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 0, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_3(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) < max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 0, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_4(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length < len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 0, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_5(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = None

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 0, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_6(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length + len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 0, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_7(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = None
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_8(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(None, 0, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_9(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", None, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_10(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 0, None)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_11(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(0, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_12(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_13(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 0, )
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_14(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.find(" ", 0, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_15(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind("XX XX", 0, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_16(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 1, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_17(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 0, truncate_at)
        if space_pos >= 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_18(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 0, truncate_at)
        if space_pos > 1:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def x_truncate__mutmut_19(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 0, truncate_at)
        if space_pos > 0:
            truncate_at = None

    return text[:truncate_at] + suffix


def x_truncate__mutmut_20(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 0, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] - suffix

x_truncate__mutmut_mutants : ClassVar[MutantDict] = {
'x_truncate__mutmut_1': x_truncate__mutmut_1, 
    'x_truncate__mutmut_2': x_truncate__mutmut_2, 
    'x_truncate__mutmut_3': x_truncate__mutmut_3, 
    'x_truncate__mutmut_4': x_truncate__mutmut_4, 
    'x_truncate__mutmut_5': x_truncate__mutmut_5, 
    'x_truncate__mutmut_6': x_truncate__mutmut_6, 
    'x_truncate__mutmut_7': x_truncate__mutmut_7, 
    'x_truncate__mutmut_8': x_truncate__mutmut_8, 
    'x_truncate__mutmut_9': x_truncate__mutmut_9, 
    'x_truncate__mutmut_10': x_truncate__mutmut_10, 
    'x_truncate__mutmut_11': x_truncate__mutmut_11, 
    'x_truncate__mutmut_12': x_truncate__mutmut_12, 
    'x_truncate__mutmut_13': x_truncate__mutmut_13, 
    'x_truncate__mutmut_14': x_truncate__mutmut_14, 
    'x_truncate__mutmut_15': x_truncate__mutmut_15, 
    'x_truncate__mutmut_16': x_truncate__mutmut_16, 
    'x_truncate__mutmut_17': x_truncate__mutmut_17, 
    'x_truncate__mutmut_18': x_truncate__mutmut_18, 
    'x_truncate__mutmut_19': x_truncate__mutmut_19, 
    'x_truncate__mutmut_20': x_truncate__mutmut_20
}

def truncate(*args, **kwargs):
    result = _mutmut_trampoline(x_truncate__mutmut_orig, x_truncate__mutmut_mutants, args, kwargs)
    return result 

truncate.__signature__ = _mutmut_signature(x_truncate__mutmut_orig)
x_truncate__mutmut_orig.__name__ = 'x_truncate'


def x_pluralize__mutmut_orig(count: int, singular: str, plural: str | None = None) -> str:
    """Get singular or plural form based on count.

    Args:
        count: Item count
        singular: Singular form
        plural: Plural form (default: singular + 's')

    Returns:
        Appropriate singular/plural form with count

    Examples:
        >>> pluralize(1, "file")
        '1 file'
        >>> pluralize(5, "file")
        '5 files'
        >>> pluralize(2, "child", "children")
        '2 children'

    """
    if plural is None:
        plural = f"{singular}s"

    word = singular if count == 1 else plural
    return f"{count} {word}"


def x_pluralize__mutmut_1(count: int, singular: str, plural: str | None = None) -> str:
    """Get singular or plural form based on count.

    Args:
        count: Item count
        singular: Singular form
        plural: Plural form (default: singular + 's')

    Returns:
        Appropriate singular/plural form with count

    Examples:
        >>> pluralize(1, "file")
        '1 file'
        >>> pluralize(5, "file")
        '5 files'
        >>> pluralize(2, "child", "children")
        '2 children'

    """
    if plural is not None:
        plural = f"{singular}s"

    word = singular if count == 1 else plural
    return f"{count} {word}"


def x_pluralize__mutmut_2(count: int, singular: str, plural: str | None = None) -> str:
    """Get singular or plural form based on count.

    Args:
        count: Item count
        singular: Singular form
        plural: Plural form (default: singular + 's')

    Returns:
        Appropriate singular/plural form with count

    Examples:
        >>> pluralize(1, "file")
        '1 file'
        >>> pluralize(5, "file")
        '5 files'
        >>> pluralize(2, "child", "children")
        '2 children'

    """
    if plural is None:
        plural = None

    word = singular if count == 1 else plural
    return f"{count} {word}"


def x_pluralize__mutmut_3(count: int, singular: str, plural: str | None = None) -> str:
    """Get singular or plural form based on count.

    Args:
        count: Item count
        singular: Singular form
        plural: Plural form (default: singular + 's')

    Returns:
        Appropriate singular/plural form with count

    Examples:
        >>> pluralize(1, "file")
        '1 file'
        >>> pluralize(5, "file")
        '5 files'
        >>> pluralize(2, "child", "children")
        '2 children'

    """
    if plural is None:
        plural = f"{singular}s"

    word = None
    return f"{count} {word}"


def x_pluralize__mutmut_4(count: int, singular: str, plural: str | None = None) -> str:
    """Get singular or plural form based on count.

    Args:
        count: Item count
        singular: Singular form
        plural: Plural form (default: singular + 's')

    Returns:
        Appropriate singular/plural form with count

    Examples:
        >>> pluralize(1, "file")
        '1 file'
        >>> pluralize(5, "file")
        '5 files'
        >>> pluralize(2, "child", "children")
        '2 children'

    """
    if plural is None:
        plural = f"{singular}s"

    word = singular if count != 1 else plural
    return f"{count} {word}"


def x_pluralize__mutmut_5(count: int, singular: str, plural: str | None = None) -> str:
    """Get singular or plural form based on count.

    Args:
        count: Item count
        singular: Singular form
        plural: Plural form (default: singular + 's')

    Returns:
        Appropriate singular/plural form with count

    Examples:
        >>> pluralize(1, "file")
        '1 file'
        >>> pluralize(5, "file")
        '5 files'
        >>> pluralize(2, "child", "children")
        '2 children'

    """
    if plural is None:
        plural = f"{singular}s"

    word = singular if count == 2 else plural
    return f"{count} {word}"

x_pluralize__mutmut_mutants : ClassVar[MutantDict] = {
'x_pluralize__mutmut_1': x_pluralize__mutmut_1, 
    'x_pluralize__mutmut_2': x_pluralize__mutmut_2, 
    'x_pluralize__mutmut_3': x_pluralize__mutmut_3, 
    'x_pluralize__mutmut_4': x_pluralize__mutmut_4, 
    'x_pluralize__mutmut_5': x_pluralize__mutmut_5
}

def pluralize(*args, **kwargs):
    result = _mutmut_trampoline(x_pluralize__mutmut_orig, x_pluralize__mutmut_mutants, args, kwargs)
    return result 

pluralize.__signature__ = _mutmut_signature(x_pluralize__mutmut_orig)
x_pluralize__mutmut_orig.__name__ = 'x_pluralize'


def x_indent__mutmut_orig(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_1(text: str, spaces: int = 3, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_2(text: str, spaces: int = 2, first_line: bool = False) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_3(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = None
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_4(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " / spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_5(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = "XX XX" * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_6(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = None

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_7(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_8(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = None
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_9(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(None):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_10(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 or not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_11(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i != 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_12(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 1 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_13(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_14(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(None)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def x_indent__mutmut_15(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(None)

    return "\n".join(result)


def x_indent__mutmut_16(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str - line if line else "")

    return "\n".join(result)


def x_indent__mutmut_17(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "XXXX")

    return "\n".join(result)


def x_indent__mutmut_18(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(None)


def x_indent__mutmut_19(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "XX\nXX".join(result)

x_indent__mutmut_mutants : ClassVar[MutantDict] = {
'x_indent__mutmut_1': x_indent__mutmut_1, 
    'x_indent__mutmut_2': x_indent__mutmut_2, 
    'x_indent__mutmut_3': x_indent__mutmut_3, 
    'x_indent__mutmut_4': x_indent__mutmut_4, 
    'x_indent__mutmut_5': x_indent__mutmut_5, 
    'x_indent__mutmut_6': x_indent__mutmut_6, 
    'x_indent__mutmut_7': x_indent__mutmut_7, 
    'x_indent__mutmut_8': x_indent__mutmut_8, 
    'x_indent__mutmut_9': x_indent__mutmut_9, 
    'x_indent__mutmut_10': x_indent__mutmut_10, 
    'x_indent__mutmut_11': x_indent__mutmut_11, 
    'x_indent__mutmut_12': x_indent__mutmut_12, 
    'x_indent__mutmut_13': x_indent__mutmut_13, 
    'x_indent__mutmut_14': x_indent__mutmut_14, 
    'x_indent__mutmut_15': x_indent__mutmut_15, 
    'x_indent__mutmut_16': x_indent__mutmut_16, 
    'x_indent__mutmut_17': x_indent__mutmut_17, 
    'x_indent__mutmut_18': x_indent__mutmut_18, 
    'x_indent__mutmut_19': x_indent__mutmut_19
}

def indent(*args, **kwargs):
    result = _mutmut_trampoline(x_indent__mutmut_orig, x_indent__mutmut_mutants, args, kwargs)
    return result 

indent.__signature__ = _mutmut_signature(x_indent__mutmut_orig)
x_indent__mutmut_orig.__name__ = 'x_indent'


def x_wrap_text__mutmut_orig(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_1(text: str, width: int = 81, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_2(text: str, width: int = 80, indent_first: int = 1, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_3(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 1) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_4(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = None

    return wrapper.fill(text)


def x_wrap_text__mutmut_5(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=None,
        initial_indent=" " * indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_6(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=None,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_7(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent=None,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_8(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=None,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_9(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        break_on_hyphens=None,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_10(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        initial_indent=" " * indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_11(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_12(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_13(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent=" " * indent_rest,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_14(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        )

    return wrapper.fill(text)


def x_wrap_text__mutmut_15(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " / indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_16(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent="XX XX" * indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_17(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent=" " / indent_rest,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_18(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent="XX XX" * indent_rest,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_19(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=True,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_20(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        break_on_hyphens=True,
    )

    return wrapper.fill(text)


def x_wrap_text__mutmut_21(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(None)

x_wrap_text__mutmut_mutants : ClassVar[MutantDict] = {
'x_wrap_text__mutmut_1': x_wrap_text__mutmut_1, 
    'x_wrap_text__mutmut_2': x_wrap_text__mutmut_2, 
    'x_wrap_text__mutmut_3': x_wrap_text__mutmut_3, 
    'x_wrap_text__mutmut_4': x_wrap_text__mutmut_4, 
    'x_wrap_text__mutmut_5': x_wrap_text__mutmut_5, 
    'x_wrap_text__mutmut_6': x_wrap_text__mutmut_6, 
    'x_wrap_text__mutmut_7': x_wrap_text__mutmut_7, 
    'x_wrap_text__mutmut_8': x_wrap_text__mutmut_8, 
    'x_wrap_text__mutmut_9': x_wrap_text__mutmut_9, 
    'x_wrap_text__mutmut_10': x_wrap_text__mutmut_10, 
    'x_wrap_text__mutmut_11': x_wrap_text__mutmut_11, 
    'x_wrap_text__mutmut_12': x_wrap_text__mutmut_12, 
    'x_wrap_text__mutmut_13': x_wrap_text__mutmut_13, 
    'x_wrap_text__mutmut_14': x_wrap_text__mutmut_14, 
    'x_wrap_text__mutmut_15': x_wrap_text__mutmut_15, 
    'x_wrap_text__mutmut_16': x_wrap_text__mutmut_16, 
    'x_wrap_text__mutmut_17': x_wrap_text__mutmut_17, 
    'x_wrap_text__mutmut_18': x_wrap_text__mutmut_18, 
    'x_wrap_text__mutmut_19': x_wrap_text__mutmut_19, 
    'x_wrap_text__mutmut_20': x_wrap_text__mutmut_20, 
    'x_wrap_text__mutmut_21': x_wrap_text__mutmut_21
}

def wrap_text(*args, **kwargs):
    result = _mutmut_trampoline(x_wrap_text__mutmut_orig, x_wrap_text__mutmut_mutants, args, kwargs)
    return result 

wrap_text.__signature__ = _mutmut_signature(x_wrap_text__mutmut_orig)
x_wrap_text__mutmut_orig.__name__ = 'x_wrap_text'


def x_strip_ansi__mutmut_orig(text: str) -> str:
    """Strip ANSI color codes from text.

    Args:
        text: Text with potential ANSI codes

    Returns:
        Text without ANSI codes

    """
    return ANSI_PATTERN.sub("", text)


def x_strip_ansi__mutmut_1(text: str) -> str:
    """Strip ANSI color codes from text.

    Args:
        text: Text with potential ANSI codes

    Returns:
        Text without ANSI codes

    """
    return ANSI_PATTERN.sub(None, text)


def x_strip_ansi__mutmut_2(text: str) -> str:
    """Strip ANSI color codes from text.

    Args:
        text: Text with potential ANSI codes

    Returns:
        Text without ANSI codes

    """
    return ANSI_PATTERN.sub("", None)


def x_strip_ansi__mutmut_3(text: str) -> str:
    """Strip ANSI color codes from text.

    Args:
        text: Text with potential ANSI codes

    Returns:
        Text without ANSI codes

    """
    return ANSI_PATTERN.sub(text)


def x_strip_ansi__mutmut_4(text: str) -> str:
    """Strip ANSI color codes from text.

    Args:
        text: Text with potential ANSI codes

    Returns:
        Text without ANSI codes

    """
    return ANSI_PATTERN.sub("", )


def x_strip_ansi__mutmut_5(text: str) -> str:
    """Strip ANSI color codes from text.

    Args:
        text: Text with potential ANSI codes

    Returns:
        Text without ANSI codes

    """
    return ANSI_PATTERN.sub("XXXX", text)

x_strip_ansi__mutmut_mutants : ClassVar[MutantDict] = {
'x_strip_ansi__mutmut_1': x_strip_ansi__mutmut_1, 
    'x_strip_ansi__mutmut_2': x_strip_ansi__mutmut_2, 
    'x_strip_ansi__mutmut_3': x_strip_ansi__mutmut_3, 
    'x_strip_ansi__mutmut_4': x_strip_ansi__mutmut_4, 
    'x_strip_ansi__mutmut_5': x_strip_ansi__mutmut_5
}

def strip_ansi(*args, **kwargs):
    result = _mutmut_trampoline(x_strip_ansi__mutmut_orig, x_strip_ansi__mutmut_mutants, args, kwargs)
    return result 

strip_ansi.__signature__ = _mutmut_signature(x_strip_ansi__mutmut_orig)
x_strip_ansi__mutmut_orig.__name__ = 'x_strip_ansi'


__all__ = [
    "indent",
    "pluralize",
    "strip_ansi",
    "truncate",
    "wrap_text",
]


# <3 🧱🤝🎨🪄
