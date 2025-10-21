# provide/foundation/eventsets/display.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from provide.foundation.eventsets.registry import discover_event_sets, get_registry
from provide.foundation.eventsets.resolver import get_resolver
from provide.foundation.logger import get_logger

if TYPE_CHECKING:
    from provide.foundation.eventsets.resolver import EventSetResolver
    from provide.foundation.eventsets.types import EventSet

"""Event set display utilities for Foundation."""

log = get_logger(__name__)
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


def x__format_event_set_config__mutmut_orig(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 5:
            lines.append(f"      ... and {len(config.field_mappings) - 5} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_1(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(None)
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 5:
            lines.append(f"      ... and {len(config.field_mappings) - 5} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_2(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(None)

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 5:
            lines.append(f"      ... and {len(config.field_mappings) - 5} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_3(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(None)
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 5:
            lines.append(f"      ... and {len(config.field_mappings) - 5} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_4(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:6]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 5:
            lines.append(f"      ... and {len(config.field_mappings) - 5} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_5(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(None)
        if len(config.field_mappings) > 5:
            lines.append(f"      ... and {len(config.field_mappings) - 5} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_6(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) >= 5:
            lines.append(f"      ... and {len(config.field_mappings) - 5} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_7(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 6:
            lines.append(f"      ... and {len(config.field_mappings) - 5} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_8(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 5:
            lines.append(None)

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_9(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 5:
            lines.append(f"      ... and {len(config.field_mappings) + 5} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_10(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 5:
            lines.append(f"      ... and {len(config.field_mappings) - 6} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_11(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 5:
            lines.append(f"      ... and {len(config.field_mappings) - 5} more")

    # Show mappings
    if config.mappings:
        lines.append(None)
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_12(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 5:
            lines.append(f"      ... and {len(config.field_mappings) - 5} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = None
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_13(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 5:
            lines.append(f"      ... and {len(config.field_mappings) - 5} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = None
            transform_count = len(event_mapping.transformations)
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_14(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 5:
            lines.append(f"      ... and {len(config.field_mappings) - 5} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = None
            lines.append(
                f"      - {event_mapping.name}: "
                f"{marker_count} markers, "
                f"{metadata_count} metadata, "
                f"{transform_count} transforms",
            )


def x__format_event_set_config__mutmut_15(config: EventSet, lines: list[str]) -> None:
    """Format a single event set configuration."""
    lines.append(f"\n  {config.name} (priority: {config.priority})")
    if config.description:
        lines.append(f"    {config.description}")

    # Show field mappings
    if config.field_mappings:
        lines.append(f"    Field Mappings ({len(config.field_mappings)}):")
        for mapping in config.field_mappings[:5]:  # Show first 5
            lines.append(f"      - {mapping.log_key}")
        if len(config.field_mappings) > 5:
            lines.append(f"      ... and {len(config.field_mappings) - 5} more")

    # Show mappings
    if config.mappings:
        lines.append(f"    Mappings ({len(config.mappings)}):")
        for event_mapping in config.mappings:
            marker_count = len(event_mapping.visual_markers)
            metadata_count = len(event_mapping.metadata_fields)
            transform_count = len(event_mapping.transformations)
            lines.append(
                None,
            )

x__format_event_set_config__mutmut_mutants : ClassVar[MutantDict] = {
'x__format_event_set_config__mutmut_1': x__format_event_set_config__mutmut_1, 
    'x__format_event_set_config__mutmut_2': x__format_event_set_config__mutmut_2, 
    'x__format_event_set_config__mutmut_3': x__format_event_set_config__mutmut_3, 
    'x__format_event_set_config__mutmut_4': x__format_event_set_config__mutmut_4, 
    'x__format_event_set_config__mutmut_5': x__format_event_set_config__mutmut_5, 
    'x__format_event_set_config__mutmut_6': x__format_event_set_config__mutmut_6, 
    'x__format_event_set_config__mutmut_7': x__format_event_set_config__mutmut_7, 
    'x__format_event_set_config__mutmut_8': x__format_event_set_config__mutmut_8, 
    'x__format_event_set_config__mutmut_9': x__format_event_set_config__mutmut_9, 
    'x__format_event_set_config__mutmut_10': x__format_event_set_config__mutmut_10, 
    'x__format_event_set_config__mutmut_11': x__format_event_set_config__mutmut_11, 
    'x__format_event_set_config__mutmut_12': x__format_event_set_config__mutmut_12, 
    'x__format_event_set_config__mutmut_13': x__format_event_set_config__mutmut_13, 
    'x__format_event_set_config__mutmut_14': x__format_event_set_config__mutmut_14, 
    'x__format_event_set_config__mutmut_15': x__format_event_set_config__mutmut_15
}

def _format_event_set_config(*args, **kwargs):
    result = _mutmut_trampoline(x__format_event_set_config__mutmut_orig, x__format_event_set_config__mutmut_mutants, args, kwargs)
    return result 

_format_event_set_config.__signature__ = _mutmut_signature(x__format_event_set_config__mutmut_orig)
x__format_event_set_config__mutmut_orig.__name__ = 'x__format_event_set_config'


def x__format_registered_event_sets__mutmut_orig(event_sets: list[EventSet], lines: list[str]) -> None:
    """Format the registered event sets section."""
    if event_sets:
        lines.append(f"\nRegistered Event Sets ({len(event_sets)}):")
        for config in event_sets:
            _format_event_set_config(config, lines)
    else:
        lines.append("\n  (No event sets registered)")


def x__format_registered_event_sets__mutmut_1(event_sets: list[EventSet], lines: list[str]) -> None:
    """Format the registered event sets section."""
    if event_sets:
        lines.append(None)
        for config in event_sets:
            _format_event_set_config(config, lines)
    else:
        lines.append("\n  (No event sets registered)")


def x__format_registered_event_sets__mutmut_2(event_sets: list[EventSet], lines: list[str]) -> None:
    """Format the registered event sets section."""
    if event_sets:
        lines.append(f"\nRegistered Event Sets ({len(event_sets)}):")
        for config in event_sets:
            _format_event_set_config(None, lines)
    else:
        lines.append("\n  (No event sets registered)")


def x__format_registered_event_sets__mutmut_3(event_sets: list[EventSet], lines: list[str]) -> None:
    """Format the registered event sets section."""
    if event_sets:
        lines.append(f"\nRegistered Event Sets ({len(event_sets)}):")
        for config in event_sets:
            _format_event_set_config(config, None)
    else:
        lines.append("\n  (No event sets registered)")


def x__format_registered_event_sets__mutmut_4(event_sets: list[EventSet], lines: list[str]) -> None:
    """Format the registered event sets section."""
    if event_sets:
        lines.append(f"\nRegistered Event Sets ({len(event_sets)}):")
        for config in event_sets:
            _format_event_set_config(lines)
    else:
        lines.append("\n  (No event sets registered)")


def x__format_registered_event_sets__mutmut_5(event_sets: list[EventSet], lines: list[str]) -> None:
    """Format the registered event sets section."""
    if event_sets:
        lines.append(f"\nRegistered Event Sets ({len(event_sets)}):")
        for config in event_sets:
            _format_event_set_config(config, )
    else:
        lines.append("\n  (No event sets registered)")


def x__format_registered_event_sets__mutmut_6(event_sets: list[EventSet], lines: list[str]) -> None:
    """Format the registered event sets section."""
    if event_sets:
        lines.append(f"\nRegistered Event Sets ({len(event_sets)}):")
        for config in event_sets:
            _format_event_set_config(config, lines)
    else:
        lines.append(None)


def x__format_registered_event_sets__mutmut_7(event_sets: list[EventSet], lines: list[str]) -> None:
    """Format the registered event sets section."""
    if event_sets:
        lines.append(f"\nRegistered Event Sets ({len(event_sets)}):")
        for config in event_sets:
            _format_event_set_config(config, lines)
    else:
        lines.append("XX\n  (No event sets registered)XX")


def x__format_registered_event_sets__mutmut_8(event_sets: list[EventSet], lines: list[str]) -> None:
    """Format the registered event sets section."""
    if event_sets:
        lines.append(f"\nRegistered Event Sets ({len(event_sets)}):")
        for config in event_sets:
            _format_event_set_config(config, lines)
    else:
        lines.append("\n  (no event sets registered)")


def x__format_registered_event_sets__mutmut_9(event_sets: list[EventSet], lines: list[str]) -> None:
    """Format the registered event sets section."""
    if event_sets:
        lines.append(f"\nRegistered Event Sets ({len(event_sets)}):")
        for config in event_sets:
            _format_event_set_config(config, lines)
    else:
        lines.append("\n  (NO EVENT SETS REGISTERED)")

x__format_registered_event_sets__mutmut_mutants : ClassVar[MutantDict] = {
'x__format_registered_event_sets__mutmut_1': x__format_registered_event_sets__mutmut_1, 
    'x__format_registered_event_sets__mutmut_2': x__format_registered_event_sets__mutmut_2, 
    'x__format_registered_event_sets__mutmut_3': x__format_registered_event_sets__mutmut_3, 
    'x__format_registered_event_sets__mutmut_4': x__format_registered_event_sets__mutmut_4, 
    'x__format_registered_event_sets__mutmut_5': x__format_registered_event_sets__mutmut_5, 
    'x__format_registered_event_sets__mutmut_6': x__format_registered_event_sets__mutmut_6, 
    'x__format_registered_event_sets__mutmut_7': x__format_registered_event_sets__mutmut_7, 
    'x__format_registered_event_sets__mutmut_8': x__format_registered_event_sets__mutmut_8, 
    'x__format_registered_event_sets__mutmut_9': x__format_registered_event_sets__mutmut_9
}

def _format_registered_event_sets(*args, **kwargs):
    result = _mutmut_trampoline(x__format_registered_event_sets__mutmut_orig, x__format_registered_event_sets__mutmut_mutants, args, kwargs)
    return result 

_format_registered_event_sets.__signature__ = _mutmut_signature(x__format_registered_event_sets__mutmut_orig)
x__format_registered_event_sets__mutmut_orig.__name__ = 'x__format_registered_event_sets'


def x__format_resolver_state__mutmut_orig(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_1(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append(None)
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_2(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("XX\nResolver State:XX")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_3(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nresolver state:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_4(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nRESOLVER STATE:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_5(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(None)
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_6(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(None)

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_7(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append(None)
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_8(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("XX\n  Sample Visual Markers:XX")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_9(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  sample visual markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_10(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  SAMPLE VISUAL MARKERS:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_11(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(None)[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_12(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:4]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_13(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:2]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_14(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = None
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_15(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(None)[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_16(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:4]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_17(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(None)
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_18(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(None)
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_19(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        return  # Only show first mapping with visual markers
    else:
        lines.append("\n  (Resolver not yet initialized)")


def x__format_resolver_state__mutmut_20(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append(None)


def x__format_resolver_state__mutmut_21(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("XX\n  (Resolver not yet initialized)XX")


def x__format_resolver_state__mutmut_22(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (resolver not yet initialized)")


def x__format_resolver_state__mutmut_23(resolver: EventSetResolver, lines: list[str]) -> None:
    """Format the resolver state section."""
    if resolver._resolved:
        lines.append("\nResolver State:")
        lines.append(f"  Total Field Mappings: {len(resolver._field_mappings)}")
        lines.append(f"  Total Event Sets: {len(resolver._event_mappings_by_set)}")

        # Show sample visual markers
        if resolver._event_mappings_by_set:
            lines.append("\n  Sample Visual Markers:")
            for name, mappings in list(resolver._event_mappings_by_set.items())[:3]:
                for mapping in mappings[:1]:  # Just show first mapping from each set
                    if mapping.visual_markers:
                        sample_markers = list(mapping.visual_markers.items())[:3]
                        lines.append(f"    {name}:")
                        for key, marker in sample_markers:
                            lines.append(f"      {marker} -> {key}")
                        break  # Only show first mapping with visual markers
    else:
        lines.append("\n  (RESOLVER NOT YET INITIALIZED)")

x__format_resolver_state__mutmut_mutants : ClassVar[MutantDict] = {
'x__format_resolver_state__mutmut_1': x__format_resolver_state__mutmut_1, 
    'x__format_resolver_state__mutmut_2': x__format_resolver_state__mutmut_2, 
    'x__format_resolver_state__mutmut_3': x__format_resolver_state__mutmut_3, 
    'x__format_resolver_state__mutmut_4': x__format_resolver_state__mutmut_4, 
    'x__format_resolver_state__mutmut_5': x__format_resolver_state__mutmut_5, 
    'x__format_resolver_state__mutmut_6': x__format_resolver_state__mutmut_6, 
    'x__format_resolver_state__mutmut_7': x__format_resolver_state__mutmut_7, 
    'x__format_resolver_state__mutmut_8': x__format_resolver_state__mutmut_8, 
    'x__format_resolver_state__mutmut_9': x__format_resolver_state__mutmut_9, 
    'x__format_resolver_state__mutmut_10': x__format_resolver_state__mutmut_10, 
    'x__format_resolver_state__mutmut_11': x__format_resolver_state__mutmut_11, 
    'x__format_resolver_state__mutmut_12': x__format_resolver_state__mutmut_12, 
    'x__format_resolver_state__mutmut_13': x__format_resolver_state__mutmut_13, 
    'x__format_resolver_state__mutmut_14': x__format_resolver_state__mutmut_14, 
    'x__format_resolver_state__mutmut_15': x__format_resolver_state__mutmut_15, 
    'x__format_resolver_state__mutmut_16': x__format_resolver_state__mutmut_16, 
    'x__format_resolver_state__mutmut_17': x__format_resolver_state__mutmut_17, 
    'x__format_resolver_state__mutmut_18': x__format_resolver_state__mutmut_18, 
    'x__format_resolver_state__mutmut_19': x__format_resolver_state__mutmut_19, 
    'x__format_resolver_state__mutmut_20': x__format_resolver_state__mutmut_20, 
    'x__format_resolver_state__mutmut_21': x__format_resolver_state__mutmut_21, 
    'x__format_resolver_state__mutmut_22': x__format_resolver_state__mutmut_22, 
    'x__format_resolver_state__mutmut_23': x__format_resolver_state__mutmut_23
}

def _format_resolver_state(*args, **kwargs):
    result = _mutmut_trampoline(x__format_resolver_state__mutmut_orig, x__format_resolver_state__mutmut_mutants, args, kwargs)
    return result 

_format_resolver_state.__signature__ = _mutmut_signature(x__format_resolver_state__mutmut_orig)
x__format_resolver_state__mutmut_orig.__name__ = 'x__format_resolver_state'


def x_show_event_matrix__mutmut_orig() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_1() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = None
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_2() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = None

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_3() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = None
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_4() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["XXFoundation Event Sets: Active ConfigurationXX"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_5() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["foundation event sets: active configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_6() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["FOUNDATION EVENT SETS: ACTIVE CONFIGURATION"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_7() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append(None)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_8() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" / 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_9() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("XX=XX" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_10() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 71)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_11() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = None
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_12() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(None, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_13() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, None)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_14() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_15() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, )

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_16() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append(None)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_17() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" - "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_18() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("XX\nXX" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_19() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" / 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_20() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "XX=XX" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_21() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 71)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_22() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(None, lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_23() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, None)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_24() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(lines)

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_25() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, )

    # Log the complete display
    log.info("\n".join(lines))


def x_show_event_matrix__mutmut_26() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info(None)


def x_show_event_matrix__mutmut_27() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("\n".join(None))


def x_show_event_matrix__mutmut_28() -> None:
    """Display the active event set configuration to the console.
    Shows all registered event sets and their field mappings.
    """
    # Ensure event sets are discovered
    discover_event_sets()

    registry = get_registry()
    resolver = get_resolver()

    # Force resolution to ensure everything is loaded
    resolver.resolve()

    lines: list[str] = ["Foundation Event Sets: Active Configuration"]
    lines.append("=" * 70)

    # Show registered event sets
    event_sets = registry.list_event_sets()
    _format_registered_event_sets(event_sets, lines)

    lines.append("\n" + "=" * 70)

    # Show resolved state
    _format_resolver_state(resolver, lines)

    # Log the complete display
    log.info("XX\nXX".join(lines))

x_show_event_matrix__mutmut_mutants : ClassVar[MutantDict] = {
'x_show_event_matrix__mutmut_1': x_show_event_matrix__mutmut_1, 
    'x_show_event_matrix__mutmut_2': x_show_event_matrix__mutmut_2, 
    'x_show_event_matrix__mutmut_3': x_show_event_matrix__mutmut_3, 
    'x_show_event_matrix__mutmut_4': x_show_event_matrix__mutmut_4, 
    'x_show_event_matrix__mutmut_5': x_show_event_matrix__mutmut_5, 
    'x_show_event_matrix__mutmut_6': x_show_event_matrix__mutmut_6, 
    'x_show_event_matrix__mutmut_7': x_show_event_matrix__mutmut_7, 
    'x_show_event_matrix__mutmut_8': x_show_event_matrix__mutmut_8, 
    'x_show_event_matrix__mutmut_9': x_show_event_matrix__mutmut_9, 
    'x_show_event_matrix__mutmut_10': x_show_event_matrix__mutmut_10, 
    'x_show_event_matrix__mutmut_11': x_show_event_matrix__mutmut_11, 
    'x_show_event_matrix__mutmut_12': x_show_event_matrix__mutmut_12, 
    'x_show_event_matrix__mutmut_13': x_show_event_matrix__mutmut_13, 
    'x_show_event_matrix__mutmut_14': x_show_event_matrix__mutmut_14, 
    'x_show_event_matrix__mutmut_15': x_show_event_matrix__mutmut_15, 
    'x_show_event_matrix__mutmut_16': x_show_event_matrix__mutmut_16, 
    'x_show_event_matrix__mutmut_17': x_show_event_matrix__mutmut_17, 
    'x_show_event_matrix__mutmut_18': x_show_event_matrix__mutmut_18, 
    'x_show_event_matrix__mutmut_19': x_show_event_matrix__mutmut_19, 
    'x_show_event_matrix__mutmut_20': x_show_event_matrix__mutmut_20, 
    'x_show_event_matrix__mutmut_21': x_show_event_matrix__mutmut_21, 
    'x_show_event_matrix__mutmut_22': x_show_event_matrix__mutmut_22, 
    'x_show_event_matrix__mutmut_23': x_show_event_matrix__mutmut_23, 
    'x_show_event_matrix__mutmut_24': x_show_event_matrix__mutmut_24, 
    'x_show_event_matrix__mutmut_25': x_show_event_matrix__mutmut_25, 
    'x_show_event_matrix__mutmut_26': x_show_event_matrix__mutmut_26, 
    'x_show_event_matrix__mutmut_27': x_show_event_matrix__mutmut_27, 
    'x_show_event_matrix__mutmut_28': x_show_event_matrix__mutmut_28
}

def show_event_matrix(*args, **kwargs):
    result = _mutmut_trampoline(x_show_event_matrix__mutmut_orig, x_show_event_matrix__mutmut_mutants, args, kwargs)
    return result 

show_event_matrix.__signature__ = _mutmut_signature(x_show_event_matrix__mutmut_orig)
x_show_event_matrix__mutmut_orig.__name__ = 'x_show_event_matrix'


# <3 🧱🤝📊🪄
