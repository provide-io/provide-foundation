# provide/foundation/formatting/tables.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

"""Table formatting utilities.

Provides utilities for formatting data as ASCII tables with proper
alignment and column width calculation.
"""
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


def x__calculate_column_widths__mutmut_orig(headers: list[str], rows: list[list[str]]) -> list[int]:
    """Calculate optimal column widths for table formatting."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(cell))
    return widths


def x__calculate_column_widths__mutmut_1(headers: list[str], rows: list[list[str]]) -> list[int]:
    """Calculate optimal column widths for table formatting."""
    widths = None
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(cell))
    return widths


def x__calculate_column_widths__mutmut_2(headers: list[str], rows: list[list[str]]) -> list[int]:
    """Calculate optimal column widths for table formatting."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(None):
            if i < len(widths):
                widths[i] = max(widths[i], len(cell))
    return widths


def x__calculate_column_widths__mutmut_3(headers: list[str], rows: list[list[str]]) -> list[int]:
    """Calculate optimal column widths for table formatting."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i <= len(widths):
                widths[i] = max(widths[i], len(cell))
    return widths


def x__calculate_column_widths__mutmut_4(headers: list[str], rows: list[list[str]]) -> list[int]:
    """Calculate optimal column widths for table formatting."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = None
    return widths


def x__calculate_column_widths__mutmut_5(headers: list[str], rows: list[list[str]]) -> list[int]:
    """Calculate optimal column widths for table formatting."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(None, len(cell))
    return widths


def x__calculate_column_widths__mutmut_6(headers: list[str], rows: list[list[str]]) -> list[int]:
    """Calculate optimal column widths for table formatting."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], None)
    return widths


def x__calculate_column_widths__mutmut_7(headers: list[str], rows: list[list[str]]) -> list[int]:
    """Calculate optimal column widths for table formatting."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(len(cell))
    return widths


def x__calculate_column_widths__mutmut_8(headers: list[str], rows: list[list[str]]) -> list[int]:
    """Calculate optimal column widths for table formatting."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(
                    widths[i],
                )
    return widths


x__calculate_column_widths__mutmut_mutants: ClassVar[MutantDict] = {
    "x__calculate_column_widths__mutmut_1": x__calculate_column_widths__mutmut_1,
    "x__calculate_column_widths__mutmut_2": x__calculate_column_widths__mutmut_2,
    "x__calculate_column_widths__mutmut_3": x__calculate_column_widths__mutmut_3,
    "x__calculate_column_widths__mutmut_4": x__calculate_column_widths__mutmut_4,
    "x__calculate_column_widths__mutmut_5": x__calculate_column_widths__mutmut_5,
    "x__calculate_column_widths__mutmut_6": x__calculate_column_widths__mutmut_6,
    "x__calculate_column_widths__mutmut_7": x__calculate_column_widths__mutmut_7,
    "x__calculate_column_widths__mutmut_8": x__calculate_column_widths__mutmut_8,
}


def _calculate_column_widths(*args, **kwargs):
    result = _mutmut_trampoline(
        x__calculate_column_widths__mutmut_orig, x__calculate_column_widths__mutmut_mutants, args, kwargs
    )
    return result


_calculate_column_widths.__signature__ = _mutmut_signature(x__calculate_column_widths__mutmut_orig)
x__calculate_column_widths__mutmut_orig.__name__ = "x__calculate_column_widths"


def x__align_cell__mutmut_orig(text: str, width: int, alignment: str) -> str:
    """Align cell text within the specified width."""
    if alignment == "r":
        return text.rjust(width)
    elif alignment == "c":
        return text.center(width)
    else:
        return text.ljust(width)


def x__align_cell__mutmut_1(text: str, width: int, alignment: str) -> str:
    """Align cell text within the specified width."""
    if alignment != "r":
        return text.rjust(width)
    elif alignment == "c":
        return text.center(width)
    else:
        return text.ljust(width)


def x__align_cell__mutmut_2(text: str, width: int, alignment: str) -> str:
    """Align cell text within the specified width."""
    if alignment == "XXrXX":
        return text.rjust(width)
    elif alignment == "c":
        return text.center(width)
    else:
        return text.ljust(width)


def x__align_cell__mutmut_3(text: str, width: int, alignment: str) -> str:
    """Align cell text within the specified width."""
    if alignment == "R":
        return text.rjust(width)
    elif alignment == "c":
        return text.center(width)
    else:
        return text.ljust(width)


def x__align_cell__mutmut_4(text: str, width: int, alignment: str) -> str:
    """Align cell text within the specified width."""
    if alignment == "r":
        return text.rjust(None)
    elif alignment == "c":
        return text.center(width)
    else:
        return text.ljust(width)


def x__align_cell__mutmut_5(text: str, width: int, alignment: str) -> str:
    """Align cell text within the specified width."""
    if alignment == "r":
        return text.ljust(width)
    elif alignment == "c":
        return text.center(width)
    else:
        return text.ljust(width)


def x__align_cell__mutmut_6(text: str, width: int, alignment: str) -> str:
    """Align cell text within the specified width."""
    if alignment == "r":
        return text.rjust(width)
    elif alignment != "c":
        return text.center(width)
    else:
        return text.ljust(width)


def x__align_cell__mutmut_7(text: str, width: int, alignment: str) -> str:
    """Align cell text within the specified width."""
    if alignment == "r":
        return text.rjust(width)
    elif alignment == "XXcXX":
        return text.center(width)
    else:
        return text.ljust(width)


def x__align_cell__mutmut_8(text: str, width: int, alignment: str) -> str:
    """Align cell text within the specified width."""
    if alignment == "r":
        return text.rjust(width)
    elif alignment == "C":
        return text.center(width)
    else:
        return text.ljust(width)


def x__align_cell__mutmut_9(text: str, width: int, alignment: str) -> str:
    """Align cell text within the specified width."""
    if alignment == "r":
        return text.rjust(width)
    elif alignment == "c":
        return text.center(None)
    else:
        return text.ljust(width)


def x__align_cell__mutmut_10(text: str, width: int, alignment: str) -> str:
    """Align cell text within the specified width."""
    if alignment == "r":
        return text.rjust(width)
    elif alignment == "c":
        return text.center(width)
    else:
        return text.ljust(None)


def x__align_cell__mutmut_11(text: str, width: int, alignment: str) -> str:
    """Align cell text within the specified width."""
    if alignment == "r":
        return text.rjust(width)
    elif alignment == "c":
        return text.center(width)
    else:
        return text.rjust(width)


x__align_cell__mutmut_mutants: ClassVar[MutantDict] = {
    "x__align_cell__mutmut_1": x__align_cell__mutmut_1,
    "x__align_cell__mutmut_2": x__align_cell__mutmut_2,
    "x__align_cell__mutmut_3": x__align_cell__mutmut_3,
    "x__align_cell__mutmut_4": x__align_cell__mutmut_4,
    "x__align_cell__mutmut_5": x__align_cell__mutmut_5,
    "x__align_cell__mutmut_6": x__align_cell__mutmut_6,
    "x__align_cell__mutmut_7": x__align_cell__mutmut_7,
    "x__align_cell__mutmut_8": x__align_cell__mutmut_8,
    "x__align_cell__mutmut_9": x__align_cell__mutmut_9,
    "x__align_cell__mutmut_10": x__align_cell__mutmut_10,
    "x__align_cell__mutmut_11": x__align_cell__mutmut_11,
}


def _align_cell(*args, **kwargs):
    result = _mutmut_trampoline(x__align_cell__mutmut_orig, x__align_cell__mutmut_mutants, args, kwargs)
    return result


_align_cell.__signature__ = _mutmut_signature(x__align_cell__mutmut_orig)
x__align_cell__mutmut_orig.__name__ = "x__align_cell"


def x__format_table_header__mutmut_orig(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_1(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = None
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_2(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = None

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_3(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(None):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_4(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(None, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_5(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, None, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_6(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=None)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_7(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_8(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_9(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(
        zip(
            headers,
            widths,
        )
    ):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_10(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=True)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_11(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = None
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_12(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i <= len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_13(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "XXlXX"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_14(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "L"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_15(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(None)
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_16(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(None, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_17(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, None, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_18(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, None))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_19(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_20(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_21(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(
            _align_cell(
                header,
                width,
            )
        )
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_22(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append(None)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_23(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" / width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_24(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("XX-XX" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_25(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(None), "-|-".join(separator_parts)


def x__format_table_header__mutmut_26(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return "XX | XX".join(header_parts), "-|-".join(separator_parts)


def x__format_table_header__mutmut_27(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(None)


def x__format_table_header__mutmut_28(
    headers: list[str], widths: list[int], alignment: list[str]
) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "XX-|-XX".join(separator_parts)


x__format_table_header__mutmut_mutants: ClassVar[MutantDict] = {
    "x__format_table_header__mutmut_1": x__format_table_header__mutmut_1,
    "x__format_table_header__mutmut_2": x__format_table_header__mutmut_2,
    "x__format_table_header__mutmut_3": x__format_table_header__mutmut_3,
    "x__format_table_header__mutmut_4": x__format_table_header__mutmut_4,
    "x__format_table_header__mutmut_5": x__format_table_header__mutmut_5,
    "x__format_table_header__mutmut_6": x__format_table_header__mutmut_6,
    "x__format_table_header__mutmut_7": x__format_table_header__mutmut_7,
    "x__format_table_header__mutmut_8": x__format_table_header__mutmut_8,
    "x__format_table_header__mutmut_9": x__format_table_header__mutmut_9,
    "x__format_table_header__mutmut_10": x__format_table_header__mutmut_10,
    "x__format_table_header__mutmut_11": x__format_table_header__mutmut_11,
    "x__format_table_header__mutmut_12": x__format_table_header__mutmut_12,
    "x__format_table_header__mutmut_13": x__format_table_header__mutmut_13,
    "x__format_table_header__mutmut_14": x__format_table_header__mutmut_14,
    "x__format_table_header__mutmut_15": x__format_table_header__mutmut_15,
    "x__format_table_header__mutmut_16": x__format_table_header__mutmut_16,
    "x__format_table_header__mutmut_17": x__format_table_header__mutmut_17,
    "x__format_table_header__mutmut_18": x__format_table_header__mutmut_18,
    "x__format_table_header__mutmut_19": x__format_table_header__mutmut_19,
    "x__format_table_header__mutmut_20": x__format_table_header__mutmut_20,
    "x__format_table_header__mutmut_21": x__format_table_header__mutmut_21,
    "x__format_table_header__mutmut_22": x__format_table_header__mutmut_22,
    "x__format_table_header__mutmut_23": x__format_table_header__mutmut_23,
    "x__format_table_header__mutmut_24": x__format_table_header__mutmut_24,
    "x__format_table_header__mutmut_25": x__format_table_header__mutmut_25,
    "x__format_table_header__mutmut_26": x__format_table_header__mutmut_26,
    "x__format_table_header__mutmut_27": x__format_table_header__mutmut_27,
    "x__format_table_header__mutmut_28": x__format_table_header__mutmut_28,
}


def _format_table_header(*args, **kwargs):
    result = _mutmut_trampoline(
        x__format_table_header__mutmut_orig, x__format_table_header__mutmut_mutants, args, kwargs
    )
    return result


_format_table_header.__signature__ = _mutmut_signature(x__format_table_header__mutmut_orig)
x__format_table_header__mutmut_orig.__name__ = "x__format_table_header"


def x__format_table_row__mutmut_orig(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "l"
            row_parts.append(_align_cell(cell, widths[i], align))
    return " | ".join(row_parts)


def x__format_table_row__mutmut_1(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = None
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "l"
            row_parts.append(_align_cell(cell, widths[i], align))
    return " | ".join(row_parts)


def x__format_table_row__mutmut_2(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(None):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "l"
            row_parts.append(_align_cell(cell, widths[i], align))
    return " | ".join(row_parts)


def x__format_table_row__mutmut_3(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i <= len(widths):
            align = alignment[i] if i < len(alignment) else "l"
            row_parts.append(_align_cell(cell, widths[i], align))
    return " | ".join(row_parts)


def x__format_table_row__mutmut_4(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = None
            row_parts.append(_align_cell(cell, widths[i], align))
    return " | ".join(row_parts)


def x__format_table_row__mutmut_5(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i <= len(alignment) else "l"
            row_parts.append(_align_cell(cell, widths[i], align))
    return " | ".join(row_parts)


def x__format_table_row__mutmut_6(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "XXlXX"
            row_parts.append(_align_cell(cell, widths[i], align))
    return " | ".join(row_parts)


def x__format_table_row__mutmut_7(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "L"
            row_parts.append(_align_cell(cell, widths[i], align))
    return " | ".join(row_parts)


def x__format_table_row__mutmut_8(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "l"
            row_parts.append(None)
    return " | ".join(row_parts)


def x__format_table_row__mutmut_9(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "l"
            row_parts.append(_align_cell(None, widths[i], align))
    return " | ".join(row_parts)


def x__format_table_row__mutmut_10(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "l"
            row_parts.append(_align_cell(cell, None, align))
    return " | ".join(row_parts)


def x__format_table_row__mutmut_11(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "l"
            row_parts.append(_align_cell(cell, widths[i], None))
    return " | ".join(row_parts)


def x__format_table_row__mutmut_12(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "l"
            row_parts.append(_align_cell(widths[i], align))
    return " | ".join(row_parts)


def x__format_table_row__mutmut_13(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "l"
            row_parts.append(_align_cell(cell, align))
    return " | ".join(row_parts)


def x__format_table_row__mutmut_14(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "l"
            row_parts.append(
                _align_cell(
                    cell,
                    widths[i],
                )
            )
    return " | ".join(row_parts)


def x__format_table_row__mutmut_15(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "l"
            row_parts.append(_align_cell(cell, widths[i], align))
    return " | ".join(None)


def x__format_table_row__mutmut_16(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "l"
            row_parts.append(_align_cell(cell, widths[i], align))
    return "XX | XX".join(row_parts)


x__format_table_row__mutmut_mutants: ClassVar[MutantDict] = {
    "x__format_table_row__mutmut_1": x__format_table_row__mutmut_1,
    "x__format_table_row__mutmut_2": x__format_table_row__mutmut_2,
    "x__format_table_row__mutmut_3": x__format_table_row__mutmut_3,
    "x__format_table_row__mutmut_4": x__format_table_row__mutmut_4,
    "x__format_table_row__mutmut_5": x__format_table_row__mutmut_5,
    "x__format_table_row__mutmut_6": x__format_table_row__mutmut_6,
    "x__format_table_row__mutmut_7": x__format_table_row__mutmut_7,
    "x__format_table_row__mutmut_8": x__format_table_row__mutmut_8,
    "x__format_table_row__mutmut_9": x__format_table_row__mutmut_9,
    "x__format_table_row__mutmut_10": x__format_table_row__mutmut_10,
    "x__format_table_row__mutmut_11": x__format_table_row__mutmut_11,
    "x__format_table_row__mutmut_12": x__format_table_row__mutmut_12,
    "x__format_table_row__mutmut_13": x__format_table_row__mutmut_13,
    "x__format_table_row__mutmut_14": x__format_table_row__mutmut_14,
    "x__format_table_row__mutmut_15": x__format_table_row__mutmut_15,
    "x__format_table_row__mutmut_16": x__format_table_row__mutmut_16,
}


def _format_table_row(*args, **kwargs):
    result = _mutmut_trampoline(
        x__format_table_row__mutmut_orig, x__format_table_row__mutmut_mutants, args, kwargs
    )
    return result


_format_table_row.__signature__ = _mutmut_signature(x__format_table_row__mutmut_orig)
x__format_table_row__mutmut_orig.__name__ = "x__format_table_row"


def x_format_table__mutmut_orig(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_1(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers or not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_2(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_3(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_4(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return "XXXX"

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_5(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = None
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_6(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(None) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_7(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = None

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_8(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(None) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_9(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = None

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_10(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(None, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_11(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, None)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_12(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_13(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(
        str_headers,
    )

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_14(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is not None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_15(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = None

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_16(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] / len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_17(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["XXlXX"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_18(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["L"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_19(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = None
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_20(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(None, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_21(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, None, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_22(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, None)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_23(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_24(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_25(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(
        str_headers,
        widths,
    )
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_26(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = None

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_27(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(None)

    return "\n".join(lines)


def x_format_table__mutmut_28(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(None, widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_29(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, None, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_30(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, None))

    return "\n".join(lines)


def x_format_table__mutmut_31(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(widths, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_32(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, alignment))

    return "\n".join(lines)


def x_format_table__mutmut_33(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(
            _format_table_row(
                row,
                widths,
            )
        )

    return "\n".join(lines)


def x_format_table__mutmut_34(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(None)


def x_format_table__mutmut_35(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "XX\nXX".join(lines)


x_format_table__mutmut_mutants: ClassVar[MutantDict] = {
    "x_format_table__mutmut_1": x_format_table__mutmut_1,
    "x_format_table__mutmut_2": x_format_table__mutmut_2,
    "x_format_table__mutmut_3": x_format_table__mutmut_3,
    "x_format_table__mutmut_4": x_format_table__mutmut_4,
    "x_format_table__mutmut_5": x_format_table__mutmut_5,
    "x_format_table__mutmut_6": x_format_table__mutmut_6,
    "x_format_table__mutmut_7": x_format_table__mutmut_7,
    "x_format_table__mutmut_8": x_format_table__mutmut_8,
    "x_format_table__mutmut_9": x_format_table__mutmut_9,
    "x_format_table__mutmut_10": x_format_table__mutmut_10,
    "x_format_table__mutmut_11": x_format_table__mutmut_11,
    "x_format_table__mutmut_12": x_format_table__mutmut_12,
    "x_format_table__mutmut_13": x_format_table__mutmut_13,
    "x_format_table__mutmut_14": x_format_table__mutmut_14,
    "x_format_table__mutmut_15": x_format_table__mutmut_15,
    "x_format_table__mutmut_16": x_format_table__mutmut_16,
    "x_format_table__mutmut_17": x_format_table__mutmut_17,
    "x_format_table__mutmut_18": x_format_table__mutmut_18,
    "x_format_table__mutmut_19": x_format_table__mutmut_19,
    "x_format_table__mutmut_20": x_format_table__mutmut_20,
    "x_format_table__mutmut_21": x_format_table__mutmut_21,
    "x_format_table__mutmut_22": x_format_table__mutmut_22,
    "x_format_table__mutmut_23": x_format_table__mutmut_23,
    "x_format_table__mutmut_24": x_format_table__mutmut_24,
    "x_format_table__mutmut_25": x_format_table__mutmut_25,
    "x_format_table__mutmut_26": x_format_table__mutmut_26,
    "x_format_table__mutmut_27": x_format_table__mutmut_27,
    "x_format_table__mutmut_28": x_format_table__mutmut_28,
    "x_format_table__mutmut_29": x_format_table__mutmut_29,
    "x_format_table__mutmut_30": x_format_table__mutmut_30,
    "x_format_table__mutmut_31": x_format_table__mutmut_31,
    "x_format_table__mutmut_32": x_format_table__mutmut_32,
    "x_format_table__mutmut_33": x_format_table__mutmut_33,
    "x_format_table__mutmut_34": x_format_table__mutmut_34,
    "x_format_table__mutmut_35": x_format_table__mutmut_35,
}


def format_table(*args, **kwargs):
    result = _mutmut_trampoline(x_format_table__mutmut_orig, x_format_table__mutmut_mutants, args, kwargs)
    return result


format_table.__signature__ = _mutmut_signature(x_format_table__mutmut_orig)
x_format_table__mutmut_orig.__name__ = "x_format_table"


__all__ = [
    "format_table",
]


# <3 🧱🤝🎨🪄
